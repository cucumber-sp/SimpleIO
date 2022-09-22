# SimpleIO

#### Simple Object-based IO library for python scripts. 

Usage:
```python
import sys
from simple_io import *

# Get FolderPath object of script folder
script_folder = FolderPath(sys.path[0])

# Creating subfolder
subfolder = script_folder.clone_and_extend("Subfolder").create_folder()

# Creating text file in subfolder and writing some data inside
text_file = subfolder.extend_to_file("file.txt")
text_file.write_text("Hello, world!")

# Delete subfolder
subfolder.delete_folder()

# Print all files names in script folder
for file in script_folder.get_files_in_folder():
    print(str(file))
```
