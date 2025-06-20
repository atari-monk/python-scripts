from plumbum import cli
from tool.blog.core.config_crud import ConfigCRUD
from tool.blog.core.cli import prompt_for_target_details


class AddTarget(cli.Application):
    
    def main(self, target_name: str = None, target_path: str = None):
        config = ConfigCRUD.load()
        
        if target_name and target_path:
            if target_name in config.targets:
                print(f"Target '{target_name}' already exists")
                return 1
        else:
            target_name, target_path = prompt_for_target_details(config)
            
        config.targets[target_name] = target_path
        ConfigCRUD.save(config)
        
        print(f"Added target '{target_name}' with path '{target_path}'")
        return 0