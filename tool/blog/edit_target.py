from plumbum import cli
from tool.blog.core.config_crud import ConfigCRUD
from tool.blog.core.cli import select_target_name_interactive, prompt_for_target_details


class EditTarget(cli.Application):
    
    def main(self, target_name: str = None, new_path: str = None):
        config = ConfigCRUD.load()
        
        if not config.targets:
            print("No targets configured. Use 'add-target' first.")
            return 1
            
        if not target_name:
            try:
                target_name = select_target_name_interactive(config, "Select target to edit")
            except ValueError as e:
                print(str(e))
                return 1
        
        if target_name not in config.targets:
            print(f"Target '{target_name}' doesn't exist")
            return 1
            
        if new_path:
            current_path = config.targets[target_name]
            config.targets[target_name] = new_path
        else:
            _, new_path = prompt_for_target_details(config, target_name)
            current_path = config.targets[target_name]
            config.targets[target_name] = new_path
        
        ConfigCRUD.save(config)
        print(f"Updated target '{target_name}'")
        print(f"Old path: {current_path}")
        print(f"New path: {new_path}")
        
        return 0