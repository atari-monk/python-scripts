## Mannual Testing

Here's a comprehensive manual testing guide for the blog tool CLI application:

### Setup Instructions
1. Install dependencies:
   ```bash
   pip install plumbum pyperclip
   ```

### General Testing Approach
- Run each command with and without arguments
- Test both interactive and direct modes
- Verify config file updates at `C:\atari-monk\code\apps-data-store\blog_config.json`

### 1. Configuration Management

**Test: Add Target**
```bash
# Direct mode
blog add-target my_blog C:/path/to/blog

# Interactive mode
blog add-target
> Enter target name: test_blog
> Enter path: C:/test/path
```

**Verification:**
- Check config file contains new target
- Try adding duplicate name (should fail)
- Try empty path (should fail)

**Test: Edit Target**
```bash
# Direct mode
blog edit-target my_blog C:/new/path

# Interactive mode
blog edit-target
> Select target to edit
> Enter new path: C:/updated/path
```

**Verification:**
- Verify path updates in config
- Try editing non-existent target (should fail)

**Test: Delete Target**
```bash
# Direct mode
blog delete-target my_blog

# Interactive mode
blog delete-target
> Select target to delete
```

**Verification:**
- Check target removed from config
- Try deleting non-existent target (should fail)

### 2. Content Navigation

**Test: List Categories**
```bash
# Basic
blog list-category

# With target
blog list-category --target my_blog

# With search
blog list-category -s python
```

**Verification:**
- Verify tree structure displays correctly
- Search should filter categories

**Test: List Files**
```bash
# All files
blog list-files

# Specific category
blog list-files -c tech/python

# With search
blog list-files -s "readme"
```

**Verification:**
- Files should be grouped by category
- Search should filter filenames

### 3. Content Operations

**Test: Save Content**
```bash
# Full command
blog save --target my_blog --category tech/python --file new_post

# Interactive mode
blog save
> Select target
> Enter category: tech/python
> Enter filename: test_post
> [Copy content to clipboard and press Enter]
```

**Verification:**
- Check file created at correct path
- Content should match clipboard
- Should create directories if needed

**Test: Open File**
```bash
# By filename
blog open-file my_post.md

# With category
blog open-file -c tech/python my_post.md

# Interactive selection
blog open-file
```

**Verification:**
- File should open in default/system editor
- Should handle missing files gracefully

### 4. Utility Commands

**Test: Print Config**
```bash
blog print-config
```

**Verification:**
- Should display all configured targets

### Edge Cases to Test
1. Empty configuration file
2. Non-existent target paths
3. Invalid file names
4. Missing category directories
5. Special characters in paths/filenames
6. Very long category paths

### Test Data Suggestions
- Create test directory structure with:
  ```
  /blog_root
    /tech
      /python
        intro.md
      /javascript
    /personal
  ```
- Use different target types (local paths, network paths)

### Verification Points
1. Config file integrity after each operation
2. Correct file system operations
3. Appropriate error messages
4. Interactive prompts handle invalid input
5. Command help texts are clear (`--help`)

Would you like me to elaborate on any particular test scenario or add more specific test cases?