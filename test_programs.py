# test_programs.py
# Тестовые программы для проверки ассемблера УВМ

def create_test_files():
    # Создание тестовых файлов для всех команд спецификации

    # Тест LOAD_CONST (A=4, B=279, C=140)
    with open('test_load_const.csv', 'w', encoding='utf-8') as f:
        f.write("instruction,field1,field2\n")
        f.write("LOAD_CONST,279,140\n")

    # Тест READ_MEM (A=6, B=29, C=344, D=265)
    with open('test_read_mem.csv', 'w', encoding='utf-8') as f:
        f.write("instruction,field1,field2,field3\n")
        f.write("READ_MEM,29,344,265\n")

    # Тест WRITE_MEM (A=15, B=591, C=403)
    with open('test_write_mem.csv', 'w', encoding='utf-8') as f:
        f.write("instruction,field1,field2\n")
        f.write("WRITE_MEM,591,403\n")

    # Тест NOT (A=2, B=280, C=240)
    with open('test_not.csv', 'w', encoding='utf-8') as f:
        f.write("instruction,field1,field2\n")
        f.write("NOT,280,240\n")

    # Пример программы с несколькими командами
    with open('example_program.csv', 'w', encoding='utf-8') as f:
        f.write("instruction,field1,field2,field3\n")
        f.write("LOAD_CONST,100,42\n")
        f.write("NOT,101,100\n")
        f.write("READ_MEM,5,102,103\n")
        f.write("WRITE_MEM,104,105\n")

    print("Созданы тестовые файлы:")
    print("- test_load_const.csv (LOAD_CONST тест)")
    print("- test_read_mem.csv (READ_MEM тест)")
    print("- test_write_mem.csv (WRITE_MEM тест)")
    print("- test_not.csv (NOT тест)")
    print("- example_program.csv (пример программы)")


def verify_test_files():
    # Проверка созданных тестовых файлов
    test_files = [
        'test_load_const.csv',
        'test_read_mem.csv',
        'test_write_mem.csv',
        'test_not.csv',
        'example_program.csv'
    ]

    print("\nПроверка созданных файлов:")
    for filename in test_files:
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
                print(f" {filename}: {len(content.splitlines())} строк")
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
    print("\n2. Тестирование примера программы:")
    print("   python main.py example_program.csv output.bin --test")