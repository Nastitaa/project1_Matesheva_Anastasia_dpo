# Действия игрока
from .constants import ROOMS
from .utils import random_event


def show_inventory(game_state):
    """
    Отображает содержимое инвентаря игрока
    """
    inventory = game_state.get('player_inventory', [])

    if not inventory:
        print("\nВаш инвентарь пуст.")
    else:
        print("\n Ваш инвентарь:")
        for i, item in enumerate(inventory, 1):
            print(f"  {i}. {item}")


def get_input(prompt="> "):
    """
    Запрашивает ввод у пользователя с обработкой ошибок
    """
    try:
        user_input = input(prompt)
        return user_input.strip()
    except EOFError:
        print("\nВвод завершен. Выход из игры.")
        exit()
    except KeyboardInterrupt:
        print("\n\nИгра прервана. До свидания!")
        exit()


def move_player(game_state, direction):
    """
    Перемещает игрока в указанном направлении
    """
    current_room = game_state['current_room']
    room_data = ROOMS.get(current_room, {})
    exits = room_data.get('exits', {})

    # Проверяем, существует ли выход в этом направлении
    if direction in exits:
        next_room = exits[direction]
        
        # Проверяем доступ к treasure_room
        if next_room == 'treasure_room':
            inventory = game_state.get('player_inventory', [])
            if 'rusty_key' not in inventory:
                print("Дверь заперта. Нужен ключ, чтобы пройти дальше.")
                return False
            else:
                print(
                """
                Вы используете найденный ключ,
                чтобы открыть путь в комнату сокровищ.
                """)
        
        # Обновляем текущую комнату
        game_state['current_room'] = next_room
        
        # Увеличиваем шаг на единицу
        game_state['steps_taken'] = game_state.get('steps_taken', 0) + 1
        
        # Выводим описание новой комнаты
        from .utils import describe_current_room
        describe_current_room(game_state)
        
        # Вызываем случайное событие
        random_event(game_state)
        
        return True
    else:
        # Выводим сообщение, если выхода нет
        print("Нельзя пойти в этом направлении.")
        return False


def take_item(game_state, item_name):
    """
    Берет предмет из комнаты и добавляет в инвентарь
    """
    current_room = game_state['current_room']
    room_data = ROOMS.get(current_room, {})
    items = room_data.get('items', [])
    
    # Проверяем, есть ли предмет в комнате
    if item_name in items:
        # Проверяем, не пытается ли игрок взять сундук
        if item_name == 'treasure_chest':
            print("Вы не можете поднять сундук, он слишком тяжелый.")
            return False
            
        # Добавляем предмет в инвентарь игрока
        if 'player_inventory' not in game_state:
            game_state['player_inventory'] = []
        game_state['player_inventory'].append(item_name)
        
        # Удаляем предмет из списка предметов комнаты
        items.remove(item_name)
        
        # Печатаем сообщение о взятии предмета
        print(f"Вы подняли: {item_name}")
        return True
    else:
        # Выводим сообщение, если предмета нет
        print("Такого предмета здесь нет.")
        return False


def use_item(game_state, item_name):
    """
    Использует предмет из инвентаря
    """
    inventory = game_state.get('player_inventory', [])
    
    # Проверяем, есть ли предмет в инвентаре
    if item_name not in inventory:
        print("У вас нет такого предмета.")
        return False
    
    # Выполняем уникальное действие для каждого предмета
    match item_name:
        case 'torch':
            print(" Вы зажгли факел. Стало светлее.")
        
        case 'sword':
            print(" Вы почувствовали уверенность, держа меч в руках.")
        
        case 'bronze_box':
            print(" Вы открыли бронзовую шкатулку.")
            if 'rusty_key' not in inventory:
                game_state['player_inventory'].append('rusty_key')
                print("Внутри вы нашли ржавый ключ!")
            else:
                print("Шкатулка пуста.")
        
        case 'rusty_key':
            print(" Ржавый ключ. Возможно, он подойдет к какой-то двери.")
        
        case 'ancient_book':
            print(" Вы пролистали древнюю книгу, "
                  "но не смогли разобрать письмена.")
        
        case 'blue_crystal':
            print(" Кристалл мягко светится в ваших руках.")
        
        case 'silver_mirror':
            print(" В зеркале вы видите свое отражение.")
        
        case 'glowing_flower':
            print(" Цветок излучает мягкий свет.")
        
        case 'ancient_scroll':
            print(" Свиток покрыт древними символами, "
                  "которые вы не можете прочитать.")
        
        case _:
            print(f"Вы не знаете, как использовать {item_name}.")
    
    return True


def solve_puzzle(game_state):
    """
    Решает загадку в текущей комнате
    """
    from .utils import solve_puzzle as utils_solve_puzzle
    return utils_solve_puzzle(game_state)