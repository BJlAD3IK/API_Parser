# api_parser.py
import requests
import yaml
from logger_config import log

class APISchemeParser:
    def __init__(self, url):
        self.url = url
        self.spec_data = {}
        self.endpoints = {}

    def fetch_spec(self):
        log.info(f"Downloading spec from {self.url}...")
        try:
            r = requests.get(self.url)
            if r.status_code == 200:
                self.spec_data = yaml.safe_load(r.text)
                log.info("Spec downloaded successfully.")
            else:
                raise Exception(f"Status code {r.status_code}")
        except Exception as e:
            log.error(f"Error fetching spec: {e}")

    def analyze_full_details(self):
        paths = self.spec_data.get('paths', {})
        for path, methods in paths.items():
            self.endpoints[path] = list(methods.keys())
        log.info(f"Analyzed {len(self.endpoints)} endpoints.")
        return self.endpoints