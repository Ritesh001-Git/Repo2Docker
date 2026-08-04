# Repo2Docker

Repo2Docker is a simple web app that builds and pushes a Docker image from a public GitHub repository using Jenkins.

The app accepts a GitHub repository URL, Docker image name, and port number. FastAPI triggers a parameterized Jenkins build, stores status and logs in SQLite, and asks Google Gemini for a plain-language explanation when a build fails.

## Stack

- Frontend: React, Vite, Tailwind CSS, Axios
- Backend: FastAPI, SQLite, SQLAlchemy, Requests
- CI: Jenkins Pipeline
- Container: Docker
- AI: Google Gemini API

## Project Structure

```text
backend/
  app/
    api/              FastAPI routes
    services/         Jenkins, Gemini, and build orchestration services
    config.py         Environment variable settings
    database.py       SQLite setup
    models.py         SQLAlchemy models
    schemas.py        Pydantic request and response models
  Dockerfile
  requirements.txt
frontend/
  src/
    pages/            Dashboard, Build Status, Build Result
    services/api.js   Axios API client
jenkins/
  Jenkinsfile         Sample parameterized Jenkins pipeline
```

## Backend Setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

Backend runs at `http://localhost:8000`.

Required backend environment variables:

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

## Frontend Setup

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

Frontend runs at `http://localhost:5173`.

## Jenkins Setup

1. Create a Jenkins Pipeline job named `repo2docker`.
2. Use `jenkins/Jenkinsfile` as the pipeline definition.
3. Ensure the Jenkins agent has `git` and `docker` installed.
4. Give the Jenkins agent permission to run Docker commands.
5. Add Docker Hub credentials in Jenkins:
   - Kind: Username with password
   - ID: `dockerhub-credentials`
   - Username: your Docker Hub username
   - Password: your Docker Hub token or password

The pipeline accepts these parameters:

- `REPO_URL`
- `IMAGE_NAME`
- `PORT`

For the MVP, the pipeline checks only `source/Dockerfile`, which means the Dockerfile must exist at the repository root.

## API

### `POST /build`

Starts a Jenkins build and returns a local build ID.

```json
{
  "repository_url": "https://github.com/user/project",
  "image_name": "my-app",
  "port": 3000
}
```

### `GET /status/{build_id}`

Returns build metadata and current status.

### `GET /logs/{build_id}`

Returns saved Jenkins logs, Gemini explanation for failures, and Docker commands for successful builds.

## Backend Docker Image

```bash
cd backend
docker build -t repo2docker-backend .
docker run --env-file .env -p 8000:8000 repo2docker-backend
```

## Success Output

When a build succeeds, the UI displays:

```bash
docker pull <dockerhub_username>/<image_name>:latest
docker run -d -p <user_port>:<user_port> <dockerhub_username>/<image_name>:latest
```
