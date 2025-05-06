import os
import requests
import logging

from connectors.interface import DNSUpdater


class WixUpdater(DNSUpdater):
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("WIX_API_KEY")
        if not self.api_key:
            raise ValueError("WIX_API_KEY is required")
        self.base_url = "https://www.wixapis.com/domains/v1/dns-zones"

    def update_record(self, zone_id, record_id, name, record_type, new_value):
        url = f"{self.base_url}/{zone_id}"
        headers = {
            "Authorization": self.api_key,
            "Content-Type": "application/json"
        }

        payload = {
            "additions": [{
                "type": record_type,
                "hostName": name,
                "values": new_value,
                "ttl": 3600
            }],
            "deletions": [
                {
                    "type": record_type,
                    "hostName": name
                }
            ],
            "domainName": zone_id,
        }

        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 200:
            logging.info(f"Successfully updated {record_type} record for {name}.{zone_id}")
            return True
        else:
            logging.error(f"Failed to update DNS record: {response.status_code} - {response.text}")
            return False
