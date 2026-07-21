import os
import downloader
from commands import command
from project import Project, DownloadInfo

@command("download")
def download(project: Project, args: list[str]):
    mods_dir = os.path.join(project.root_path, "mods")
    loader = project.configs.loader
    version = project.configs.version

    if loader is None:
        print("You haven't set the loader")
        return

    if version is None:
        print("You haven't set the version")
        return

    os.makedirs(os.path.join(project.root_path, "mods"), exist_ok=True)

    mods_to_download = project.configs.mods
    if args:
        args = [a.lower() for a in args]
        for slug in args.copy():
            if slug not in project.configs.mods.keys():
                args.remove(slug)
                print(f"Mod {slug} not found in the config")

        mods_to_download = {
            k: v
            for k, v in project.configs.mods.items() if k in args
        }

    if not mods_to_download:
        return

    print("Fetching versions...", end="")
    download_options: dict[str, list[downloader.DownloadOption]] = {}
    for slug, mod_info in mods_to_download.items():
        download_options[slug] = downloader.fetch_versions(slug, [version], [loader])
    print(f"\r{len(download_options)} version(s) found")

    print("Choosing files...", end="")
    download_files: dict[str, downloader.DownloadFile] = {}
    for slug, mod_info in mods_to_download.items():
        if (file := downloader.choose_file(download_options[slug], loader, version)):
            download_files[slug] = file
        else:
            print(f"No matching version for {mod_info.title} found")
    print(f"\r{len(download_files)} files(s) found")

    for slug, download_file in download_files.items():
        download_info = project.configs.downloads.get(slug)

        mod_info = mods_to_download[slug]

        if download_info and download_info.sha512 == download_file.sha512:
            print(f"Mod [{mod_info.title}] is up to date")
            continue

        try:
            download_info = downloader.download(mods_dir, download_file, loader, version)
            if download_info:
                project.configs.downloads[slug] = download_info
                print(f"Mod [{mod_info.title}] has been downloaded successfully")
            else:
                print(f"Unable to download mod [{mod_info.title}]")
        except Exception as e:
            print(f"Failed to fetch data for slug '{slug}': {e}")

    project.save()
