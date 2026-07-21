from commands import command
from project import Project

@command("loader")
def loader(project: Project, args: list[str]):
    if len(args) == 0:
        loader = project.configs.loader
        if loader:
            print(f"Loader: {project.configs.loader}")
        else:
            print(f"Loader has not been set")
        return

    new_loader = args[0]
    project.configs.loader = new_loader
    print(f"Loader has been set to {new_loader}")
    project.save()