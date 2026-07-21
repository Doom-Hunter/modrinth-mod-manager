from commands import command
from project import require_project, Project

@command("version")
def version(project: Project, args: list[str]):
    if len(args) == 0:
        version = project.configs.version
        if version:
            print(f"Version: {version}")
        else:
            print(f"Version has not been set")
        return

    new_version = args[0]
    project.configs.version = new_version
    print(f"Version has been set to {new_version}")
    project.save()