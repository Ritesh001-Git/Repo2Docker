from dataclasses import dataclass

from app.config import Settings


@dataclass
class PreviewDeployment:
    namespace: str
    url: str
    status: str


class KubernetesPreviewService:
    """Creates short-lived Kubernetes preview apps for successfully built images."""

    def __init__(self, settings: Settings):
        self.settings = settings

    def deploy_preview(self, build_id: int, image_name: str, port: int) -> PreviewDeployment | None:
        if not self.settings.preview_deploy_enabled:
            return None
        if not self.settings.dockerhub_username:
            raise RuntimeError("DOCKERHUB_USERNAME is required for preview deployments.")

        try:
            from kubernetes import client, config
            from kubernetes.client.rest import ApiException
        except ImportError as exc:
            raise RuntimeError("Install the kubernetes Python package to enable previews.") from exc

        try:
            config.load_incluster_config()
        except Exception:
            config.load_kube_config()

        namespace = f"{self.settings.preview_namespace_prefix}-{build_id}"
        app_name = f"preview-{build_id}"
        image = f"{self.settings.dockerhub_username}/{image_name}:latest"
        path = f"/apps/{build_id}"
        preview_url = f"{self.settings.preview_base_url.rstrip('/')}{path}"

        core = client.CoreV1Api()
        apps = client.AppsV1Api()
        networking = client.NetworkingV1Api()
        autoscaling = client.AutoscalingV2Api()
        custom = client.CustomObjectsApi()

        try:
            core.create_namespace(
                client.V1Namespace(
                    metadata=client.V1ObjectMeta(
                        name=namespace,
                        labels={
                            "repo2docker.io/preview": "true",
                            "repo2docker.io/build-id": str(build_id),
                        },
                    )
                )
            )
        except ApiException as exc:
            if exc.status != 409:
                raise

        labels = {"app": app_name, "repo2docker.io/build-id": str(build_id)}
        container = client.V1Container(
            name="app",
            image=image,
            image_pull_policy=self.settings.preview_image_pull_policy,
            ports=[client.V1ContainerPort(container_port=port)],
            resources=client.V1ResourceRequirements(
                requests={
                    "cpu": self.settings.preview_cpu_request,
                    "memory": self.settings.preview_memory_request,
                },
                limits={
                    "cpu": self.settings.preview_cpu_limit,
                    "memory": self.settings.preview_memory_limit,
                },
            ),
        )
        deployment = client.V1Deployment(
            metadata=client.V1ObjectMeta(name=app_name, namespace=namespace, labels=labels),
            spec=client.V1DeploymentSpec(
                replicas=1,
                selector=client.V1LabelSelector(match_labels=labels),
                template=client.V1PodTemplateSpec(
                    metadata=client.V1ObjectMeta(labels=labels),
                    spec=client.V1PodSpec(
                        automount_service_account_token=False,
                        containers=[container],
                    ),
                ),
            ),
        )
        service = client.V1Service(
            metadata=client.V1ObjectMeta(name=app_name, namespace=namespace, labels=labels),
            spec=client.V1ServiceSpec(
                selector=labels,
                ports=[client.V1ServicePort(name="http", port=80, target_port=port)],
                type="ClusterIP",
            ),
        )
        ingress = client.V1Ingress(
            metadata=client.V1ObjectMeta(
                name=app_name,
                namespace=namespace,
                annotations={
                    "nginx.ingress.kubernetes.io/rewrite-target": "/",
                    "traefik.ingress.kubernetes.io/router.middlewares": f"{namespace}-{app_name}-strip@kubernetescrd",
                },
            ),
            spec=client.V1IngressSpec(
                rules=[
                    client.V1IngressRule(
                        http=client.V1HTTPIngressRuleValue(
                            paths=[
                                client.V1HTTPIngressPath(
                                    path=path,
                                    path_type="Prefix",
                                    backend=client.V1IngressBackend(
                                        service=client.V1IngressServiceBackend(
                                            name=app_name,
                                            port=client.V1ServiceBackendPort(number=80),
                                        )
                                    ),
                                )
                            ]
                        )
                    )
                ]
            ),
        )
        hpa = client.V2HorizontalPodAutoscaler(
            metadata=client.V1ObjectMeta(name=app_name, namespace=namespace, labels=labels),
            spec=client.V2HorizontalPodAutoscalerSpec(
                min_replicas=self.settings.preview_min_replicas,
                max_replicas=self.settings.preview_max_replicas,
                scale_target_ref=client.V2CrossVersionObjectReference(
                    api_version="apps/v1",
                    kind="Deployment",
                    name=app_name,
                ),
                metrics=[
                    client.V2MetricSpec(
                        type="Resource",
                        resource=client.V2ResourceMetricSource(
                            name="cpu",
                            target=client.V2MetricTarget(
                                type="Utilization",
                                average_utilization=self.settings.preview_cpu_target_percentage,
                            ),
                        ),
                    )
                ],
            ),
        )

        self._create_or_replace(apps, namespace, app_name, deployment, "deployment")
        self._create_or_replace(core, namespace, app_name, service, "service")
        self._create_traefik_strip_prefix(custom, namespace, app_name, path)
        self._create_or_replace(networking, namespace, app_name, ingress, "ingress")
        self._create_or_replace(autoscaling, namespace, app_name, hpa, "hpa")

        return PreviewDeployment(namespace=namespace, url=preview_url, status="created")

    def _create_or_replace(self, api, namespace: str, name: str, body, kind: str) -> None:
        try:
            if kind == "deployment":
                api.create_namespaced_deployment(namespace=namespace, body=body)
            elif kind == "service":
                api.create_namespaced_service(namespace=namespace, body=body)
            elif kind == "ingress":
                api.create_namespaced_ingress(namespace=namespace, body=body)
            elif kind == "hpa":
                api.create_namespaced_horizontal_pod_autoscaler(namespace=namespace, body=body)
        except Exception as exc:
            status = getattr(exc, "status", None)
            if status != 409:
                raise
            if kind == "deployment":
                api.replace_namespaced_deployment(name=name, namespace=namespace, body=body)
            elif kind == "service":
                api.replace_namespaced_service(name=name, namespace=namespace, body=body)
            elif kind == "ingress":
                api.replace_namespaced_ingress(name=name, namespace=namespace, body=body)
            elif kind == "hpa":
                api.replace_namespaced_horizontal_pod_autoscaler(name=name, namespace=namespace, body=body)

    def _create_traefik_strip_prefix(self, api, namespace: str, name: str, path: str) -> None:
        body = {
            "apiVersion": "traefik.io/v1alpha1",
            "kind": "Middleware",
            "metadata": {"name": f"{name}-strip", "namespace": namespace},
            "spec": {"stripPrefix": {"prefixes": [path]}},
        }
        try:
            api.create_namespaced_custom_object(
                group="traefik.io",
                version="v1alpha1",
                namespace=namespace,
                plural="middlewares",
                body=body,
            )
        except Exception as exc:
            status = getattr(exc, "status", None)
            if status == 409:
                api.replace_namespaced_custom_object(
                    group="traefik.io",
                    version="v1alpha1",
                    namespace=namespace,
                    plural="middlewares",
                    name=f"{name}-strip",
                    body=body,
                )
