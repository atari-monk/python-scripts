from plumbum import cli
from tool.blog.core.config_crud import ConfigCRUD


class PrintConfig(cli.Application):
    
    def main(self):
        config = ConfigCRUD.load()
        
        print("Targets:")
        for name, path in config.targets.items():
            print(f"  {name}: {path}")
        
        if config.last_used_target:
            print(f"\nLast used target: {config.last_used_target}")
        else:
            print("\nNo last used target set")
            
        return 0