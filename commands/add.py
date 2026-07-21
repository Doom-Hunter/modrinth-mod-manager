import downloader
from commands import command
from project import Project, ModInfo

@command("add")
def add(project: Project, args: list[str]):
    if len(args) < 1:
        print("Please provide the slug(s) to the mod")
        return
    for slug in args:
        if project.configs.mods.__contains__(slug):
            print(f"Mod {slug} already exists in the pack")
            continue

        mod_info = downloader.fetch_info(slug)
        if mod_info is None:
            print(f"Mod {slug} not found on Modrinth")
            continue
        project.configs.mods[slug] = mod_info
        print(f"Mod [{mod_info.title}] has been added to the pack")
    project.save()