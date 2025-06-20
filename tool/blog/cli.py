from plumbum import cli


class BlogCLI(cli.Application):
    
    def main(self):
        if not self.nested_command:
            print("No command specified")
            self.help()
            return 1
        
        
def main():
    from tool.blog.add_target import AddTarget
    from tool.blog.print_config import PrintConfig
    from tool.blog.list_category import ListCategory

    BlogCLI.subcommand("add-target")(AddTarget)
    BlogCLI.subcommand("print-config")(PrintConfig)
    BlogCLI.subcommand("list-category")(ListCategory)
    BlogCLI.run()


if __name__ == "__main__":
    main()