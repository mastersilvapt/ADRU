
from connectors.cloudflare import CloudflareUpdater

def main():
    updater = CloudflareUpdater(api_token="your_token_here")
    success = updater.update_record("example.com", "A", "www", "192.0.2.1")
    
    if success:
        print("DNS record updated successfully.")
    else:
        print("Failed to update DNS record.")


if __name__ == "__main__":
    main()

