import os
import sys
import json
import search_api
import commands
import project as pj
from project import Project, require_project

def search_mods(query: str, versions: str, page: int = 0):
    amount = 10
    data = search_api.search(query, page * amount, amount, versions, project_type="mod")
    if not data:
        return

    with open("raw_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    hits = data.get("hits", [])
    if not hits:
        return

    title_width = max(len(item.get("title", "")) for item in hits)
    slug_width = max(len(item.get("slug", "")) for item in hits)

    for item in hits:
        slug = item.get("slug", "")
        title = item.get("title", "")
        print(f"{title}{(title_width - len(title)) * " "}\t{slug}{(slug_width - len(slug)) * " "}\t[x]")

def main(args: list[str]):
        if len(args) < 1:
            print("Provide an action")
            return

        command = args.pop(0).lower()
        cwd = os.getcwd()

        if command == "init":
            init_path = args[1] if len(args) > 1 else cwd
            Project(init_path, init=True)

        else:
            commands.call(name=command, path=cwd, args=args)

if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        pass
    # finally:
    #     exit()