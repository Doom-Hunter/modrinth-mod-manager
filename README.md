# modrinth-mod-manager
A CLI mod manager built on top of Modrinth's API to manage mod files automatically

## About

Modrinth Mod Manager simplifies browsing, managing, and updating Minecraft mods sourced from the Modrinth API. It provides a clean terminal interface to keep your local mod folders organized without manually digging through browser downloads.

Built with Python, it manages and keep track of mods similar to a package manager

Designed for fast execution and minimal dependencies, making mod pack setup quick and straightforward.

## Installation

```bash
git clone [https://github.com/Doom-Hunter/modrinth-mod-manager.git](https://github.com/Doom-Hunter/modrinth-mod-manager.git)
```
Add an alias to your `~/.bashrc` (or `~/.zshrc`) to run it from anywhere:

```bash
echo alias modmanager="python3 /path/to/modrinth-mod-manager/main.py"
```
```ps1
Add-Content $PROFILE "`nfunction modmanager { python C:\path\to\modrinth-mod-manager\main.py `$args }"

```
## Installation Script
If you're not nerdy enough to figure out the setup, you can copy and run this script below and it'll set things up for you.

### mac/Linux (bash/zsh)
```bash
git clone [https://github.com/Doom-Hunter/modrinth-mod-manager.git](https://github.com/Doom-Hunter/modrinth-mod-manager.git)
cd modrinth-mod-manager
if [ -n "$ZSH_VERSION" ]; then CONF="$HOME/.zshrc"; else CONF="$HOME/.bashrc"; fi && echo "alias modmanager=\"python3 $(pwd)/main.py\"" >> "$CONF" && source "$CONF"
source "$CONF"
```

### Windows (powershell)
```ps1
git clone [https://github.com/Doom-Hunter/modrinth-mod-manager.git](https://github.com/Doom-Hunter/modrinth-mod-manager.git)
cd modrinth-mod-manager
if (!(Test-Path $PROFILE)) { New-Item -Type File -Path $PROFILE -Force }; Add-Content $PROFILE "`nfunction modmanager { python $((Get-Item .).FullName)\main.py `$args }"
. $PROFILE
```