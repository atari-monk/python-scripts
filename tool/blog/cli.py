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
    from tool.blog.save_content import SaveContent
    from tool.blog.delete_target import DeleteTarget
    from tool.blog.edit_target import EditTarget
    from tool.blog.list_files import ListFiles
    from tool.blog.open_file import OpenFile
    from tool.blog.show_in_chrome import ShowInChrome
    from tool.blog.delete_file import DeleteFile

    BlogCLI.subcommand("add-target")(AddTarget)
    BlogCLI.subcommand("print-config")(PrintConfig)
    BlogCLI.subcommand("list-category")(ListCategory)
    BlogCLI.subcommand("save")(SaveContent)
    BlogCLI.subcommand("delete-target")(DeleteTarget)
    BlogCLI.subcommand("edit-target")(EditTarget)
    BlogCLI.subcommand("list-files")(ListFiles)
    BlogCLI.subcommand("open-file")(OpenFile)
    BlogCLI.subcommand("show-in-chrome")(ShowInChrome)
    BlogCLI.subcommand("delete-file")(DeleteFile)
    
    BlogCLI.run()


if __name__ == "__main__":
    main()