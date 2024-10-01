import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import random
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class PhpUnitScanner:
    def __init__(self):
        self.base_url = "http://"
        self.endpoint_list_url = "https://raw.githubusercontent.com/rabeltester44/phpunitchecker/refs/heads/main/phpunit.txt"
        self.user_agents = self.load_user_agents("users_agents.txt")

    def load_user_agents(self, filename):
        try:
            with open(filename, 'r') as file:
                return [line.strip() for line in file.readlines() if line.strip()]
        except FileNotFoundError:
            logging.error(f"User agent file {filename} not found.")
            return []

    def save(self, save, name):
        with open(name, "a+") as result_file:
            result_file.write(f"{save}\n")

    def check_url(self, web):
        headers = {'User-Agent': random.choice(self.user_agents)} if self.user_agents else {}
        try:
            response = requests.head(web, headers=headers, allow_redirects=True, timeout=5)
            if response.status_code == 200:
                return web, True
        except requests.RequestException as e:
            logging.warning(f"Error checking URL {web}: {e}")
        return web, False

    def validate_path(self, web):
        try:
            response = requests.get(web, timeout=5)
            return response.status_code == 200
        except requests.RequestException as e:
            logging.warning(f"Validation failed for {web}: {e}")
            return False

    def mass_laravel(self, domain):
        full_url = self.base_url + domain

        try:
            response = requests.get(self.endpoint_list_url, timeout=5)
            response.raise_for_status()
            endpoints = response.text.splitlines()
        except requests.RequestException as e:
            logging.error(f"Failed to retrieve the list of endpoints: {e}")
            return

        endpoints = [endpoint for endpoint in endpoints if endpoint.strip()]

        with ThreadPoolExecutor(max_workers=10) as executor:  # Adjusted number of workers
            future_to_url = {executor.submit(self.check_url, full_url + endpoint.strip()): endpoint for endpoint in endpoints}
            for future in as_completed(future_to_url):
                endpoint = future_to_url[future]
                web = full_url + endpoint.strip()
                try:
                    url, found = future.result()
                    if found:
                        logging.info(f"[+] Found => {url}")
                        self.save(url, "phpunit.txt")
                        
                        if self.validate_path(url):
                            if "eval-stdin.php" in url:
                                logging.warning(f"[!] Accessing eval-stdin.php, might be blank!")
                        else:
                            logging.info(f"[-] Not Valid => {url}")
                    else:
                        logging.info(f"[-] Not Found => {web}")
                except Exception as e:
                    logging.error(f"Error checking {web}: {e}")

    def choose_option(self):
        print("\n\t<!> Scan Laravel Phpunit Coded By ./EcchiExploit <!>")
        print("\nNote: Don't Change http:// Or https://")
        print("1. Mass Scan Laravel Phpunit")
        print("2. Scan Laravel Phpunit No Mass")
        option = input("\nChoose Your 1/2 => ").strip()

        if option == '1':
            file_path = input("Your List site => ").strip()
            try:
                with open(file_path, 'r') as file:
                    domains = file.readlines()
                    for domain in domains:
                        self.mass_laravel(domain.strip())
            except FileNotFoundError:
                logging.error(f"File {file_path} not found.")
            except Exception as e:
                logging.error(f"Error reading file: {e}")

        elif option == '2':
            domain = input("Enter a single domain => ").strip()
            self.mass_laravel(domain)
        else:
            logging.error("Invalid option. Please choose 1 or 2.")

if __name__ == "__main__":
    scanner = PhpUnitScanner()
    scanner.choose_option()
