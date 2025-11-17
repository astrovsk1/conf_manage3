import sys
import csv
import struct
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

    def parse_arguments(self) -> Dict[str, Any]:
        # Парсинг аргументов командной строки
        if len(sys.argv) < 3:
            print("Использование: python assembler.py <input_file> <output_file> [--test]")
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

    def display_intermediate_representation(self, intermediate: List[Dict]):
        # Вывод промежуточного представления в тестовом режиме
        print("Промежуточное представление программы:")
        for i, cmd in enumerate(intermediate):
            print(f"Команда {i}:")
            for field, value in cmd.items():
                print(f"  {field}: {value}")
            print()

    def save_intermediate(self, intermediate: List[Dict], filename: str):
        # Сохранение промежуточного представления (заглушка для этапа 1)
        with open(filename, 'w') as f:
            for cmd in intermediate:
                f.write(str(cmd) + '\n')

    def run_tests(self):
        # Запуск тестов из спецификации УВМ
        test_cases = [
            {
                'name': 'LOAD_CONST тест',
                'expected': {'A': 4, 'B': 279, 'C': 140},
                'csv_content': 'instruction,field1,field2\nLOAD_CONST,279,140'
            },
            {
                'name': 'READ_MEM тест',
                'expected': {'A': 6, 'B': 29, 'C': 344, 'D': 265},
                'csv_content': 'instruction,field1,field2,field3\nREAD_MEM,29,344,265'
            },
            {
                'name': 'WRITE_MEM тест',
                'expected': {'A': 15, 'B': 591, 'C': 403},
                'csv_content': 'instruction,field1,field2\nWRITE_MEM,591,403'
            },
            {
                'name': 'NOT тест',
                'expected': {'A': 2, 'B': 280, 'C': 240},
                'csv_content': 'instruction,field1,field2\nNOT,280,240'
            }
        ]

        print("Запуск тестов из спецификации УВМ:")
        print("=" * 50)

        for test in test_cases:
            print(f"\n{test['name']}:")

            # Создаем временный файл для теста
            with open('test_temp.csv', 'w', encoding='utf-8') as f:
                f.write(test['csv_content'])

            try:
                # Читаем и ассемблируем команду
                commands = self.read_assembly_file('test_temp.csv')
                intermediate = self.assemble_to_intermediate(commands)

                # Проверяем результат
                if len(intermediate) == 1:
                    result = intermediate[0]
                    if result == test['expected']:
                        print("   Результат соответствует ожидаемому")
                        print(f"  Поля: {result}")
                    else:
                        print("   Результат не соответствует ожидаемому")
                        print(f"  Ожидалось: {test['expected']}")
                        print(f"  Получено: {result}")
                else:
                    print("  ✗ ОШИБКА: Неверное количество команд")

            except Exception as e:
                print(f"   ОШИБКА: {e}")

            finally:
                # Удаляем временный файл
                import os
                if os.path.exists('test_temp.csv'):
                    os.remove('test_temp.csv')


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

        # Сохранение результата
        assembler.save_intermediate(intermediate, args['output_file'])

        print(f"Ассемблирование завершено успешно!")
        print(f"Обработано команд: {len(intermediate)}")

    except Exception as e:
        print(f"Ошибка ассемблирования: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()