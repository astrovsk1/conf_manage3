# Тестовые программы для проверки ассемблера УВМ
def create_test_files():
    with open('test_load_const.csv', 'w', encoding='utf-8') as f:
        f.write("instruction,field1,field2\n")
        f.write("LOAD_CONST,31,140\n")

    with open('test_read_mem.csv', 'w', encoding='utf-8') as f:
        f.write("instruction,field1,field2,field3\n")
        f.write("READ_MEM,29,344,265\n")

    with open('test_write_mem.csv', 'w', encoding='utf-8') as f:
        f.write("instruction,field1,field2\n")
        f.write("WRITE_MEM,63,403\n")

    with open('test_not.csv', 'w', encoding='utf-8') as f:
        f.write("instruction,field1,field2\n")
        f.write("NOT,45,240\n")

    with open('all_tests_program.csv', 'w', encoding='utf-8') as f:
        f.write("instruction,field1,field2,field3\n")
        f.write("LOAD_CONST,31,140\n")
        f.write("READ_MEM,29,344,265\n")
        f.write("WRITE_MEM,63,403\n")
        f.write("NOT,45,240\n")

    with open('example_program.csv', 'w', encoding='utf-8') as f:
        f.write("instruction,field1,field2,field3\n")
        f.write("LOAD_CONST,10,42\n")
        f.write("NOT,11,100\n")
        f.write("READ_MEM,5,102,103\n")
        f.write("WRITE_MEM,12,105\n")

    print("Созданы тестовые файлы для Этапа 2:")
    print("- test_load_const.csv (LOAD_CONST тест)")
    print("- test_read_mem.csv (READ_MEM тест)")
    print("- test_write_mem.csv (WRITE_MEM тест)")
    print("- test_not.csv (NOT тест)")
    print("- all_tests_program.csv (все тестовые команды)")
    print("- example_program.csv (пример программы)")


# Проверка созданных тестовых файлов
def verify_test_files():
    test_files = [
        'test_load_const.csv',
        'test_read_mem.csv',
        'test_write_mem.csv',
        'test_not.csv',
        'all_tests_program.csv',
        'example_program.csv'
    ]

    print("\nПроверка созданных файлов:")
    for filename in test_files:
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.splitlines()
                print(f" {filename}: {len(lines)} строк, {len(lines) - 1} команд")
        except FileNotFoundError:
            print(f" {filename}: файл не найден")


if __name__ == "__main__":
    create_test_files()
    verify_test_files()

    print("\nИнструкция по тестированию:")
    print("1. Запуск тестов из спецификации:")
    print("   python main.py test_load_const.csv output.bin --test")
    print("   python main.py test_read_mem.csv output.bin --test")
    print("   python main.py test_write_mem.csv output.bin --test")
    print("   python main.py test_not.csv output.bin --test")
    print("\n2. Тестирование программы со всеми командами:")
    print("   python main.py all_tests_program.csv all_tests.bin --test")
    print("\n3. Обычное ассемблирование:")
    print("   python main.py example_program.csv program.bin")