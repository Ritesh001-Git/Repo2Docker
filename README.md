# Repo2Docker — DevOps Automation Platform

Repo2Docker is a web-based DevOps automation platform that takes a public GitHub repository and automates the process of building a Docker image, publishing it to Docker Hub, and deploying it to Kubernetes for a preview environment. It combines a React frontend, a FastAPI backend, Jenkins CI/CD pipelines, Docker, AWS infrastructure provisioned with Terraform, and an observability stack.

The platform is designed to make application packaging and deployment easier: users submit repository details through the UI, follow build status and logs, and receive Docker usage commands or a preview link when the relevant deployment workflow succeeds. When a build fails, the backend can use the Google Gemini API to provide a plain-language explanation.

> **Project status:** Capabilities depend on the configured Jenkins pipeline, AWS/K3s environment, and observability services. Review the configuration and pipeline files in this repository before deploying to a new environment.

## 🎥 Workflow Animation

The animation below demonstrates the Repo2Docker workflow, including GitHub repository cloning, Jenkins CI/CD, Docker image build and push, Kubernetes deployment, and AI-assisted error analysis.

https://github.com/user-attachments/assets/197e3bf0-1bc0-4819-a007-8679df75bc0a

## Key Features

- **Repository-based builds:** Submit a public GitHub repository URL and build configuration from the web interface.
- **Automated CI/CD:** Use Jenkins pipelines to clone source code, validate the Dockerfile, build a container image, and publish it to Docker Hub.
- **Build status and logs:** The FastAPI backend stores build metadata, status, and logs in SQLite for the frontend to retrieve.
- **AI-assisted troubleshooting:** Google Gemini can explain build failures in plain language when the API is configured.
- **Kubernetes preview deployments:** In the configured K3s/Helm workflow, successfully built images can be deployed as preview applications.
- **Infrastructure as Code:** Terraform provisions the AWS infrastructure defined by the project configuration.
- **Observability:** Prometheus and Grafana provide metrics and dashboards; ELK components support log collection and analysis; OpenTelemetry and Jaeger support request tracing.

## How It Works

1. **User submits configuration** in the React web interface, such as the GitHub repository URL, image name, and application port.
2. **FastAPI validates and records the request** and triggers the configured Jenkins job.
3. **Jenkins runs the pipeline:** clone the repository, check for a Dockerfile, build the image, and push it to Docker Hub when the pipeline succeeds.
4. **Build status and logs are collected** and made available through the backend API and frontend.
5. **Deployment workflow (when configured):** the image is deployed to K3s using Kubernetes resources managed through Helm. A preview URL is available when the deployment and ingress configuration support it.
6. **Observability services collect operational data:** Prometheus scrapes metrics, Grafana displays dashboards, the ELK stack handles logs, and OpenTelemetry/Jaeger support tracing.
7. **Failure explanation (when configured):** the backend can send relevant failure details to Gemini and show a plain-language explanation.

## Technology Stack and Purpose

| Technology | Purpose in Repo2Docker |
|---|---|
| React | Builds the interactive web interface and dashboard. |
| Vite | Development server and frontend build tooling. |
| Tailwind CSS | Styles the frontend UI. |
| Axios | Sends HTTP requests from the frontend to the backend API. |
| FastAPI | Provides API endpoints for starting builds and retrieving status/logs. |
| Pydantic | Validates API request and response data. |
| SQLAlchemy | Maps build records to database models. |
| SQLite | Stores build metadata, status, and logs for the MVP. |
| Requests | Allows backend services to call Jenkins and other HTTP APIs. |
| Jenkins Pipeline | Automates repository checkout, validation, image building, scanning where configured, publishing, and deployment stages. |
| Docker | Packages applications into portable container images. |
| Docker Hub | Stores and distributes built container images. |
| Kubernetes (K3s) | Runs the platform and configured preview applications on a lightweight Kubernetes cluster. |
| Helm | Packages and configures Kubernetes resources for repeatable deployment. |
| Terraform | Provisions AWS infrastructure defined by the Terraform configuration. |
| AWS EC2 | Hosts the project services and K3s cluster in the single-instance deployment model. |
| AWS VPC and Security Groups | Provide network isolation and control inbound/outbound access according to configured rules. |
| Trivy (if configured) | Scans container images for vulnerabilities in the production pipeline. |
| Google Gemini API | Generates plain-language explanations of build failures. |
| Prometheus | Collects time-series metrics from configured targets. |
| Grafana | Visualizes metrics through dashboards. |
| Node Exporter | Exposes host-level metrics. |
| kube-state-metrics | Exposes Kubernetes object and workload state metrics. |
| Filebeat, Logstash, Elasticsearch, Kibana (ELK) | Collect, process, index, and explore logs. |
| OpenTelemetry | Instruments or exports telemetry for tracing, depending on the application configuration. |
| Jaeger | Receives and displays distributed traces. |

## Architecture at a Glance

```text
User
  |
  v
React + Vite Frontend
  |
  | HTTP API requests
  v
FastAPI Backend -----> SQLite (build records, status, logs)
  |
  | Trigger Jenkins job / retrieve build information
  v
Jenkins Pipeline
  |
  +--> Clone GitHub repository
  +--> Validate Dockerfile
  +--> Build Docker image
  +--> Optional vulnerability scan (Trivy)
  +--> Push image to Docker Hub
  |
  +--> Optional deployment stage
          |
          v
      Helm / Kubernetes (K3s on AWS EC2)
          |
          +--> Application Deployment and Service
          +--> Ingress / preview URL (if configured)
          +--> HPA (if configured)

Observability:
  Metrics: Prometheus --> Grafana
  Host/Kubernetes metrics: Node Exporter + kube-state-metrics --> Prometheus
  Logs: Filebeat --> Logstash --> Elasticsearch --> Kibana
  Traces: OpenTelemetry --> Jaeger
```

## Repository Structure

The following is a representative structure based on the project layout; optional deployment and observability folders may differ by branch.

```text
.
├── backend/
│   ├── app/
│   │   ├── api/              # FastAPI routes
│   │   ├── services/         # Jenkins, Gemini, and build orchestration
│   │   ├── config.py         # Environment-based configuration
│   │   ├── database.py       # Database setup
│   │   ├── models.py         # SQLAlchemy models
│   │   └── schemas.py        # Pydantic schemas
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   └── src/
│       ├── pages/            # Dashboard, build status, and result views
│       └── services/api.js   # Axios API client
├── jenkins/
│   ├── Jenkinsfile           # Build pipeline
│   └── Jenkinsfile.production # Production pipeline, if present
├── charts/                   # Helm chart(s), if present
├── terraform/                # AWS infrastructure definitions, if present
└── README.md
```

## Prerequisites

Install or prepare the tools required for the parts you intend to run:

- Git
- Python version supported by `backend/requirements.txt`
- Node.js and npm compatible with the frontend lockfile
- Docker Engine/Desktop
- A running Jenkins controller and an agent that can run Git and Docker commands
- Docker Hub account and access token
- Terraform and AWS CLI for AWS provisioning
- `kubectl`, K3s, and Helm for Kubernetes deployment and verification
- Optional: Trivy, Google Gemini API key, Prometheus, Grafana, ELK, OpenTelemetry, and Jaeger

> Versions and exact requirements should be taken from the repository's dependency files and deployment configuration.

## Configuration and Secrets

Create local environment files from the provided examples where available (`.env.example`). Do not commit `.env` files, API keys, passwords, access tokens, private keys, or Terraform state containing sensitive values.

Typical backend configuration:

```env
DATABASE_URL=sqlite:///./repo2docker.db
CORS_ORIGINS=http://localhost:5173
JENKINS_URL=http://localhost:8080
JENKINS_JOB_NAME=repo2docker
JENKINS_USERNAME=your-jenkins-user
JENKINS_API_TOKEN=your-jenkins-api-token
GEMINI_API_KEY=your-gemini-api-key
DOCKERHUB_USERNAME=your-dockerhub-username
```

Use the variable names actually read by your current backend configuration. The list above follows the supplied earlier README and may need adjustment if the implementation has changed.

## Local Development

### 1. Start the backend

```bash
cd backend
python -m venv .venv

# macOS / Linux
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create a local environment file if an example is provided
cp .env.example .env

# Start FastAPI
uvicorn app.main:app --reload
```

Backend base URL: `http://localhost:8000`

If enabled in the application, interactive API documentation is available at `http://localhost:8000/docs`.

### 2. Start the frontend

Open a second terminal:

```bash
cd frontend
npm install

# Create a local environment file if an example is provided
cp .env.example .env

npm run dev
```

Frontend URL: `http://localhost:5173`

Ensure the frontend's API base URL points to the running backend. Check the existing Axios client and environment-variable conventions before changing it.

## Jenkins Configuration

1. Create the Jenkins job expected by the backend (the supplied README uses `repo2docker`).
2. Configure the job to use the appropriate Jenkinsfile from this repository.
3. Ensure the Jenkins agent has Git and Docker installed and permission to execute Docker commands.
4. Configure Jenkins credentials rather than hardcoding secrets in a pipeline.
5. Add Docker Hub credentials using the credential ID referenced by the Jenkinsfile (the earlier configuration uses `dockerhub-credentials`).
6. Configure any required build parameters to match the backend request and Jenkinsfile.

The earlier MVP pipeline used the parameters `REPO_URL`, `IMAGE_NAME`, and `PORT`, and checked for `source/Dockerfile` in the cloned repository. If your current Jenkinsfile instead uses different parameter names or expects `Dockerfile` at the repository root, update this section and the backend together. The Jenkinsfile is the source of truth for the actual pipeline behavior.

## Kubernetes / K3s Deployment

For deployments using the K3s and Helm setup:

1. Provision the required AWS infrastructure using the Terraform configuration.
2. Install or verify K3s on the target EC2 instance.
3. Configure `kubectl` access to the cluster.
4. Configure image repositories, tags, ingress, secrets, and application settings in the Helm values.
5. Deploy or upgrade the application using the chart included in the repository.

Example command (adjust the chart path, values, and image names to your configuration):

```bash
helm upgrade --install repo2docker charts/repo2docker \
  --namespace repo2docker \
  --create-namespace
```

Verify the deployment:

```bash
kubectl get nodes
kubectl get pods -n repo2docker
kubectl get services -n repo2docker
kubectl get ingress -n repo2docker
kubectl get hpa -n repo2docker
```

These commands assume the namespace and resource types are enabled in your chart. A preview deployment also depends on the backend deployment logic, permissions, ingress/DNS configuration, and the availability of the built image.

## AWS Infrastructure with Terraform

Terraform is used to create the AWS resources defined in the project's `.tf` files, such as EC2, networking, security groups, and optionally an Elastic IP. The exact resources depend on the Terraform configuration.

From the directory containing the Terraform configuration:

```bash
terraform init
terraform validate
terraform plan
terraform apply
```

After the demonstration or test, review the plan carefully and remove resources that were created solely for the project:

```bash
terraform destroy
```

Before destroying resources, confirm that no data or infrastructure you need will be removed. Check the AWS Console afterward for resources not managed by the same Terraform state, including EBS volumes, snapshots, Elastic IPs, load balancers, and NAT Gateways. AWS charges may continue for resources left behind.

## API Endpoints

The earlier MVP README documented these endpoints. Confirm their current paths and schemas in the FastAPI routes before relying on them.

### `POST /build`

Starts a Jenkins build.

Example request:

```json
{
  "repository_url": "https://github.com/user/project",
  "image_name": "my-app",
  "port": 3000
}
```

### `GET /status/{build_id}`

Retrieves build metadata and current status.

### `GET /logs/{build_id}`

Retrieves saved Jenkins logs and, where configured, a Gemini failure explanation or Docker commands for a successful build.

## Monitoring, Logging, and Tracing

The optional observability stack is intended to help inspect application and infrastructure behavior:

- **Prometheus:** scrapes metrics from configured endpoints and exporters.
- **Grafana:** displays dashboards using Prometheus as a data source.
- **Node Exporter:** exposes host metrics.
- **kube-state-metrics:** exposes Kubernetes object and workload state.
- **ELK:** Filebeat collects logs, Logstash processes them, Elasticsearch indexes them, and Kibana provides search and visualization.
- **OpenTelemetry + Jaeger:** supports instrumentation and trace collection/inspection when the application and exporters are configured correctly.

The exact scrape targets, ports, dashboards, retention settings, and tracing exporters are defined by the project's deployment and configuration files. Confirm those settings before the demo.

## Troubleshooting

| Symptom | Checks |
|---|---|
| Frontend cannot reach FastAPI | Verify the backend is running, the API base URL is correct, and CORS allows the frontend origin. |
| Jenkins build does not start | Check `JENKINS_URL`, job name, Jenkins username/API token, job parameters, and Jenkins logs. |
| Docker build fails | Check the repository's Dockerfile location, build context, and build logs. |
| Docker Hub push fails | Verify the image name, Docker Hub credentials, credential ID, and registry permissions. |
| Kubernetes pods do not start | Inspect `kubectl describe pod`, `kubectl logs`, image pull errors, resource limits, and cluster capacity. |
| Preview URL is inaccessible | Check Ingress resources, ingress controller, host/DNS configuration, security-group rules, and service endpoints. |
| Metrics or traces are missing | Verify exporter/instrumentation configuration, service endpoints, Prometheus targets, and OpenTelemetry exporter settings. |
| Elasticsearch is unhealthy | Check available memory, JVM heap, disk space, and container logs. |

## Security Notes

- Use Jenkins credentials and Kubernetes Secrets for sensitive values.
- Do not expose Jenkins, Prometheus, Grafana, Elasticsearch, Kibana, or Jaeger publicly without authentication and appropriate network restrictions.
- Limit EC2 security-group inbound rules to the required source IPs and ports.
- Treat user-provided repository URLs as untrusted input; validate them and avoid executing untrusted code on privileged build agents.
- Keep dependencies and container images updated, and use image scanning where configured.
- Avoid storing secrets in Git, build logs, frontend bundles, or public Docker images.

## Limitations and Scope

- Public GitHub repositories are the intended input for the documented MVP flow; private repository access requires additional authentication setup.
- Build and deployment behavior depends on the Jenkinsfile and deployment configuration currently checked into the repository.
- Kubernetes preview deployment and observability features require the corresponding infrastructure and services to be provisioned and configured.
- A single EC2 host is cost-effective for a demonstration but is not a highly available production architecture. Kubernetes HPA scales pods; it does not automatically scale the underlying EC2 instance.

## Future Improvements

- Add authentication and authorization for users and build operations.
- Add stronger repository validation, build isolation, quotas, and cleanup policies.
- Add automated unit and integration test coverage.
- Improve build cancellation, retries, and structured failure reporting.
- Add configurable image retention and preview-environment expiration.
- Add alerting, dashboards, and observability retention policies.
- Move to a managed database and a multi-node cluster for production workloads if required.

## License

Add the license used by this repository here. If no license has been selected, state that the project is currently unlicensed rather than implying permission to reuse the code.
