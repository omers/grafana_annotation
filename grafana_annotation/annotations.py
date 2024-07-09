import requests
import json

class GrafanaAnnotator:
    def __init__(self, grafana_url, api_key):
        self.grafana_url = grafana_url.rstrip('/')  # Ensure no trailing slash
        self.api_key = api_key

    def create_annotation(self, timestamp, description):
        url = f"{self.grafana_url}/api/annotations"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        data = {
            "time": int(timestamp),
            "text": description,
            "tags": ["python"]
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))

        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()  # Raise HTTPError for non-200 responses
