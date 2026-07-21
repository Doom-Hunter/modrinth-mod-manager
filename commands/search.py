import json
import search_api
from project import Project
from commands import command

@command("search")
def search_mods(project: Project, args: list[str]):
    amount = 10
    query = args[0] if len(args) > 0 else ""
    versions = args[1] if len(args) > 1 else ""
    page = 0
    try:
        if len(args) > 2:
            page = int(args[2])
    except ValueError:
        pass

    title = f"search: {query} | version: {versions if versions else "-"}"
    print("=" * len(title))
    print(title)
    print("-" * len(title))

    data = search_api.search(query, page * amount, amount, versions, project_type="mod")
    if not data:
        print("No search results were returned.")
        return

    hits = data.get("hits", [])
    if not hits:
        print(f"The search {query} returned no matching mods.")
        return

    title_width = max(len(item.get("title", "")) for item in hits)
    slug_width = max(len(item.get("slug", "")) for item in hits)

    for item in hits:
        slug = item.get("slug", "")
        title = item.get("title", "")
        has_slug = slug in project.configs.mods
        status = "x"
        if has_slug:
            downloaded = slug in project.configs.downloads
            if downloaded:
                status = "✓✓"
            else:
                status = "✓"
        print(f"{title}{(title_width - len(title)) * " "}\t[{status}]")
        print(f"{slug}{(slug_width - len(slug)) * " "}")
        print()