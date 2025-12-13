import os


def generate_tree(path, prefix="", file=None, depth=None, level=0):
    if depth is not None and level > depth:
        return

    try:
        entries = sorted(
            os.listdir(path),
            key=lambda x: (not os.path.isdir(os.path.join(path, x)), x.lower())
        )
    except PermissionError:
        return

    for index, entry in enumerate(entries):
        full_path = os.path.join(path, entry)
        is_last = index == len(entries) - 1

        branch = "└──" if is_last else "├──"
        spacer = "    " if is_last else "│   "

        icon = "📁" if os.path.isdir(full_path) else "📄"
        line = f"{prefix}{branch} {icon} {entry}"

        print(line)
        if file:
            file.write(line + "\n")

        if os.path.isdir(full_path):
            generate_tree(
                full_path,
                prefix + spacer,
                file,
                depth,
                level + 1
            )


def print_directory_tree(root_path, output_file="file_tree.txt", depth=None):
    title = f" Directory Tree "
    path_line = f" {root_path} "

    width = max(len(title), len(path_line)) + 4

    box = (
        f"╔{'═' * (width - 2)}╗\n"
        f"║{title.center(width - 2)}║\n"
        f"║{path_line.center(width - 2)}║\n"
        f"╚{'═' * (width - 2)}╝\n"
    )

    print(box)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(box)
        generate_tree(root_path, file=f, depth=depth)


# ---------------- MAIN ----------------

folder_path = input("Enter folder path: ").strip()

if not os.path.isdir(folder_path):
    print("❌ Invalid folder path.")
else:
    print_directory_tree(folder_path, depth=None)
    print("\n✔ Output saved to file_tree.txt")
