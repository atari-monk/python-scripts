from plumbum import cli


class BlogCLI(cli.Application):
    
    def main(self):
        if not self.nested_command:
            print("No command specified")
            self.help()
            return 1
        
        
def main():
    from tool.blog.blog_add_target import BlogAddTarget
    BlogCLI.subcommand("add")(BlogAddTarget)
    BlogCLI.run()


if __name__ == "__main__":
    main()