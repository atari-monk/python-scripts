from plumbum import cli
from tool.blog.blog_crud import BlogCRUD


class BlogAddTarget(cli.Application):
    
    def main(self, target_name: str = None, target_path: str = None):
        config = BlogCRUD.load()
        
        if target_name is None:
            while True:
                target_name = input("Enter target name: ").strip()
                if target_name:
                    break
                print("Error: Target name cannot be empty")
                
        if target_name in config.targets:
            print(f"Target '{target_name}' already exists")
            return 1
            
        if target_path is None:
            while True:
                target_path = input(f"Enter path for target '{target_name}': ").strip()
                if target_path:
                    break
                print("Error: Path cannot be empty")
                
        config.targets[target_name] = target_path
        config.last_used_target = target_name
        BlogCRUD.save(config)
        
        print(f"Added target '{target_name}' with path '{target_path}'")
        return 0
