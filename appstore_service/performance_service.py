import requests
from .api_auth import AppStoreConnectAuth

class PerformanceService:
    def __init__(self, auth: AppStoreConnectAuth):
        self.auth = auth

    def get_perf_power_metrics(self, app_id: str):
        """
        Get a list of performance power metrics for a specific app.
        """
        url = f"{self.auth.base_url}/apps/{app_id}/perfPowerMetrics"
        response = requests.get(url, headers=self.auth.headers)
        response.raise_for_status()
        return response.json() 