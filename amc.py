#!/bin/python3.13
from requests import get as req_get, exceptions as req_exceptions
from regex import compile as re_compile
from json import dump as json_dump
from threading import Thread


class Data():
    thread_count: int = 5
    threads = []
    DOWNLOAD_URL = "https://archlinux.org/download/"
    mirrors = []
    # done_mirrors[0] = Wroking (amount)
    # done_mirrors[1] = Not Working (amount)
    done_mirrors = [0, 0]
    all_mirrors = len(mirrors)
    log_data = {}

class RegEx():
    MIRROS = re_compile('<li>\s*<a href="(.*?)"\s*title="Download from .*">\s*(.*?)\s*</a>\s*</li>')
    CERT_ERROR = re_compile("certificate verify failed: (.*?) \(")

data = Data()
regex = RegEx()


def log(data: dict = {}, reset: bool = False) -> int:
    if reset:
        with open("log.json", 'w') as f:
            json_dump({}, f, indent=4)
        return 1
    with open("log.json", 'w') as f:
        json_dump(data, f, indent=4)
    return 1

def get_mirrors(url: str = data.DOWNLOAD_URL) -> list:
    req = req_get(url)
    if str(req.status_code)[0] != "2":
        print(f"Failed to get Mirros from {url}")
        return []
    return RegEx.MIRROS.findall(req.text)

def check_mirror(url: str, use_ssl: bool = True, domain_name: str = None) -> list[int|str, int, int]:
    try:
        req = req_get(url, verify=use_ssl, allow_redirects=True, timeout=60)
        if str(req.status_code)[0] == "2":
            return [1, round(req.elapsed.total_seconds() * 1000, 2), round(req.elapsed.total_seconds() * 1000000, 2)]
        elif str(req.status_code)[0] == "4":
            return [0, f"ERROR. Response Code: ({req.status_code})"]
        elif str(req.status_code)[0] == "5":
            return [0, f"ERROR. Server ERROR: {req.status_code}"]
        return [0, f"Either Not Supported Status Code, or error. Status Code: {req.status_code}"]
    except req_exceptions.Timeout:
        return [0, "Timeout, took longer than 60 seconds"]
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
    
def main(mirrors: list) -> int:
    for mirror in mirrors:
        # mirror [0] = Mirror URL
        # mirror [1] = Mirror Domain Name
        if mirror[0] in data.log_data:
            if data.done_mirrors[0] > 0 and data.done_mirrors[1] > 0:
                print(f" [\033[31m{data.done_mirrors[1]}\033[0m / \033[32m{data.done_mirrors[0]}\033[0m ({((data.done_mirrors[0] / (data.done_mirrors[0]+data.done_mirrors[1])) * 100):.2f}%)/ {data.all_mirrors} / {((data.done_mirrors[0]+data.done_mirrors[1]*100)/data.all_mirrors):.2f}%]",end='\r')
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
            print(mirror[0] + " "*(70 - len(mirror[0])) + log_instance["status"]["status"] + " " + str(log_instance["status"]["ms"]) + "ms / " + str(log_instance["status"]["µs"]) + "µs")
            print(f" [\033[31m{data.done_mirrors[1]}\033[0m / \033[32m{data.done_mirrors[0]}\033[0m ({((data.done_mirrors[0] / (data.done_mirrors[0]+data.done_mirrors[1])) * 100):.2f}%)/ {data.all_mirrors} / {((data.done_mirrors[0]+data.done_mirrors[1]*100)/data.all_mirrors):.2f}%]",end='\r')
            continue
        data.done_mirrors[1] += 1
        log_instance["status"]["error"] = check[1]
        log_instance["status"]["status"] = "❌"
        print(mirror[0] + " "*(70 - len(mirror[0])) + log_instance["status"]["status"] + " " + log_instance["status"]["error"])
        print(f" [\033[31m{data.done_mirrors[1]}\033[0m / \033[32m{data.done_mirrors[0]}\033[0m ({((data.done_mirrors[0] / (data.done_mirrors[0]+data.done_mirrors[1])) * 100):.2f}%)/ {data.all_mirrors} / {((data.done_mirrors[0]+data.done_mirrors[1]*100)/data.all_mirrors):.2f}%]",end='\r')
    log(data.log_data)
    return 1

def init() -> int:
    mirror_url = input(f"Mirror URL: [{data.DOWNLOAD_URL}]\n# ") or data.DOWNLOAD_URL
    data.log_data['mirror_url'] = mirror_url
    mirrors = get_mirrors(mirror_url)
    if len(mirrors) == 0:
        print(f"Mirrors empty:\n{mirrors}")
    data.all_mirrors = len(mirrors)
    for _ in range(data.thread_count):
        t = Thread(target=main, args=(mirrors, ))
        data.threads.append(t)
        t.start()
    return 1


if __name__ == "__main__":
    log(reset=True)
    init()
    
    for t in data.threads:
        t.join()
    exit(1)
