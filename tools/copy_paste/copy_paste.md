# Copy Paste Script 

Copy code files to predefined paths

- Assumptions:
  - Ask questions if something is unclear
  - Tell if you have simpler idea
  - Write so that even machine can use this code
  - Simpliffy as much as possible
- Development:
  - Use python
  - No comments, self-documenting code only
  - Write pytest unit tests first
  - Implement class to pass tests
  - Implement script to use class in CLI
  - CLI script in separate file
  - For CLI use argparse
- Functionality:
  - First time it runs it asks about data
- Takes path, category
- Saves data in config, under some key, also ask user to name key
- Allow option to add to config and select current by key
- Ask for path, category in loop, place this obj in array under key in config
- When script is run normally take current key and print user category, ask for file name
- Then wait for file from clipboard, store it (watch for new lines, keep it as original) in path, on enter
- This way we will handle adding files to paths faster, hope this is clear  
