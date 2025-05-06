import argparse
import os
import logging
from time import sleep

from dotenv import load_dotenv

# Import all updaters
from connectors.cloudflare import CloudflareUpdater
from connectors.wix import WixUpdater
# from connectors.google import GoogleUpdater

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("/var/log/updater.log"),
        logging.StreamHandler()
    ]
)

UPDATERS = {
    "cloudflare": CloudflareUpdater,
    "wix": WixUpdater,
    # "google": GoogleUpdater,
}

def get_ip(file="/tmp/latest_ip"):
    import requests
    if os.path.exists(file):
        with open(file, "r") as f:
            ip = f.readline().strip()
    else:
        ip = None

    try:
        new_ip = requests.get("https://ifconfig.me/ip", timeout=5).text.strip()
    except Exception as e:
        logging.error(f"Failed to fetch external IP: {e}")
        return False, None

    if ip != new_ip:
        with open(file, "w") as f:
            f.write(new_ip)
        return True, new_ip

    return False, None


def main():
    load_dotenv()

    parser = argparse.ArgumentParser(description="DNS Updater Tool")
    parser.add_argument('--cronjob')
    subparsers = parser.add_subparsers(dest="provider", help="DNS provider to use")

    # Subparser for Cloudflare
    cf_parser = subparsers.add_parser("cloudflare", help="Use Cloudflare as DNS provider")
    cf_parser.add_argument('--zone-id')
    cf_parser.add_argument('--record-id')
    cf_parser.add_argument('--name')
    cf_parser.add_argument('--type')

    # Add subparsers for other providers as needed
    wix_parser = subparsers.add_parser("wix", help="Use Wix as DNS provider")
    wix_parser.add_argument('--domain')
    wix_parser.add_argument('--name')
    wix_parser.add_argument('--type')

    # google_parser = subparsers.add_parser("google", help="Use Google as DNS provider")

    args = parser.parse_args()

    if not args.provider and not os.environ["PROVIDER"]:
        parser.print_help()
        exit(1)

    updater_class = UPDATERS.get(args.provider or os.environ['PROVIDER'])
    if not updater_class:
        logging.error(f"No updater found for provider '{args.provider}'")
        exit(1)

    # Load arguments (with .env fallback)
    zone_id = getattr(args, "zone_id", None) or os.getenv("ZONE_ID")
    record_id = getattr(args, "record_id", None) or os.getenv("DNS_RECORD_ID")
    name = getattr(args, "name", None) or os.getenv("DNS_RECORD_NAME")
    record_type = getattr(args, "type", None) or os.getenv("DNS_RECORD_TYPE")

    missing = [k for k, v in {
        "zone-id": zone_id,
        "record-id": record_id,
        "name": name,
        "type": record_type,
    }.items() if v is None]

    if missing:
        logging.error(f"Missing required parameters: {', '.join(missing)}")
        exit(1)

    updater = updater_class()

    is_cronjob = getattr(args, "cronjob", False)

    timeout = int(os.environ.__contains__("TIMEOUT") and os.environ["TIMEOUT"]) or 3600

    while True:
        changed, value = get_ip()
        if changed:
            success = updater.update_record(zone_id, record_id, name, record_type, value)
            if success:
                logging.info(f"DNS record updated. New IP: {value}")
            else:
                logging.error(f"Failed to update DNS record. New IP: {value}")
        else:
            logging.info("No IP change. Skipping update.")
        if is_cronjob :
            break
        sleep(timeout)


if __name__ == "__main__":
    main()