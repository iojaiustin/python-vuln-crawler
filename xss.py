import requests
from pprint import pprint
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin

def get_all_forms(url):
    soup = bs(requests.get(url).content, "html.parser")
    return soup.find_all(["form"])

def get_form_details(form):
    details = {}
    action = form.attrs.get("action").lower()
    method = form.attrs.get("method", "get").lower()
    inputs = []
    for input_tag in form.find_all("input"):
        input_type = input_tag.attrs.get("type", "text")
        input_name = input_tag.attrs.get("name")
        inputs.append({"type": input_type, "name": input_name})
    details["action"] = action
    details["method"] = method
    details["inputs"] = inputs
    return details

def submit_form(form_details, url, payload):
    target_url = urljoin(url, form_details["action"])
    inputs = form_details["inputs"]
    data = {}
    for input in inputs:
        if input["type"] == "text" or input["type"] == "search":
            input["value"] = payload
        input_name = input.get("name")
        input_value = input.get("value")
        if input_name and input_value:
            data[input_name] = input_value

    if form_details["method"] == "post":
        return requests.post(target_url, data=data)
    else:
        return requests.get(target_url, params=data)

def scan(url,wordlist):
    vuln = False
    forms = get_all_forms(url)
    if len(forms):
        print(f"[+] Detected {len(forms)} forms on {url}.")
        print("[i] Starting the scan")
        for form in forms:
            for payload in wordlist:
                form_details = get_form_details(form)
                content = submit_form(form_details, url, payload).content.decode()
                if payload in content:
                    vuln = True
                    print(f"[!] XSS vulnerability detected at {url}")
                    print(f"[i] Form details:")
                    print(f"        Form name : {form_details['inputs'][0]['name']}")
                    print(f"        Payload used : {form_details['inputs'][0]['value']}")
                    print(f"        Form type : {form_details['inputs'][0]['type']}")
                    break
    return vuln