import os
import sys
import json
import inspect
import configs
from functools import wraps
from dataclasses import dataclass, field, asdict, fields
from typing import Callable, Any, Optional

class ProjectError(Exception):
    """Base exception for all modloader project-related issues."""
    pass

class ConfigCorruptedError(ProjectError):
    """Raised when the project configuration file is missing, empty, or invalid."""
    pass

@dataclass
class DownloadInfo:
    filename: str
    sha512: str

    @classmethod
    def from_dict(cls, data: dict):
        try:
            return cls(
                filename=data["filename"],
                sha512=data["sha512"],
            )
        except KeyError:
            return None

@dataclass
class ModInfo:
    title: str
    description: str

    @classmethod
    def from_dict(cls, data: dict):
        try:
            return cls(
                title=data["title"],
                description=data["description"],
            )
        except KeyError:
            return None

@dataclass
class Configs:
    loader: str | None = None
    version: str | None = None
    mods: dict[str, ModInfo] = field(default_factory=dict)
    downloads: dict[str, DownloadInfo] = field(default_factory=dict)

    def to_dict(self) -> dict:
        """Converts the dataclass to a JSON-safe dictionary."""
        return asdict(self)

class Project:
    def __init__(self, root_path: str, init: bool = False) -> None:
        self.root_path: str = root_path
        self.project_path: str = os.path.join(self.root_path, configs.PROJECT_DIR_NAME)
        self.config_path: str = os.path.join(self.project_path, configs.CONFIG_FILE_NAME)
        self.configs: Configs = Configs()

        if init:
            self._init()
        else:
            self.configs = self._load()

    def _load(self) -> Configs:
        if os.path.exists(self.config_path):
            with open(self.config_path, "r") as f:
                contents = f.read().strip()
                try:
                    if contents:
                        raw_pj_configs: dict = json.loads(contents)
                        raw_mods: dict[str, dict] = raw_pj_configs.get("mods", {})
                        raw_downloads: dict[str, dict] = raw_pj_configs.get("downloads", {})
                        mods = {
                            key: mod
                            for key, raw_mod_infos in raw_mods.items()
                            if (mod := ModInfo.from_dict(raw_mod_infos)) is not None
                        }
                        downloads = {
                            key: download
                            for key, raw_mod_infos in raw_downloads.items()
                            if (download := DownloadInfo.from_dict(raw_mod_infos)) is not None
                        }

                        return Configs(
                            loader=raw_pj_configs.get("loader"),
                            version=raw_pj_configs.get("version"),
                            mods=mods,
                            downloads=downloads,
                        )
                except json.JSONDecodeError as e:
                    raise ConfigCorruptedError(f"Config file at {self.config_path} is not valid JSON.") from e

        # Also raise this if the file doesn't exist or is completely empty
        raise ConfigCorruptedError(f"Config file at {self.config_path} is missing or empty.")

    def _setup(self):
        os.makedirs(self.project_path, exist_ok=True)
        self.save()
        self.configs = self._load()
        self.save()

    def _init(self):
        try:
            is_reinit = os.path.exists(self.project_path)
            self._setup()
            if is_reinit:
                print(f"Reinitialized project in {self.root_path}.")
            else:
                print(f"Initialized empty project in {self.root_path}.")
        except PermissionError:
            print(f"Error: Cannot initialize. Path {self.root_path} is blocked or inaccessible.")
        except NotADirectoryError:
            print(f"Error: Cannot initialize. Path {self.root_path} is a file.")
        except Exception as e:
            print(f"Error: Unexpected issue initializing environment: {e}")

    def save(self):
        with open(self.config_path, "w") as f:
            json.dump(self.configs.to_dict(), f, indent=4)

def find_project_root(path: str):
    while True:
        potential_repo = os.path.join(path, configs.PROJECT_DIR_NAME)
        if os.path.isdir(potential_repo):
            return path

        parent_dir = os.path.dirname(path)
        if parent_dir == path:
            break
        path = parent_dir

    return None

def require_project(func: Callable[..., Any]) -> Callable[..., Any]:
    # Find out the name of the project parameter slot (e.g., 'project')
    sig = inspect.signature(func)
    param_name = None
    for name, param in sig.parameters.items():
        if param.annotation == Project:
            param_name = name
            break

    if not param_name:
        raise TypeError(f"Function '{func.__name__}' wrapped with @require_project must have a parameter annotated with 'Project'.")

    @wraps(func)
    def wrapper(*args: Any, path: str, **kwargs: Any) -> Any:
        root = find_project_root(path)
        if not root:
            print(f"Error: Path '{path}' is not part of a modloader project.", file=sys.stderr)
            sys.exit(1)
        try:
            project_obj = Project(root)
        except ConfigCorruptedError as e:
            print(f"CRITICAL: Config file contains corrupted JSON.", file=sys.stderr)
            print(f"Details: {e}", file=sys.stderr)
            sys.exit(1)

        kwargs[param_name] = project_obj
        return func(*args, **kwargs)
    return wrapper