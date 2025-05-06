
from connectors.interface import DNSUpdater
import cloudflare

class CloudflareUpdater(DNSUpdater):

    cf = None

    def __init__(self):
        self.cf = cloudflare.Cloudflare()

    def update_record(self, zone_id, record_id, name, record_type, value) -> bool:
        res = self.cf.dns.records.update(dns_record_id=record_id,
                                   name=name,
                                   zone_id=zone_id,
                                   comment="",
                                   content=value,
                                   type=record_type)
        return res.content == value