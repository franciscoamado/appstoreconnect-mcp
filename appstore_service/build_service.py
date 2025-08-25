"""Service for managing App Store Connect build operations."""
import requests
from .api_auth import AppStoreConnectAuth

# Default timeout for all requests (30 seconds)
REQUEST_TIMEOUT = 30


class BuildService:
    """Service for managing App Store Connect build operations."""

    def __init__(self, auth: AppStoreConnectAuth):
        self.auth = auth

    def list_builds(self, app_id: str):
        """
        Fetch a list of builds for a specific app.
        Endpoint: GET https://api.appstoreconnect.apple.com/v1/builds
        ?filter[app]={APP_ID}&include=preReleaseVersion
        """
        url = f"{self.auth.base_url}/builds?filter[app]={app_id}&include=preReleaseVersion&limit=50"
        response = requests.get(
            url, headers=self.auth.headers, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return response.json()

    def get_build_details(self, build_id: str):
        """
        Fetch details for a specific build.
        Endpoint: GET https://api.appstoreconnect.apple.com/v1/builds/{build_id}
        """
        url = f"{self.auth.base_url}/builds/{build_id}"
        response = requests.get(
            url, headers=self.auth.headers, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return response.json()
