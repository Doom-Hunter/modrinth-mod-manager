import project
from commands import command

@command(name="where")
def where(path: str):
    root = project.find_project_root(path)
    if root:
        print(f"Your project root is at {root}")
    else:
        print("Project root not found.")