import os
import sys
import json
import configs
import api_endpoint
import urllib.error
import urllib.parse
import urllib.request
from project import ModInfo, DownloadInfo
from dataclasses import dataclass, field

@dataclass
class DownloadFile:
    primary: bool
    filename: str
    url: str
    sha512: str

@dataclass
class DownloadOption:
    game_versions: list[str]
    loaders: list[str]
    files: list[DownloadFile]

def fetch_info(slug: str) -> ModInfo | None:
    url = f"{configs.PROJECT_BASE_URL}/{slug}"
    req = urllib.request.Request(url)
    api_endpoint.add_headers(req)

    try:
        with urllib.request.urlopen(req) as response:
            raw_info = json.loads(response.read().decode())
            return ModInfo(
                title=raw_info["title"],
                description=raw_info["description"],
            )
    except KeyError:
        return None
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        else:
            raise

def fetch_infos(slugs: list[str]) -> dict[str, ModInfo]:
    slugs_json = json.dumps(slugs)
    slugs_url = urllib.parse.quote(slugs_json)
    url = f"{configs.PROJECTS_BASE_URL}?ids={slugs_url}"
    req = urllib.request.Request(url)
    api_endpoint.add_headers(req)

    mod_infos: dict[str, ModInfo] = {}
    try:
        with urllib.request.urlopen(req) as response:
            raw_info: list[dict] = json.loads(response.read().decode())
            for i, raw_mod in enumerate(raw_info):
                mod_infos[slugs[i]] = ModInfo(
                    title=raw_mod["title"],
                    description=raw_mod["description"],
                )
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return {}
        else:
            raise
    return mod_infos

def fetch_versions(slug: str, game_versions: list[str], loaders: list[str]) -> list[DownloadOption]:
    params: dict[str, str] = {}
    if game_versions:
        params["game_versions"] = urllib.parse.quote(json.dumps(game_versions))
    if loaders:
        params["loaders"] = urllib.parse.quote(json.dumps(loaders))
    url = f"{configs.PROJECT_BASE_URL}/{slug}/version"
    if params:
        url += "?" + '&'.join(f"{k}={v}" for k, v in params.items())
    req = urllib.request.Request(url)
    api_endpoint.add_headers(req)

    try:
        with urllib.request.urlopen(req) as response:
            raw_version_data = json.loads(response.read().decode())

    except urllib.error.HTTPError as e:
        if e.code == 404:
            return []
        else:
            raise

    download_infos: list[DownloadOption] = []
    for version in raw_version_data:
        files = version.get("files", [])
        download_infos.append(DownloadOption(
            game_versions=version.get("game_versions", []),
            loaders=version.get("loaders", []),
            files=[
                DownloadFile(
                    primary=f.get("primary", False),
                    filename=f.get("filename", ''),
                    url=f.get("url", ''),
                    sha512=f.get("hashes", {}).get("sha512", ''),
                )
                for f in files
            ],
        ))
        # if files:
        #     primary = next((f for f in files if f.get("primary")), files[0])
    return download_infos

def fetch_multiple_download_options(ids: list[str]) -> dict[str, list[DownloadOption]]:
    ids_json = json.dumps(ids)
    ids_url = urllib.parse.quote(ids_json)
    url = f"{configs.VERSIONS_BASE_URL}?ids={ids_url}"
    print(url)
    req = urllib.request.Request(url)
    api_endpoint.add_headers(req)

    try:
        with urllib.request.urlopen(req) as response:
            raw_version_data = json.loads(response.read().decode())

    except urllib.error.HTTPError as e:
        if e.code == 404:
            return {}
        else:
            raise

    all_download_options: dict[str, list[DownloadOption]] = {}
    for i, raw_mods in enumerate(raw_version_data):
        download_options = []
        for version in raw_mods:
            files = version.get("files", [])
            download_options.append(DownloadOption(
                game_versions=version.get("game_versions", []),
                loaders=version.get("loaders", []),
                files=[
                    DownloadFile(
                        primary=f.get("primary", False),
                        filename=f.get("filename", ''),
                        url=f.get("url", ''),
                        sha512=f.get("hashes", {}).get("sha512", ''),
                    )
                    for f in files
                ],
            ))
        all_download_options[ids[i]] = download_options
        # if files:
        #     primary = next((f for f in files if f.get("primary")), files[0])
    return all_download_options

def choose_file(download_options: list[DownloadOption], loader: str, game_version: str)-> DownloadFile | None:
    for version in download_options:
        if game_version not in version.game_versions and loader not in version.loaders:
            continue

        # Grab the primary file array
        files = version.files
        if files:
            # Find the primary file, or fallback to the first entry
            return next((f for f in files if f.primary), files[0])

def download(output_dir: str, download_file: DownloadFile, loader: str, game_version: str)-> DownloadInfo:
    dest_path = os.path.join(output_dir, download_file.filename)
    urllib.request.urlretrieve(download_file.url, dest_path)
    return DownloadInfo(
        filename=download_file.filename,
        sha512=download_file.sha512
    )
