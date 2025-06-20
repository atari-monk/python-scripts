from plumbum import cli
from tool.blog.core.config_crud import ConfigCRUD

class DeleteTarget(cli.Application):
    """Remove a target from the configuration"""
    
    def main(self, target_name: str = None):
        config = ConfigCRUD.load()
        
        if not config.targets:
            print("No targets configured")
            return 1
            
        if target_name:
            if target_name not in config.targets:
                print(f"Target '{target_name}' doesn't exist")
                return 1
        else:
            print("Available targets:")
            for i, (name, path) in enumerate(config.targets.items(), 1):
                print(f"{i}. {name}: {path}")
            
            while True:
                choice = input("\nEnter target number to delete (1-{}): ".format(
                    len(config.targets))).strip()
                
                try:
                    choice_num = int(choice)
                    if 1 <= choice_num <= len(config.targets):
                        target_name = list(config.targets.keys())[choice_num-1]
                        break
                except ValueError:
                    pass
                print("Invalid selection")
        
        del config.targets[target_name]
        ConfigCRUD.save(config)
        print(f"Removed target '{target_name}'")
        return 0