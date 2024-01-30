# utils.d/add_file_path_comment.py
import os

ignore_files_list = [
    "__init__.py",
    "manage.py",
]

ignore_dirs = ["migrations"]


def add_file_path_comment(root_dir: str) -> None:
    """
    Add or update a file path comment to the top of every .py file in the directory
    and its subdirectories,
    excluding files in ignore_files_list and directories in ignore_dirs.
    """
    for root, _, files in os.walk(root_dir):
        if any(ignored_dir in root.split(os.sep) for ignored_dir in ignore_dirs):
            continue  # Skip files in ignored directories

        for file in files:
            if file.endswith(".py") and file not in ignore_files_list:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, root_dir)

                with open(file_path, "r") as f:
                    lines = f.readlines()

                # Check if the first 5 lines are path comments for .py files
                for i in range(5):
                    if len(lines) >= 1 and lines[0].startswith("# ") and lines[0].endswith(".py\n"):
                        lines.pop(0)
                    else:
                        break

                # Check if the top line is the path comment
                if not lines or not lines[0].startswith(f"# {relative_path}"):
                    lines.insert(0, f"# {relative_path}\n")

                with open(file_path, "w") as f:
                    f.writelines(lines)


if __name__ == "__main__":
    project_directory = "."  # Current directory. Change this if you want to target another directory.
    add_file_path_comment(project_directory)
