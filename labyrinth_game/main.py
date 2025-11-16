#!/usr/bin/env python3
from .player_actions import (
    get_input,
    move_player,
    show_inventory,
    solve_puzzle,
    take_item,
    use_item,
)
from .utils import (
    attempt_open_treasure,
    describe_current_room,
    is_valid_direction,
    parse_command,
    show_help,
)


def process_command(game_state, user_input):
    """
    Обрабатывает команду пользователя
    """
    # Разделяем строку на команду и аргумент
    command, argument = parse_command(user_input)
    
    # Используем match/case для определения команды
    match command:
        case 'look':
            describe_current_room(game_state)
        
        case 'go':
            if not argument:
                print("Укажите направление: идти [north/south/east/west]")
                return
            
            direction = argument
            if not is_valid_direction(direction):
                print("Неверное направление. Используйте: north/south/east/west)")
                return
            
            move_player(game_state, direction)
        
        # Обработка односложных команд направления
        case 'north' | 'south' | 'east' | 'west':
            direction = command
            move_player(game_state, direction)
        
        case 'take':
            if not argument:
                print("Укажите предмет: взять [название предмета]")
                return
            
            take_item(game_state, argument)
        
        case 'use':
            if not argument:
                print("Укажите предмет: использовать [название предмета]")
                return
            
            use_item(game_state, argument)
        
        case 'solve':
            # Если в комнате с сокровищами, пытаемся открыть сундук
            if game_state['current_room'] == 'treasure_room':
                attempt_open_treasure(game_state)
            else:
                solve_puzzle(game_state)
        
        case 'inventory':
            show_inventory(game_state)
        
        case 'quit' | 'exit':
            print("Спасибо за игру! До свидания!")
            game_state['game_over'] = True
        
        case 'help':
            show_help()
        
        case _:
            print("Неизвестная команда. Введите 'help' для списка команд.")


def main():
    game_state = {
        'player_inventory': [],  # Инвентарь игрока
        'current_room': 'entrance',  # Текущая комната
        'game_over': False,  # Значения окончания игры
        'steps_taken': 0  # Количество шагов
    }
    
    # Выводим приветственное сообщение
    print("Добро пожаловать в Лабиринт сокровищ!")
    show_help()
    
    # Описываем стартовую комнату
    describe_current_room(game_state)
    
    # Основной игровой цикл
    while not game_state['game_over']:
        try:
            # Считываем команду от пользователя
            user_input = get_input("\nВведите команду: ")
            
            # Обработка пустого ввода
            if not user_input:
                continue
            
            # Обрабатываем команду
            process_command(game_state, user_input)
                
        except KeyboardInterrupt:
            print("\n\nИгра прервана. До свидания!")
            game_state['game_over'] = True
        except Exception as e:
            print(f"Произошла ошибка: {e}")


# Стандартная конструкция для запуска функции main()
if __name__ == "__main__":
    main()