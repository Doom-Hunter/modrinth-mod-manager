import json
import urllib.request

def add_headers(request: urllib.request.Request):
    request.add_header("User-Agent", "my_custom_sandbox_scraper/1.0")
    request.add_header("Accept", "application/json")