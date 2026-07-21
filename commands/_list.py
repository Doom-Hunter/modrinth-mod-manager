import rendering
from commands import command
from project import Project

@command("list")
def list_mods(project: Project, args: list[str]):
    display_mode = ''
    try:
        i = args.index("-m")
        args.pop(i)
        if i == len(args):
            print("Invalid mode")
            return
        display_mode = args.pop(i)

    except ValueError:
        pass

    query = ""
    if len(args) > 0:
        query = args[0].lower()

    modlist: list[list[str]] = []
    for slug, info in project.configs.mods.items():
        if query:
            in_slug = query in slug.lower()
            in_title = info and (query in info.title.lower())

            if not in_slug and not in_title:
                continue

        if info:
            is_downloaded = slug in project.configs.downloads
            modlist.append([(slug if display_mode == 'slug' else info.title), f"[{'✓' if is_downloaded else 'x'}]"])
            # modlist.append([info.description])
        else:
            modlist.append([f"{slug} - missing info"])

    w = 50
    version = v if (v := project.configs.version) else '-'
    loader = l if (l := project.configs.loader) else '-'
    print("="*w)
    print(f"Your Mods | version: {version} | loader: {loader}")
    print("-"*w)
    print()
    rendering.print_table(modlist, '\t\t')
    print()
    print("="*w)