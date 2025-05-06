import os

from connectors.interface import DNSUpdater
import cloudflare

class CloudflareUpdater(DNSUpdater):

    def __init__(self, api_token = None):
        self.api_token = api_token or os.environ["API_TOKEN"]
        self.cf = cloudflare.Cloudflare(api_token=self.api_token)

    def update_record(self, zone_id, record_id, name, record_type, value) -> bool:
        res = self.cf.dns.records.update(dns_record_id=record_id,
                                   name=name,
                                   zone_id=zone_id,
                                   comment="",
                                   content=value,
                                   type=record_type)
        return res.content == value