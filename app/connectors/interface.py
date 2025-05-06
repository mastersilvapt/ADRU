from abc import ABC, abstractmethod
from typing import Literal


class DNSUpdater(ABC):
    @abstractmethod
    def update_record(self,
                      zone_id: str,
                      record_id: str,
                      name: str,
                      record_type: Literal["A"]
                                   | Literal["AAAA"]
                                   | Literal["CAA"]
                                   | Literal["CERT"]
                                   | Literal["CNAME"]
                                   | Literal["DNSKEY"]
                                   | Literal["DS"]
                                   | Literal["HTTPS"]
                                   | Literal["LOC"]
                                   | Literal["MX"]
                                   | Literal["NAPTR"]
                                   | Literal["NS"]
                                   | Literal["OPENPGPKEY"]
                                   | Literal["PTR"]
                                   | Literal["SMIMEA"]
                                   | Literal["SRV"]
                                   | Literal["SSHFP"]
                                   | Literal["SVCB"]
                                   | Literal["TLSA"]
                                   | Literal["TXT"]
                                   | Literal["URI"],
                      value: str
                      ) -> bool:
        """
        Update a DNS record.
        
        Parameters:
            zone_id (str): The zone ID
            record_id (str): The record ID
            domain (str): The domain name (e.g., "www.example.com").
            record_type (str): The type of DNS record (e.g., "A", "CNAME").
            value (str): The new value for the DNS record (e.g., an IP address).
        
        Returns:
            bool: True if the update succeeded, False otherwise.
        """
        pass
