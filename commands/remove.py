import downloader
from commands import command
from project import Project

@command("remove")
def remove(project: Project, args: list[str]):
    if len(args) < 1:
        print("Please provide the slug to the mod")
        return
    for slug in args:
        if slug not in project.configs.mods:
            print(f"Mod {slug} doesn't exists in the pack")
            return

        mod_info = project.configs.mods[slug]
        title = mod_info.title if mod_info is not None else slug
        if project.configs.mods.__contains__(slug):
            del project.configs.mods[slug]
        print(f"Mod [{title}] has been removed from the pack")
    project.save()