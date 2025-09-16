import os
import re
import argparse


def search_files(directory, keywords, output_file):
    pattern = re.compile("|".join(rf"^[^(\n]*{re.escape(kw)}[^(\n]*\(" for kw in keywords))

    configs = set()
    prefixes = set()
    count = 0

    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            print(f"Retrieving from {file}...")
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    for line in f:
                        if pattern.search(line):
                            count += 1
                            configs.add(line.strip())
                            prefix = line[: line.index("(")].strip()
                            prefixes.add(prefix)
            except (UnicodeDecodeError, PermissionError) as e:
                print(f"Error reading {file_path}: {e}")
                continue
    print(f"Retrieved {count} configs")
    print(f"Get {len(configs)} unique configs")
    print(f"APIs: {sorted(prefixes)}")

    with open(output_file, "w", encoding="utf-8") as out_f:
        for line in sorted(configs):
            out_f.write(f"{line}\n")
    print(f"Saved to {output_file}")


if __name__ == "__main__":
    default_directory = "tester/api_config/5_accuracy"
    default_keywords = []
    default_output = "tester/api_config/api_config_retrieved.txt"

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--directory",
        default=default_directory,
    )
    parser.add_argument("--keywords", nargs="+", default=default_keywords)
    parser.add_argument(
        "--output",
        default=default_output,
    )
    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print(f"Error: Directory {args.directory} does not exist")
    elif not args.keywords:
        print("Error: Please provide at least one keyword")
    else:
        search_files(args.directory, args.keywords, args.output)
