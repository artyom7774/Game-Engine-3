import subprocess


def handle_output(output):
    # Ваша функция для обработки вывода
    print("Handling output:")
    print(output)


commands = [
    "echo Hello",
    "echo World",
    "ls -l"
]

for command in commands:
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # Проверка на ошибки
    if result.returncode != 0:
        print(f"Error executing {command}: {result.stderr}")
    else:
        handle_output(result.stdout)
