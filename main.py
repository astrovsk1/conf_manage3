import sys
import csv
import struct
import os
from typing import List, Dict, Tuple, Any


class VMAssembler:
    def __init__(self):
        # Инициализация инструкций и размеров полей
        self.instructions = {
            'LOAD_CONST': 4,
            'READ_MEM': 6,
            'WRITE_MEM': 15,
            'NOT': 2
        }

        self.field_sizes = {
            'A': 5,
            'B': 32,
            'C': 32,
            'D': 32
        }

        self.command_size = 13  # 13 байт на команду

    def parse_arguments(self) -> Dict[str, Any]:
        # Парсинг аргументов командной строки
        if len(sys.argv) < 3:
            print("Использование: python main.py <input_file> <output_file> [--test]")
            sys.exit(1)

        return {
            'input_file': sys.argv[1],
            'output_file': sys.argv[2],
            'test_mode': '--test' in sys.argv
        }

    def read_assembly_file(self, filename: str) -> List[Dict]:
        # Чтение и парсинг CSV файла с ассемблерным кодом
        commands = []

        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                command = {
                    'instruction': row['instruction'].strip().upper(),
                    'fields': {}
                }

                # Парсинг полей в зависимости от инструкции
                if command['instruction'] == 'LOAD_CONST':
                    command['fields']['A'] = self.instructions['LOAD_CONST']
                    command['fields']['B'] = int(row['field1'])
                    command['fields']['C'] = int(row['field2'])

                elif command['instruction'] == 'READ_MEM':
                    command['fields']['A'] = self.instructions['READ_MEM']
                    command['fields']['B'] = int(row['field1'])
                    command['fields']['C'] = int(row['field2'])
                    command['fields']['D'] = int(row['field3'])

                elif command['instruction'] == 'WRITE_MEM':
                    command['fields']['A'] = self.instructions['WRITE_MEM']
                    command['fields']['B'] = int(row['field1'])
                    command['fields']['C'] = int(row['field2'])

                elif command['instruction'] == 'NOT':
                    command['fields']['A'] = self.instructions['NOT']
                    command['fields']['B'] = int(row['field1'])
                    command['fields']['C'] = int(row['field2'])

                commands.append(command)

        return commands

    def validate_fields(self, command: Dict):
        # Валидация размеров полей
        for field, value in command['fields'].items():
            max_value = (1 << self.field_sizes[field]) - 1
            if value > max_value:
                raise ValueError(f"Поле {field} превышает максимальное значение: {value} > {max_value}")

    def assemble_to_intermediate(self, commands: List[Dict]) -> List[Dict]:
        # Трансляция в промежуточное представление
        intermediate = []

        for cmd in commands:
            self.validate_fields(cmd)

            if cmd['instruction'] == 'LOAD_CONST':
                intermediate.append({
                    'A': cmd['fields']['A'],
                    'B': cmd['fields']['B'],
                    'C': cmd['fields']['C']
                })

            elif cmd['instruction'] == 'READ_MEM':
                intermediate.append({
                    'A': cmd['fields']['A'],
                    'B': cmd['fields']['B'],
                    'C': cmd['fields']['C'],
                    'D': cmd['fields']['D']
                })

            elif cmd['instruction'] == 'WRITE_MEM':
                intermediate.append({
                    'A': cmd['fields']['A'],
                    'B': cmd['fields']['B'],
                    'C': cmd['fields']['C']
                })

            elif cmd['instruction'] == 'NOT':
                intermediate.append({
                    'A': cmd['fields']['A'],
                    'B': cmd['fields']['B'],
                    'C': cmd['fields']['C']
                })

        return intermediate

    def pack_fields_to_binary(self, command: Dict) -> bytes:
        # Упаковка полей команды в бинарное представление
        if 'D' in command:  # READ_MEM команда
            # A: 5 бит, B: 6 бит, C: 32 бита, D: 32 бита
            value = (command['A'] << 69) | (command['B'] << 63) | (command['C'] << 31) | command['D']
            # Упаковка в 13 байт (104 бита)
            packed = struct.pack('>13s', value.to_bytes(13, byteorder='big', signed=False))
        else:  # Остальные команды (A: 5 бит, B: 32 бита, C: 32 бита)
            value = (command['A'] << 64) | (command['B'] << 32) | command['C']
            # Упаковка в 13 байт (104 бита)
            packed = struct.pack('>13s', value.to_bytes(13, byteorder='big', signed=False))

        return packed

    def assemble_to_binary(self, intermediate: List[Dict]) -> bytes:
        # Трансляция промежуточного представления в машинный код
        binary_code = b''

        for cmd in intermediate:
            binary_code += self.pack_fields_to_binary(cmd)

        return binary_code

    def display_intermediate_representation(self, intermediate: List[Dict]):
        # Вывод промежуточного представления в тестовом режиме
        print("Промежуточное представление программы:")
        for i, cmd in enumerate(intermediate):
            print(f"Команда {i}:")
            for field, value in cmd.items():
                print(f"  {field}: {value}")
            print()

    def display_binary_representation(self, binary_code: bytes):
        # Вывод бинарного представления в тестовом режиме
        print("Бинарное представление программы:")
        for i in range(0, len(binary_code), self.command_size):
            chunk = binary_code[i:i + self.command_size]
            hex_bytes = [f"0x{byte:02X}" for byte in chunk]
            print(f"Команда {i // self.command_size}: {', '.join(hex_bytes)}")

    def save_binary(self, binary_code: bytes, filename: str):
        # Сохранение бинарного кода в файл
        with open(filename, 'wb') as f:
            f.write(binary_code)

        # Вывод размера файла
        file_size = os.path.getsize(filename)
        print(f"Размер двоичного файла: {file_size} байт")

    def run_tests(self):
        # Запуск тестов из спецификации УВМ
        test_cases = [
            {
                'name': 'LOAD_CONST тест',
                'expected_intermediate': {'A': 4, 'B': 279, 'C': 140},
                'expected_binary': bytes(
                    [0xE4, 0x22, 0x00, 0x00, 0x80, 0x11, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]),
                'csv_content': 'instruction,field1,field2\nLOAD_CONST,279,140'
            },
            {
                'name': 'READ_MEM тест',
                'expected_intermediate': {'A': 6, 'B': 29, 'C': 344, 'D': 265},
                'expected_binary': bytes(
                    [0xA6, 0xC3, 0x0A, 0x00, 0x00, 0x48, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]),
                'csv_content': 'instruction,field1,field2,field3\nREAD_MEM,29,344,265'
            },
            {
                'name': 'WRITE_MEM тест',
                'expected_intermediate': {'A': 15, 'B': 591, 'C': 403},
                'expected_binary': bytes(
                    [0xEF, 0x49, 0x00, 0x00, 0x60, 0x32, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]),
                'csv_content': 'instruction,field1,field2\nWRITE_MEM,591,403'
            },
            {
                'name': 'NOT тест',
                'expected_intermediate': {'A': 2, 'B': 280, 'C': 240},
                'expected_binary': bytes(
                    [0x02, 0x23, 0x00, 0x00, 0x00, 0x1E, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]),
                'csv_content': 'instruction,field1,field2\nNOT,280,240'
            }
        ]

        print("Запуск тестов из спецификации УВМ:")
        print("=" * 50)

        all_passed = True

        for test in test_cases:
            print(f"\n{test['name']}:")

            # Создаем временный файл для теста
            with open('test_temp.csv', 'w', encoding='utf-8') as f:
                f.write(test['csv_content'])

            try:
                # Читаем и ассемблируем команду
                commands = self.read_assembly_file('test_temp.csv')
                intermediate = self.assemble_to_intermediate(commands)
                binary = self.assemble_to_binary(intermediate)

                # Проверяем промежуточное представление
                if len(intermediate) == 1:
                    result_intermediate = intermediate[0]
                    if result_intermediate == test['expected_intermediate']:
                        print("   Промежуточное представление верно")
                    else:
                        print("   ОШИБКА: Промежуточное представление неверно")
                        print(f"    Ожидалось: {test['expected_intermediate']}")
                        print(f"    Получено: {result_intermediate}")
                        all_passed = False

                # Проверяем бинарное представление
                if binary == test['expected_binary']:
                    print("   Бинарное представление верно")
                    hex_bytes = [f"0x{byte:02X}" for byte in binary]
                    print(f"    Байты: {', '.join(hex_bytes)}")
                else:
                    print("   ОШИБКА: Бинарное представление неверно")
                    expected_hex = [f"0x{byte:02X}" for byte in test['expected_binary']]
                    result_hex = [f"0x{byte:02X}" for byte in binary]
                    print(f"    Ожидалось: {', '.join(expected_hex)}")
                    print(f"    Получено: {', '.join(result_hex)}")
                    all_passed = False

            except Exception as e:
                print(f"   ОШИБКА: {e}")
                all_passed = False

            finally:
                # Удаляем временный файл
                import os
                if os.path.exists('test_temp.csv'):
                    os.remove('test_temp.csv')

        print("\n" + "=" * 50)
        if all_passed:
            print(" Все тесты пройдены успешно!")
        else:
            print(" Некоторые тесты не пройдены")

        return all_passed


def main():
    # Основная функция ассемблера
    assembler = VMAssembler()
    args = assembler.parse_arguments()

    # Если включен режим тестирования, запускаем тесты
    if args['test_mode']:
        assembler.run_tests()
        return

    try:
        # Чтение исходного файла
        commands = assembler.read_assembly_file(args['input_file'])

        # Трансляция в промежуточное представление
        intermediate = assembler.assemble_to_intermediate(commands)

        # Вывод промежуточного представления
        assembler.display_intermediate_representation(intermediate)

        # Трансляция в бинарный код
        binary_code = assembler.assemble_to_binary(intermediate)

        # Вывод бинарного представления
        assembler.display_binary_representation(binary_code)

        # Сохранение результата
        assembler.save_binary(binary_code, args['output_file'])

        print(f"Ассемблирование завершено успешно!")
        print(f"Обработано команд: {len(intermediate)}")

    except Exception as e:
        print(f"Ошибка ассемблирования: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()