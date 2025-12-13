import os

def generate_tree(start_path, indent="", file=None):
    try:
        items = sorted(os.listdir(start_path))
    except PermissionError:
        return

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


# Get folder path from user
folder_path = input("Enter the folder path: ").strip()

if not os.path.isdir(folder_path):
    print("Invalid folder path.")
else:
    with open("file_tree.txt", "w", encoding="utf-8") as f:
        generate_tree(folder_path, file=f)
