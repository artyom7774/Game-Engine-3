with open("TODO.txt", "r", encoding="utf-8") as file:
    text = file.read()

count = 0

for element in text.split("\n"):
    if len(element) > 7:
        if element[6] in ("x", "-") and element[0] != "-":
            count += 1

print(count)
