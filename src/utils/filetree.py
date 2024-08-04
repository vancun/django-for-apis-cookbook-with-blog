# Based on https://stackoverflow.com/a/59109706/6949234
from pathlib import Path


def should_exclude(path):
    # Define patterns for exclusion
    excluded_patterns = ["__pycache__", "migrations", ".git", "docs"]

    # Check if any excluded pattern is in the path
    return any(pattern in path for pattern in excluded_patterns)


def gen_tree(dir_path: Path, prefix: str = ""):
    """A recursive generator, given a directory Path object
    will yield a visual tree structure line by line
    with each line prefixed by the same characters
    """
    # prefix components:
    space = "    "
    branch = "│   "
    # pointers:
    tee = "├── "
    last = "└── "

    contents = [f for f in dir_path.iterdir() if not should_exclude(str(f))]
    # contents each get pointers that are ├── with a final └── :
    pointers = [tee] * (len(contents) - 1) + [last]
    for pointer, path in zip(pointers, contents):
        yield prefix + pointer + path.name
        if path.is_dir():  # extend the prefix and recurse:
            extension = branch if pointer == tee else space
            # i.e. space because last, └── , above so no more |
            yield from gen_tree(path, prefix=prefix + extension)


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate a file tree for a directory."
    )
    parser.add_argument(
        "dir",
        nargs="?",
        default=".",
        help="The directory to generate a tree for (default: current directory).",
    )
    args = parser.parse_args()
    print("There: ", args)
    for e in gen_tree(Path(args.dir)):
        print(e)


if __name__ == "__main__":
    main()
