from plumbum import cli


class BlogCLI(cli.Application):
    
    def main(self):
        if not self.nested_command:
            print("No command specified")
            self.help()
            return 1
        
        
def main():
    BlogCLI.run()


if __name__ == "__main__":
    main()