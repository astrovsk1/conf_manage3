import sys
import csv
import struct
import os
from typing import List, Dict, Tuple, Any


class VMAssembler:
    def __init__(self):
        self.instructions = {
            'LOAD_CONST': 4,
            'READ_MEM': 6,
            'WRITE_MEM': 15,
            'NOT': 2
        }

        self.field_sizes = {
            'A': 5,
            'B': 6,
            'C': 32,
            'D': 32
        }

        self.command_size = 13

    # Парсинг аргументов командной строки
    def parse_arguments(self) -> Dict[str, Any]:
        if len(sys.argv) < 3:
            print("Использование: python main.py <input_file> <output_file> [--test]")
            sys.exit(1)

        return {
            'input_file': sys.argv[1],
            'output_file': sys.argv[2],
            'test_mode': '--test' in sys.argv
        }

    # Чтение и парсинг CSV файла с ассемблерным кодом
    def read_assembly_file(self, filename: str) -> List[Dict]:
        commands = []

        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                command = {
                    'instruction': row['instruction'].strip().upper(),
                    'fields': {}
                }

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

    # Валидация размеров полей команды
    def validate_fields(self, command: Dict):
        for field, value in command['fields'].items():
            max_value = (1 << self.field_sizes[field]) - 1
            if value > max_value:
                raise ValueError(f"Поле {field} превышает максимальное значение: {value} > {max_value}")

    # Трансляция в промежуточное представление
    def assemble_to_intermediate(self, commands: List[Dict]) -> List[Dict]:
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

    # Упаковка полей команды в бинарное представление
    def pack_fields_to_binary(self, command: Dict) -> bytes:
        if 'D' in command:
            value = (command['A'] << 99) | (command['B'] << 93) | (command['C'] << 61) | command['D']
        else:
            value = (command['A'] << 99) | (command['B'] << 93) | command['C']

        return value.to_bytes(13, byteorder='big', signed=False)

    # Трансляция промежуточного представления в машинный код
    def assemble_to_binary(self, intermediate: List[Dict]) -> bytes:
        binary_code = b''

        for cmd in intermediate:
            binary_code += self.pack_fields_to_binary(cmd)

        return binary_code

    # Вывод промежуточного представления в тестовом режиме
    def display_intermediate_representation(self, intermediate: List[Dict]):
        print("Промежуточное представление программы:")
        for i, cmd in enumerate(intermediate):
            print(f"Команда {i}:")
            for field, value in cmd.items():
                print(f"  {field}: {value}")
            print()

    # Вывод бинарного представления в тестовом режиме
    def display_binary_representation(self, binary_code: bytes):
        print("Бинарное представление программы:")
        for i in range(0, len(binary_code), self.command_size):
            chunk = binary_code[i:i + self.command_size]
            hex_bytes = [f"0x{byte:02X}" for byte in chunk]
            print(f"Команда {i // self.command_size}: {', '.join(hex_bytes)}")

    # Сохранение бинарного кода в файл
    def save_binary(self, binary_code: bytes, filename: str):
        with open(filename, 'wb') as f:
            f.write(binary_code)

        file_size = os.path.getsize(filename)
        print(f"Размер двоичного файла: {file_size} байт")

    # Запуск тестов из спецификации УВМ
    def run_tests(self):
        test_cases = [
            {
                'name': 'LOAD_CONST тест',
                'csv_content': 'instruction,field1,field2\nLOAD_CONST,31,140',
                'expected_intermediate': {'A': 4, 'B': 31, 'C': 140}
            },
            {
                'name': 'READ_MEM тест',
                'csv_content': 'instruction,field1,field2,field3\nREAD_MEM,29,344,265',
                'expected_intermediate': {'A': 6, 'B': 29, 'C': 344, 'D': 265}
            },
            {
                'name': 'WRITE_MEM тест',
                'csv_content': 'instruction,field1,field2\nWRITE_MEM,63,403',
                'expected_intermediate': {'A': 15, 'B': 63, 'C': 403}
            },
            {
                'name': 'NOT тест',
                'csv_content': 'instruction,field1,field2\nNOT,45,240',
                'expected_intermediate': {'A': 2, 'B': 45, 'C': 240}
            }
        ]

        print("Запуск тестов из спецификации УВМ:")
        print("=" * 50)

        all_passed = True

        for test in test_cases:
            print(f"\n{test['name']}:")

            with open('test_temp.csv', 'w', encoding='utf-8') as f:
                f.write(test['csv_content'])

            try:
                commands = self.read_assembly_file('test_temp.csv')
                intermediate = self.assemble_to_intermediate(commands)
                binary = self.assemble_to_binary(intermediate)

                if len(intermediate) == 1:
                    result_intermediate = intermediate[0]
                    if result_intermediate == test['expected_intermediate']:
                        print("   Промежуточное представление верно")
                    else:
                        print("   ОШИБКА: Промежуточное представление неверно")
                        print(f"    Ожидалось: {test['expected_intermediate']}")
                        print(f"    Получено: {result_intermediate}")
                        all_passed = False

                print("   Бинарное представление:")
                hex_bytes = [f"0x{byte:02X}" for byte in binary]
                print(f"    {', '.join(hex_bytes)}")

            except Exception as e:
                print(f"   ОШИБКА: {e}")
                all_passed = False

            finally:
                if os.path.exists('test_temp.csv'):
                    os.remove('test_temp.csv')

        print("\n" + "=" * 50)
        if all_passed:
            print(" Все тесты пройдены успешно!")
        else:
            print(" Некоторые тесты не пройдены")

        return all_passed


# Основная функция ассемблера
def main():
    assembler = VMAssembler()
    args = assembler.parse_arguments()

    if args['test_mode']:
        assembler.run_tests()
        return

    try:
        commands = assembler.read_assembly_file(args['input_file'])
        intermediate = assembler.assemble_to_intermediate(commands)
        assembler.display_intermediate_representation(intermediate)
        binary_code = assembler.assemble_to_binary(intermediate)
        assembler.display_binary_representation(binary_code)
        assembler.save_binary(binary_code, args['output_file'])

        print(f"Ассемблирование завершено успешно!")
        print(f"Обработано команд: {len(intermediate)}")

    except Exception as e:
        print(f"Ошибка ассемблирования: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()