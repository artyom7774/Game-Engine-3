import sys
import traceback

# Открываем файл для записи вывода
with open('output.log', 'w') as log_file:
    try:
        # Перенаправляем стандартный вывод и стандартный поток ошибок в файл
        sys.stderr = log_file

        # Ваш код здесь
        print("This is a message to the log file.")
        x = 1 / 0  # Пример ошибки

    except Exception as e:
        # Записываем трассировку стека в файл
        traceback.print_exc(file=log_file)

    finally:
        # Восстанавливаем стандартные потоки
        sys.stderr = sys.__stderr__

print("Программа завершена.")
