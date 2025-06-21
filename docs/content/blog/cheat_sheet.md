## Cheat Sheet

Here's a cheat sheet for the blog management tool:

### Basic Configuration Commands
1. **Add a new target**  
   `blog add-target [target_name] [target_path]`  
   (Interactive if no args provided)

2. **Edit an existing target**  
   `blog edit-target [target_name] [new_path]`  
   (Interactive if no args provided)

3. **Delete a target**  
   `blog delete-target [target_name]`  
   (Interactive if no name provided)

4. **View current configuration**  
   `blog print-config`

### File Management Commands
5. **List all categories**  
   `blog list-category [target_name]`  
   Options:  
   `-s/--search` - Filter categories by search term

6. **List all markdown files**  
   `blog list-files [target_name]`  
   Options:  
   `-c/--category` - Filter by specific category  
   `-s/--search` - Filter by filename search term  
   `-v/--verbose` - Debugging output

7. **Open a markdown file**  
   `blog open-file [target_name] [filename]`  
   Options:  
   `-c/--category` - Specify category path  
   `-e/--editor` - Use specific editor command

### Content Management Commands
8. **Save content to a file**  
   `blog save [target_name]`  
   Options:  
   `-c/--category` - Set category path  
   `-f/--file` - Set filename (without extension)  
   (Interactive mode appends clipboard content)

### Usage Tips
- Most commands support interactive mode if arguments are omitted
- Paths can use either forward or backward slashes
- When specifying filenames, the `.md` extension is optional
- The tool automatically creates necessary directories
- Content is automatically cleaned and formatted when saving

### Examples
```bash
# Add a new blog target
blog add-target my_blog C:/my/blog/path

# List files in a specific category
blog list-files -c tech/python

# Open a file in VS Code
blog open-file -e code my_file

# Save clipboard content to a new file
blog save -c recipes -f chocolate_cake
```