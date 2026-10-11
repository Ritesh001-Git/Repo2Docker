import time
import requests

from app.config import Settings


class GeminiService:
    """Explains Jenkins/Docker failures using Gemini with local fallback."""

    def __init__(self, settings: Settings):
        self.settings = settings

    def explain_failure(self, logs: str) -> str:

        if not self.settings.gemini_api_key:
            return self._fallback_explanation(logs)

        prompt = f"""
You are an experienced DevOps engineer.

Analyze the following Jenkins logs.

Respond ONLY in this format.

What happened:
<simple explanation>

Why it happened:
<reason>

How to fix it:
<steps>

Jenkins Logs:

{logs[-12000:]}
"""

        url = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            f"{self.settings.gemini_model}:generateContent"
        )

        body = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ]
        }

        headers = {
            "Content-Type": "application/json"
        }

        retries = 3

        for attempt in range(retries):

            try:

                response = requests.post(
                    url,
                    params={"key": self.settings.gemini_api_key},
                    headers=headers,
                    json=body,
                    timeout=30,
                )

                print("\n========== GEMINI DEBUG ==========")
                print("Attempt:", attempt + 1)
                print("Status :", response.status_code)
                print("Response:", response.text)
                print("==================================\n")

                if response.status_code == 200:

                    data = response.json()

                    candidates = data.get("candidates", [])

                    if not candidates:
                        return self._fallback_explanation(logs)

                    return (
                        candidates[0]
                        .get("content", {})
                        .get("parts", [{}])[0]
                        .get("text", self._fallback_explanation(logs))
                    )

                if response.status_code == 503:

                    if attempt < retries - 1:
                        time.sleep(2 ** attempt)
                        continue

                    return self._fallback_explanation(logs)

                if response.status_code == 429:

                    if attempt < retries - 1:
                        time.sleep(2 ** attempt)
                        continue

                    return self._fallback_explanation(logs)

                return self._fallback_explanation(logs)

            except requests.exceptions.Timeout:

                if attempt < retries - 1:
                    time.sleep(2 ** attempt)
                    continue

                return self._fallback_explanation(logs)

            except requests.exceptions.ConnectionError:
                return self._fallback_explanation(logs)

            except Exception:
                return self._fallback_explanation(logs)

        return self._fallback_explanation(logs)

    def _fallback_explanation(self, logs: str) -> str:

        logs = logs.lower()

        if "docker: command not found" in logs:
            return """
What happened:
Jenkins could not find the Docker command.

Why it happened:
Docker is not installed or Jenkins cannot access the Docker executable.

How to fix it:
1. Install Docker.
2. Add Docker to the system PATH.
3. Restart Jenkins.
"""

        if "cannot connect to the docker daemon" in logs:
            return """
What happened:
Jenkins could not connect to the Docker daemon.

Why it happened:
Docker is not running or Jenkins does not have permission to access Docker.

How to fix it:
1. Start Docker Desktop.
2. Verify Docker using 'docker info'.
3. Ensure Jenkins has permission to access Docker.
"""

        if "dockerfile" in logs and "no such file" in logs:
            return """
What happened:
Dockerfile was not found.

Why it happened:
The repository does not contain a Dockerfile in the expected location.

How to fix it:
1. Add a Dockerfile to the project root.
2. Commit and push the changes.
3. Trigger the build again.
"""

        if "authentication required" in logs:
            return """
What happened:
Docker Hub authentication failed.

Why it happened:
The Docker Hub username or password is incorrect.

How to fix it:
1. Verify Jenkins Docker credentials.
2. Update the Personal Access Token if required.
3. Retry the build.
"""

        if "requested access to the resource is denied" in logs:
            return """
What happened:
Docker Hub denied permission to push the image.

Why it happened:
The repository does not exist or you do not have permission.

How to fix it:
1. Verify the image name.
2. Verify Docker Hub username.
3. Create the repository if required.
"""

        if "repository does not exist" in logs:
            return """
What happened:
The GitHub repository could not be cloned.

Why it happened:
The repository URL is incorrect or inaccessible.

How to fix it:
1. Verify the GitHub repository URL.
2. Ensure the repository exists.
3. Check repository permissions.
"""

        if "failed to solve" in logs:
            return """
What happened:
Docker image build failed.

Why it happened:
An error occurred while executing the Dockerfile.

How to fix it:
1. Check the Dockerfile syntax.
2. Verify all COPY paths.
3. Ensure dependencies exist.
"""

        if "permission denied" in logs:
            return """
What happened:
Jenkins encountered a permission error.

Why it happened:
The Jenkins user does not have sufficient permissions.

How to fix it:
1. Grant the required permissions.
2. Restart Jenkins.
3. Retry the pipeline.
"""

        if "error response from daemon" in logs:
            return """
What happened:
Docker returned an error while processing the request.

Why it happened:
The Docker daemon rejected the operation.

How to fix it:
1. Check Docker daemon logs.
2. Verify Docker is running correctly.
3. Retry the build.
"""

        return """
What happened:
The Jenkins pipeline failed.

Why it happened:
The exact cause could not be determined automatically.

How to fix it:
1. Review the Jenkins logs below.
2. Verify the GitHub repository and Dockerfile.
3. Ensure Docker and Jenkins are configured correctly.
4. Retry the build after fixing the issue.
"""