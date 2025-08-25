"""Service for retrieving App Store Connect performance metrics."""
import requests
from .api_auth import AppStoreConnectAuth

# Default timeout for all requests (30 seconds)
REQUEST_TIMEOUT = 30


class PerformanceService:  # pylint: disable=too-few-public-methods
    """Service for retrieving App Store Connect performance and power metrics."""

    def __init__(self, auth: AppStoreConnectAuth):
        self.auth = auth

    def get_perf_power_metrics(self, app_id: str):
        """
        Get a list of performance power metrics for a specific app.
        """
        url = f"{self.auth.base_url}/apps/{app_id}/perfPowerMetrics"
        response = requests.get(
            url, headers=self.auth.headers, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return response.json()
