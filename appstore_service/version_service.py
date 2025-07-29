from .api_auth import AppStoreConnectAuth
import requests

class VersionService:
    def __init__(self, auth: AppStoreConnectAuth):
        self.auth = auth

    def create_version(self, app_id: str, version_string: str, platform: str = "IOS"):
        """
        Create a new version for an app.
        """
        url = f"{self.auth.base_url}/appStoreVersions"
        payload = {
            "data": {
                "type": "appStoreVersions",
                "attributes": {
                    "versionString": version_string,
                    "platform": platform
                },
                "relationships": {
                    "app": {
                        "data": {
                            "type": "apps",
                            "id": app_id
                        }
                    }
                }
            }
        }
        response = requests.post(url, headers=self.auth.headers, json=payload)
        response.raise_for_status()
        return response.json()

    def get_version(self, app_id: str, version_string: str):
        """
        Get an app store version by version string.
        """
        url = f"{self.auth.base_url}/appStoreVersions?filter[app]={app_id}&filter[versionString]={version_string}"
        response = requests.get(url, headers=self.auth.headers)
        response.raise_for_status()
        return response.json()

    def associate_build_to_version(self, version_id: str, build_id: str):
        """
        Associate a build with an app version.
        """
        url = f"{self.auth.base_url}/appStoreVersions/{version_id}/relationships/build"
        payload = {
            "data": {
                "type": "builds",
                "id": build_id
            }
        }
        response = requests.patch(url, headers=self.auth.headers, json=payload)
        response.raise_for_status()
        return response.json()

    def submit_for_review(self, version_id: str):
        """
        Submit an app version for review.
        """
        url = f"{self.auth.base_url}/appStoreVersionSubmissions"
        payload = {
            "data": {
                "type": "appStoreVersionSubmissions",
                "relationships": {
                    "appStoreVersion": {
                        "data": {
                            "type": "appStoreVersions",
                            "id": version_id
                        }
                    }
                }
            }
        }
        response = requests.post(url, headers=self.auth.headers, json=payload)
        response.raise_for_status()
        return response.json()

    def release_pending_version(self, version_id: str):
        """
        Release an approved app version that is pending developer release.
        """
        url = f"{self.auth.base_url}/appStoreVersionReleaseRequests"
        payload = {
            "data": {
                "type": "appStoreVersionReleaseRequests",
                "relationships": {
                    "appStoreVersion": {
                        "data": {
                            "type": "appStoreVersions",
                            "id": version_id
                        }
                    }
                }
            }
        }
        response = requests.post(url, headers=self.auth.headers, json=payload)
        response.raise_for_status()
        return response.json()

    def list(self, app_id: str):
        """
        List all app store versions for an app.
        """
        url = f"{self.auth.base_url}/apps/{app_id}/appStoreVersions"
        response = requests.get(url, headers=self.auth.headers)
        response.raise_for_status()
        return response.json() 