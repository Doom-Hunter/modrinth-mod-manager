import downloader
from commands import command
from project import Project, ModInfo

def sync_single(project: Project):
    total = len(project.configs.mods)
    synced = 0
    for slug in project.configs.mods:
        mod_info = downloader.fetch_info(slug)
        if mod_info is None:
            print(f"Mod {slug} not found on Modrinth")
            continue
        project.configs.mods[slug] = mod_info
        synced += 1
    print(f"{synced}/{total} mods has been synced")
    project.save()

@command("sync")
def sync(project: Project):
    slugs = [k for k in project.configs.mods.keys()]
    try:
        mod_infos = downloader.fetch_infos(slugs)
    except Exception as e:
        print(f"Unexpected error occured during info fetch: {e}")
        return

    for slug, mod_info in mod_infos.items():
        project.configs.mods[slug] = mod_info
    print(f"{len(project.configs.mods)} mods has been synced")
    project.save()