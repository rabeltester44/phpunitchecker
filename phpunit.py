import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

class PhpUnitScanner:
    def __init__(self):
        self.base_url = "http://"
        self.endpoint_list_url = "https://raw.githubusercontent.com/rabeltester44/phpunitchecker/refs/heads/main/phpunit.txt"
        self.user_agents = self.load_user_agents("user_agent.txt")

    def load_user_agents(self, filename):
        try:
            with open(filename, 'r') as file:
                return [line.strip() for line in file.readlines() if line.strip()]
        except FileNotFoundError:
            print(f"User agent file {filename} not found.")
            return []

    def save(self, save, name):
        with open(name, "a+") as result_file:
            result_file.write(f"{save}\n")

    def check_url(self, web):
        headers = {'User-Agent': self.user_agents[0]} if self.user_agents else {}
        try:
            response = requests.head(web, headers=headers, allow_redirects=True, timeout=5)
            if response.status_code == 200:
                return web, True
        except requests.RequestException:
            return web, False
        return web, False

    def validate_path(self, web):
        try:
            response = requests.get(web, timeout=5)
            return response.status_code == 200
        except requests.RequestException:
            return False

    def mass_laravel(self, domain):
        full_url = self.base_url + domain

        try:
            response = requests.get(self.endpoint_list_url, timeout=5)
            response.raise_for_status()
            endpoints = response.text.splitlines()
        except requests.RequestException as e:
            print(f"Failed to retrieve the list of endpoints: {e}")
            return

        endpoints = [endpoint for endpoint in endpoints if endpoint.strip()]

        valid_path_found = False
        with ThreadPoolExecutor(max_workers=100) as executor:
            future_to_url = {executor.submit(self.check_url, full_url + endpoint.strip()): endpoint for endpoint in endpoints}
            for future in as_completed(future_to_url):
                if valid_path_found:
                    break
                endpoint = future_to_url[future]
                web = full_url + endpoint.strip()
                try:
                    url, found = future.result()
                    if found:
                        # Validate the path by making a GET request
                        if self.validate_path(url):
                            valid_path_found = True
                            print(f"\033[32m[+] Found => {url}\033[0m")
                            self.save(url, "phpunit.txt")
                        else:
                            print(f"\033[31m[-] Not Valid => {url}\033[0m")  # Mark as not valid
                    else:
                        print(f"\033[31m[-] Not Found => {web}\033[0m")
                except Exception as e:
                    print(f"Error checking {web}: {e}")

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
                print(f"File {file_path} not found.")
            except Exception as e:
                print(f"Error reading file: {e}")

        elif option == '2':
            domain = input("Enter a single domain => ").strip()
            self.mass_laravel(domain)
        else:
            print("Invalid option. Please choose 1 or 2.")

if __name__ == "__main__":
    scanner = PhpUnitScanner()
    scanner.choose_option()
