import configs
import json
import urllib.error
import urllib.parse
import api_endpoint
import urllib.request

def search(query: str, offset: int = 0, limit: int = 10, versions: str | None = None, loaders: str | None = None, project_type: str | None = None) -> dict | None:
    params = {
        "query": query,
        "offset": offset,
        "limit": limit,
    }

    facets_data = []
    if versions:     facets_data.append([f"versions:{versions}"])
    if loaders:      facets_data.append([f"loaders:{loaders}"])
    if project_type: facets_data.append([f"project_type:{project_type}"])

    if facets_data:
        params["facets"] = json.dumps(facets_data)

    query_string = urllib.parse.urlencode(params)
    full_url = f"{configs.SEARCH_URL}?{query_string}"

    request = urllib.request.Request(full_url)
    api_endpoint.add_headers(request)

    try:
        with urllib.request.urlopen(request) as response:
            # Check the HTTP status code before processing
            if response.status != 200:
                print(f"Server returned HTTP Status: {response.status}")
                return None

            raw_data = response.read().decode("utf-8").strip()

            if not raw_data:
                print("Received empty payload.")
                return None
            if not raw_data.startswith(("{", "[")):
                print(f"Received malformed non-JSON string payload")
                with open("raw_data.html", "w", encoding="utf-8") as f:
                    f.write(raw_data)
                return None
            else:
                return json.loads(raw_data)

    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: {e.reason}")
        print(e.read().decode("utf-8"))
        return None
    except Exception as e:
        print(f"Unexpected connectivity error: {e}")
        return None
