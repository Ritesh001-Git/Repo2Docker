import time
from urllib.parse import quote

import requests
from requests import Session

from app.config import Settings


class JenkinsService:
    """Jenkins REST API client for triggering and watching one parameterized job."""

    def __init__(self, settings: Settings):
        self.settings = settings
        self.session: Session = requests.Session()
        if settings.jenkins_username and settings.jenkins_api_token:
            self.session.auth = (settings.jenkins_username, settings.jenkins_api_token)

    @property
    def job_url(self) -> str:
        base = self.settings.jenkins_url.rstrip("/")
        encoded_job = quote(self.settings.jenkins_job_name, safe="")
        return f"{base}/job/{encoded_job}"

    def trigger_build(self, repository_url: str, image_name: str, port: int) -> str:
        url = f"{self.job_url}/buildWithParameters"
        response = self.session.post(
            url,
            data={"REPO_URL": repository_url, "IMAGE_NAME": image_name, "PORT": port},
            timeout=self.settings.jenkins_request_timeout_seconds,
        )
        response.raise_for_status()
        queue_url = response.headers.get("Location")
        if not queue_url:
            raise RuntimeError("Jenkins did not return a queue location.")
        return queue_url

    def wait_for_executable_url(self, queue_url: str) -> str:
        api_url = f"{queue_url.rstrip('/')}/api/json"
        while True:
            response = self.session.get(
                api_url, timeout=self.settings.jenkins_request_timeout_seconds
            )
            response.raise_for_status()
            item = response.json()
            executable = item.get("executable")
            if executable and executable.get("url"):
                return executable["url"]
            if item.get("cancelled"):
                raise RuntimeError("Jenkins queue item was cancelled.")
            time.sleep(self.settings.jenkins_poll_interval_seconds)

    def get_console_text(self, build_url: str) -> str:
        response = self.session.get(
            f"{build_url.rstrip('/')}/consoleText",
            timeout=self.settings.jenkins_request_timeout_seconds,
        )
        response.raise_for_status()
        return response.text

    def get_build_result(self, build_url: str) -> str | None:
        response = self.session.get(
            f"{build_url.rstrip('/')}/api/json",
            timeout=self.settings.jenkins_request_timeout_seconds,
        )
        response.raise_for_status()
        return response.json().get("result")

    def watch_build(self, build_url: str):
        while True:
            logs = self.get_console_text(build_url)
            result = self.get_build_result(build_url)
            yield logs, result
            if result is not None:
                return
            time.sleep(self.settings.jenkins_poll_interval_seconds)
