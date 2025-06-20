# Blog Script

## Prompt

Here's a detailed prompt you could use to generate this exact script (which we've now iteratively developed together):

---

**Python Script Generation Prompt:**

I need a Python script for managing blog content with the following features:

1. **Configuration Management**:
   - Uses a JSON config file stored at `C:\atari-monk\code\apps-data-store\blog_config.json`
   - Stores multiple repository paths (at minimum 'blog' and 'dev-blog')
   - Uses dataclass `BlogConfig` with dictionary of repositories
   - Handles config file creation, corruption, and migration from old format

2. **Command Line Interface**:
   - Uses `argparse` with these arguments:
     * `-r/--repo`: Specify repository name
     * `-c/--category`: Specify category path (e.g. 'tech/python')
     * `-f/--file`: Specify filename (without .md)
     * `--list`: List configured repositories
     * `-h`: Show help
   - Falls back to interactive prompts for missing arguments

3. **Core Functionality**:
   - Creates nested category folders as needed
   - Takes content from clipboard
   - Saves as markdown file with UTF-8 encoding
   - Provides clear success/error messages

4. **Quality Requirements**:
   - Strict typing (type hints)
   - No comments in code
   - Path handling works cross-platform
   - Robust error handling (config file, directories, etc.)
   - Clean, minimalist code style

5. **Example Use Cases**:
   ```bash
   # Interactive mode
   blog
   # Command-line mode
   blog -r dev-blog -c programming/python -f new-tutorial
   # List repositories
   blog --list
   ```

6. **Behavior**:
   - First run should help configure repositories
   - Subsequent runs should remember paths
   - Should handle special characters in paths/content
   - Should create parent directories as needed

The script should prioritize:
1. Reliability (handle edge cases)
2. Clean implementation
3. Good user experience (clear prompts/messages)
4. Maintainability (typed, but no comments)

---

This prompt captures all the requirements we've iteratively developed, including:
- The config file location
- Multiple repository support
- Both CLI and interactive modes
- Type safety
- Robust error handling
- Clean code style

The prompt is detailed enough to regenerate this exact solution while being clear about requirements and priorities.

## Usage Instructions

Here are clear **Usage Instructions** for your blog management script:

---

### **Basic Commands**

#### **1. Interactive Mode (Guided)**
```bash
blog
```
- Guides you through each step with prompts
- Shows repository selection menu
- Asks for category and filename
- Waits for clipboard content

#### **2. Quick Save with CLI Args**
```bash
blog -r REPO_NAME -c CATEGORY -f FILENAME
```
Example:
```bash
blog -r dev-blog -c programming/python -f async-tutorial
```
- Immediately saves when all required args are provided
- Still waits for clipboard content

#### **3. Partial CLI Args (Mixed Mode)**
```bash
blog -r blog  # Only specify repo, get prompts for rest
blog -c tech  # Only specify category, get prompts for rest
```

---

### **Repository Management**

#### **List Configured Repositories**
```bash
blog --list
```
Shows:
```
blog: C:\blogs\main
dev-blog: C:\blogs\dev
```

#### **Add New Repository During Session**
1. Run `blog`
2. When repository selection appears, type `a`
3. Enter new repository name and path

---

### **Examples**

**1. First-Time Setup**
```bash
> blog
Available repositories:
1. blog: Not configured
2. dev-blog: Not configured
Select repository (1-2) or 'a' to add new: 1
Enter path for blog: C:\my-blog  # Saved to config
```

**2. Quick Post Creation**
```bash
> blog -r dev-blog -c rust/tutorials -f ownership
# Copies content from clipboard automatically
Saved to: C:\blogs\dev\rust\tutorials\ownership.md
```

**3. Nested Categories**
```bash
> blog -c "webdev/css/animations" -f "keyframes-guide"
# Creates all intermediate folders
```

---

### **Help Command**
```bash
blog -h
```
Shows:
```
usage: blog [-h] [-r REPO] [-c CATEGORY] [-f FILE] [--list]

Blog content manager

options:
  -h, --help            show this help message and exit
  -r REPO, --repo REPO  Specify repository name (e.g., 'blog' or 'dev-blog')
  -c CATEGORY, --category CATEGORY
                        Specify category path (e.g., 'tech/python')
  -f FILE, --file FILE  Specify filename (without .md extension)
  --list                List available repositories
```

---

### **Workflow Tips**
1. **Clipboard First**: Copy your content before running the command
2. **Tab Completion**: Works for paths in interactive mode
3. **Config Location**: `C:\atari-monk\code\apps-data-store\blog_config.json`
4. **Special Characters**: Handles spaces and Unicode in paths/content

The script combines the speed of CLI arguments with the flexibility of interactive prompts when needed.
