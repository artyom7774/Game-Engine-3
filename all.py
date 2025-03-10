import os

files = ["engine", "scr", "Game Engine 3.py"]
extensions = ["py", "pyx"]


def solve(root_paths, extensions):
    matching_files = []

    def search(path):
        if os.path.isdir(path):
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                search(item_path)

        elif os.path.isfile(path):
            for ext in extensions:
                if path.endswith(f".{ext}"):
                    matching_files.append(path)

                    break

        else:
            pass

    for root_path in root_paths:
        search(root_path)

    return matching_files


matching_files = solve(files, extensions)

text = ""

print(len(matching_files))

for file in matching_files:
    value = open(file, encoding="utf-8").read()

    text += f"\n##### {file} #####"

    for i, line in enumerate(value.split("\n")):
        text += "\n" + str(i + 1) + (5 - len(str(i))) * " " + " " + line

with open("out.txt", "w", encoding="utf-8") as file:
    file.write(text)
