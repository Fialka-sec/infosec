def print_field(field):
    """Печать игрового поля"""
    print("\n  0 1 2")
    for i in range(3):
        print(f"{i} {field[i][0]} {field[i][1]} {field[i][2]}")
    print()

def check_winner(field):
    """Проверка победителя"""
    # Проверка строк
    for row in field:
        if row[0] == row[1] == row[2] != '-':
            return row[0]
    
    # Проверка столбцов
    for col in range(3):
        if field[0][col] == field[1][col] == field[2][col] != '-':
            return field[0][col]
    
    # Проверка диагоналей
    if field[0][0] == field[1][1] == field[2][2] != '-':
        return field[0][0]
    if field[0][2] == field[1][1] == field[2][0] != '-':
        return field[0][2]
    
    return None

def is_full(field):
    """Проверка заполненности поля"""
    for row in field:
        if '-' in row:
            return False
    return True

def main():
    """Основная игра"""
    # Инициализация поля
    field = [['-' for _ in range(3)] for _ in range(3)]
    current_player = 'x'
    
    print("=" * 30)
    print("Игра 'Крестики-нолики'")
    print("=" * 30)
    print_field(field)
    
    while True:
        # Ход игрока
        print(f"Ход игрока '{current_player}'")
        try:
            row = int(input("Введите номер строки (0-2): "))
            col = int(input("Введите номер столбца (0-2): "))
            
            # Проверка корректности ввода
            if row < 0 or row > 2 or col < 0 or col > 2:
                print("❌ Координаты должны быть от 0 до 2!")
                continue
            
            if field[row][col] != '-':
                print("❌ Эта клетка уже занята!")
                continue
            
            # Установка значения
            field[row][col] = current_player
            print_field(field)
            
            # Проверка победителя
            winner = check_winner(field)
            if winner:
                print("=" * 30)
                print(f"🎉 Победил игрок '{winner}'!")
                print("=" * 30)
                break
            
            # Проверка ничьей
            if is_full(field):
                print("=" * 30)
                print("🤝 Ничья!")
                print("=" * 30)
                break
            
            # Смена игрока
            current_player = 'o' if current_player == 'x' else 'x'
            
        except ValueError:
            print("❌ Введите корректное число!")
        except KeyboardInterrupt:
            print("\n\nИгра прервана.")
            break

if __name__ == "__main__":
    main()