import os

def generate_tree(start_path, indent="", file=None):
    items = sorted(os.listdir(start_path))
    for i, item in enumerate(items):
        path = os.path.join(start_path, item)
        is_last = (i == len(items) - 1)

        connector = "└── " if is_last else "├── "
        line = indent + connector + item

        print(line)
        if file:
            file.write(line + "\n")

        if os.path.isdir(path):
            extension = "    " if is_last else "│   "
            generate_tree(path, indent + extension, file)

folder_path = "C:\\Users\\LOQ\\Desktop\\TeachingHubAcademy\\server"

with open("file_tree.txt", "w", encoding="utf-8") as f:
    generate_tree(folder_path, file=f)
