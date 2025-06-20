from plumbum import cli
from tool.blog.core.config_crud import ConfigCRUD


class PrintConfig(cli.Application):
    
    def main(self):
        config = ConfigCRUD.load()
        
        print("Targets:")
        for name, path in config.targets.items():
            print(f"  {name}: {path}")
        
        return 0