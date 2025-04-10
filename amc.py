#!/bin/env python3
from requests import get as req_get, exceptions as req_exceptions
from regex import compile as re_compile
from json import dump as json_dump
from concurrent.futures import ThreadPoolExecutor
from argparse import ArgumentParser as argparse_ArgumentParser


class Data():
    log_file = "log.json"                               # Output file
    worker_count: int = 10                              # Threads (amount) you want to use
    download_url = "https://archlinux.org/download/"    # Default download URL
    mirrors = []                                        # All Mirrors. I'll sort them by countries [next update]
    # done_mirrors[0] = Wroking (amount)
    # done_mirrors[1] = Not Working (amount)
    done_mirrors = [0, 0]                               # How many Mirrors Work / Not
    all_mirrors = len(mirrors)                          # How many Mirrors exist
    log_data = {}                                       # Json data to dump into log file

    request_timeout = 60                                # Request timeout, float || int
    check_amount = 0                                    # If 0 check all mirrors, else only first X

class RegEx():
    MIRROS = re_compile('<li>\s*<a href="(.*?)"\s*title="Download from .*">\s*(.*?)\s*</a>\s*</li>')
    CERT_ERROR = re_compile("certificate verify failed: (.*?) \(")

data = Data()
regex = RegEx()


def log(log_data: dict = {}, reset: bool = False) -> int:
    if reset:
        with open(data.log_file, 'w') as f:
            json_dump({}, f, indent=4)
        return 1
    with open(data.log_file, 'w') as f:
        json_dump(log_data, f, indent=4)
    return 1

def get_mirrors(url: str = data.download_url) -> list:
    req = req_get(url)
    if str(req.status_code)[0] != "2":
        print(f"Failed to get Mirros from {url}")
        return []
    return RegEx.MIRROS.findall(req.text)

def check_mirror(url: str, use_ssl: bool = True, domain_name: str = None) -> list[int|str, int, int]:
    try:
        req = req_get(url, verify=use_ssl, allow_redirects=True, timeout=data.request_timeout)
        if str(req.status_code)[0] == "2":
            return [1, round(req.elapsed.total_seconds() * 1000, 2), round(req.elapsed.total_seconds() * 1000000, 2)]
        elif str(req.status_code)[0] == "4":
            return [0, f"ERROR. Response Code: ({req.status_code})"]
        elif str(req.status_code)[0] == "5":
            return [0, f"ERROR. Server ERROR: {req.status_code}"]
        return [0, f"Either Not Supported Status Code, or error. Status Code: {req.status_code}"]
    except req_exceptions.Timeout:
        return [0, f"Timeout, took longer than {data.request_timeout} seconds"]
    except req_exceptions.ConnectionError as e:
        if "Failed to resolve" in str(e):
            payload = "Can't resolve domain"
        elif "No route to host" in str(e):
            payload = "No route to host"
        elif "Network is unreachable" in str(e):
            payload = "Network is unreachable"
        elif "certificate verify failed" in str(e):
            check = check_mirror(url, False)
            payload = f"SSL Certificate failed: {RegEx.CERT_ERROR.findall(str(e))[0]}"
            if check[0]:
                return check                
        else:
            payload = f"Uknown Error: {str(e)}"
        return [0, payload]
    except Exception as e:
        return [0, f"Uknown Error: {e}"]
    
def main() -> int:
    for mirror in data.mirrors:
        # mirror [0] = Mirror URL
        # mirror [1] = Mirror Domain Name

        if mirror[0] in data.log_data:
            continue

        data.log_data[mirror[0]] = {}
        log_instance = data.log_data[mirror[0]]
        log_instance["domain"] = mirror[1]
        log_instance["status"] = {}

        check = check_mirror(mirror[0], domain_name=mirror[1])
        if check[0]:
            data.done_mirrors[0] += 1
            log_instance["status"]["ms"] = check[1]
            log_instance["status"]["µs"] = check[2]
            log_instance["status"]["status"] = "✅"
            print(mirror[0] + " "*(70 - len(mirror[0])) + log_instance["status"]["status"] + " "
                  + str(log_instance["status"]["ms"]) + "ms / " + str(log_instance["status"]["µs"]) + "µs")
            percent_done = (data.done_mirrors[0] / (data.done_mirrors[0] + data.done_mirrors[1])) * 100
            total_percent = ((data.done_mirrors[0] + data.done_mirrors[1]) / data.all_mirrors) * 100
            print(f" [\033[31m{data.done_mirrors[1]}\033[0m / \033[32m{data.done_mirrors[0]}\033[0m "
                  f"({percent_done:.2f}%)/ {data.all_mirrors} / {total_percent:.2f}%]", end='\r')
            continue
        data.done_mirrors[1] += 1
        log_instance["status"]["error"] = check[1]
        log_instance["status"]["status"] = "❌"
        print(mirror[0] + " "*(70 - len(mirror[0])) + log_instance["status"]["status"] + " " + log_instance["status"]["error"])
        percent_done = (data.done_mirrors[0] / (data.done_mirrors[0] + data.done_mirrors[1])) * 100
        total_percent = ((data.done_mirrors[0] + data.done_mirrors[1]) / data.all_mirrors) * 100
        print(f" [\033[31m{data.done_mirrors[1]}\033[0m / \033[32m{data.done_mirrors[0]}\033[0m "
              f"({percent_done:.2f}%)/ {data.all_mirrors} / {total_percent:.2f}%]", end='\r')

    log(data.log_data)
    return 1


def init() -> int:
    parser = argparse_ArgumentParser(description="AMC | Arch Mirror Checker")
    parser.add_argument('--workers', '-w', type=int, help='thread amount', default=5)
    parser.add_argument('--timeout', '-t', type=float, help='Request timeout (seconds)', default=60)
    parser.add_argument('--max-check', '-c', type=int, help='Check only the first X Mirrors (0 = no limit)', default=0)
    parser.add_argument('--download-url', '-d', type=str, help=f'URL to get the Mirrors from ({data.download_url})')
    parser.add_argument('--ask-custom-url', '-a', help='Ask for a custom Download URL', action="store_true")
    parser.add_argument('--log-file', '-o', help='log output file', type=str, default="log.json")
    args = parser.parse_args()

    data.log_file = args.log_file
    data.worker_count = args.workers
    data.request_timeout = args.timeout
    data.check_amount = args.max_check
    if args.download_url:
        data.download_url = args.download_url
    
    mirror_url = data.download_url
    if args.ask_custom_url:
        mirror_url = input(f"Mirror URL: [{data.download_url}]\n# ") or data.download_url
    data.log_data['mirror_url'] = mirror_url
    data.mirrors = get_mirrors(mirror_url)
    if len(data.mirrors) == 0:
        print(f"Mirrors empty:\n{data.mirrors}")
    data.all_mirrors = len(data.mirrors)
    if data.check_amount and data.all_mirrors > data.check_amount:
        data.mirrors = data.mirrors[:data.check_amount]
        data.all_mirrors = len(data.mirrors)

    with ThreadPoolExecutor(max_workers=data.worker_count) as executor:
        for _ in range(data.worker_count):
            executor.submit(main)
    return 1


if __name__ == "__main__":
    log(reset=True)
    init()

    exit(1)
