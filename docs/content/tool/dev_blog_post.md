# Dev Blog Post Script

Stores post from clipboard in dev-blog repo according to rules

- Functionality:
  - Stores config in path
  - Config has fields repo_path, current_content, current_category
  - Config is set with input if not exists
  - Combines path with folder names and ensure they exist
  - Produces metadata
  - Takes md file from clipboard and stores it in configured path
