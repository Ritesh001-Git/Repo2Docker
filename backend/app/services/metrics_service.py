from prometheus_client import Counter, Gauge, Histogram


BUILD_REQUESTS = Counter(
    "repo2docker_build_requests_total",
    "Total number of build requests submitted.",
)
BUILD_SUCCESS = Counter(
    "repo2docker_build_success_total",
    "Total number of successful image builds.",
)
BUILD_FAILURE = Counter(
    "repo2docker_build_failure_total",
    "Total number of failed image builds.",
)
JENKINS_TRIGGER_ERRORS = Counter(
    "repo2docker_jenkins_trigger_errors_total",
    "Total Jenkins trigger or watch errors.",
)
GEMINI_EXPLANATIONS = Counter(
    "repo2docker_gemini_explanations_total",
    "Total Gemini or fallback explanations generated.",
)
PREVIEW_DEPLOYMENTS = Counter(
    "repo2docker_preview_deployments_total",
    "Total Kubernetes preview deployment attempts.",
    ["status"],
)
ACTIVE_BUILDS = Gauge(
    "repo2docker_active_builds",
    "Number of currently running builds.",
)
RUNNING_PREVIEW_APPS = Gauge(
    "repo2docker_running_preview_apps",
    "Number of preview applications created by Repo2Docker.",
)
BUILD_DURATION = Histogram(
    "repo2docker_build_duration_seconds",
    "Time spent waiting for Jenkins build completion.",
    buckets=(5, 15, 30, 60, 120, 300, 600, 1200, 1800, 3600),
)
HTTP_REQUEST_DURATION = Histogram(
    "repo2docker_api_request_duration_seconds",
    "FastAPI request latency by method, path, and status.",
    ["method", "path", "status_code"],
    buckets=(0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10),
)
