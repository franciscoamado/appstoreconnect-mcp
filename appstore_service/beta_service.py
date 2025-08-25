"""Service for managing App Store Connect beta testing operations."""
import requests
from .api_auth import AppStoreConnectAuth

# Default timeout for all requests (30 seconds)
REQUEST_TIMEOUT = 30


class BetaService:
    """Service for managing App Store Connect beta testing functionality."""

    def __init__(self, auth: AppStoreConnectAuth):
        self.auth = auth

    def fetch_beta_groups(self, app_id: str):
        """
        Fetch a list of beta groups for a specific app.
        """
        url = f"{self.auth.base_url}/betaGroups?filter[app]={app_id}"
        response = requests.get(
            url,
            headers=self.auth.headers,
            timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return response.json()

    def add_tester_to_groups(
            self,
            email: str,
            group_ids: list,
            first_name: str = None,
            last_name: str = None):
        """
        Add a new beta tester and assign them to specified beta groups.
        """
        url = f"{self.auth.base_url}/betaTesters"
        group_data = [{"type": "betaGroups", "id": group_id}
                      for group_id in group_ids]

        attributes = {"email": email}
        if first_name:
            attributes["firstName"] = first_name
        if last_name:
            attributes["lastName"] = last_name

        payload = {
            "data": {
                "type": "betaTesters",
                "attributes": attributes,
                "relationships": {
                    "betaGroups": {
                        "data": group_data
                    }
                }
            }
        }

        response = requests.post(
            url,
            headers=self.auth.headers,
            json=payload,
            timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return response.json()

    def _get_beta_tester_id_by_email(self, email: str, app_id: str):
        """
        Helper function to find a beta tester's ID by their email for a specific app.
        """
        url = f"{self.auth.base_url}/betaTesters?filter[email]={email}&filter[apps]={app_id}"
        response = requests.get(
            url,
            headers=self.auth.headers,
            timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        data = response.json()
        if data.get("data"):
            return data["data"][0]["id"]
        return None

    def remove_tester_from_groups(
            self,
            email: str,
            group_ids: list,
            app_id: str):
        """
        Remove a beta tester from specified beta groups.
        """
        tester_id = self._get_beta_tester_id_by_email(email, app_id)
        if not tester_id:
            return False

        url = f"{self.auth.base_url}/betaTesters/{tester_id}/relationships/betaGroups"
        linkages_data = [{"type": "betaGroups", "id": group_id}
                         for group_id in group_ids]
        payload = {"data": linkages_data}

        response = requests.delete(
            url,
            headers=self.auth.headers,
            json=payload,
            timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return response.status_code == 204

    def list_beta_testers(self, app_id: str):
        """
        List all beta testers for a specific app.
        """
        url = f"{self.auth.base_url}/betaTesters?filter[apps]={app_id}"
        response = requests.get(
            url,
            headers=self.auth.headers,
            timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return response.json()

    def list_testers_in_group(self, group_id: str):
        """
        Fetch a list of beta testers from a specific beta group.
        """
        url = f"{self.auth.base_url}/betaGroups/{group_id}/betaTesters"
        response = requests.get(
            url,
            headers=self.auth.headers,
            timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return response.json()

    def create_beta_group(self, app_id: str, name: str):
        """
        Create a new beta group for a specific app.
        """
        url = f"{self.auth.base_url}/betaGroups"
        payload = {
            "data": {
                "type": "betaGroups",
                "attributes": {
                    "name": name
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
        response = requests.post(
            url,
            headers=self.auth.headers,
            json=payload,
            timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return response.json()
