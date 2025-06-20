from plumbum import cli
from tool.blog.core.config_crud import ConfigCRUD
from tool.blog.core.cli import select_target_name_interactive

class DeleteTarget(cli.Application):
    
    def main(self, target_name: str = None):
        config = ConfigCRUD.load()
        
        try:
            if not target_name:
                target_name = select_target_name_interactive(config, "Select target to delete")
            
            if target_name not in config.targets:
                print(f"Target '{target_name}' doesn't exist")
                return 1
                
            del config.targets[target_name]
            ConfigCRUD.save(config)
            print(f"Removed target '{target_name}'")
            return 0
            
        except ValueError as e:
            print(str(e))
            return 1