from dataclasses import asdict
from pathlib import Path
import json
from tool.blog.core.config import Config


class ConfigCRUD:
    @staticmethod
    def get_config_path() -> Path:
        return Path(r"C:\atari-monk\code\apps-data-store\blog_config.json")

    @classmethod
    def load(cls) -> Config:
        config_path = cls.get_config_path()
        try:
            if config_path.exists() and config_path.stat().st_size > 0:
                with open(config_path, "r") as f:
                    data = json.load(f)
                    if "targets" in data:
                        return Config(
                            targets=data["targets"],
                            last_used_target=data.get("last_used_target")
                        )
                    elif "repos" in data:
                        return Config(targets=data["repos"])
                    else:
                        return Config(targets={"blog": data.get("repo_path", "")})
        except (json.JSONDecodeError, AttributeError):
            print("Warning: Config file corrupted, creating new one")
        return Config()

    @classmethod
    def save(cls, config: Config) -> None:
        with open(cls.get_config_path(), "w") as f:
            json.dump(asdict(config), f, indent=2)