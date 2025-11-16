# Вспомогательные функции
import math

from .constants import COMMANDS, MESSAGES, PUZZLES, ROOMS


def pseudo_random(seed, modulo):
    """
    Генерирует псевдослучайное число на основе синуса
    
    Args:
        seed (int): Начальное значение
        modulo (int): Модуль для диапазона результата
        
    Returns:
        int: Псевдослучайное число в диапазоне [0, modulo]
    """
    x = math.sin(seed * 12.9898) * 43758.5453
    fractional = x - math.floor(x)
    result = fractional * modulo
    return int(result)


def trigger_trap(game_state):
    """
    Активирует ловушку с негативными последствиями для игрока
    """
    print("💥 Ловушка активирована! Пол стал дрожать...")
    
    inventory = game_state.get('player_inventory', [])
    
    if inventory:
        # Выбираем случайный предмет для удаления
        item_index = pseudo_random(game_state.get('steps_taken', 0), len(inventory))
        lost_item = inventory.pop(item_index)
        print(f"💔 Вы потеряли предмет: {lost_item}")
    else:
        # Игрок получает урон
        damage_chance = pseudo_random(game_state.get('steps_taken', 0), 10)
        if damage_chance < 3:
            print("💀 Ловушка нанесла смертельный урон! Игра окончена.")
            game_state['game_over'] = True
        else:
            print("🛡️ Вам удалось увернуться от ловушки!")


def random_event(game_state):
    """
    Создает случайные события во время перемещения игрока
    """
    # Проверяем, произойдет ли событие (вероятность 1/10)
    event_chance = pseudo_random(game_state.get('steps_taken', 0), 10)
    if event_chance != 0:
        return
    
    # Выбираем тип события
    event_type = pseudo_random(game_state.get('steps_taken', 0) + 1, 3)
    
    match event_type:
        case 0:  # Находка
            print("✨ Вы нашли на полу блестящую монетку!")
            current_room = game_state['current_room']
            room_data = ROOMS.get(current_room, {})
            if 'coin' not in room_data.get('items', []):
                room_data.setdefault('items', []).append('coin')
        
        case 1:  # Испуг
            print("👂 Вы слышите странный шорох из темноты...")
            inventory = game_state.get('player_inventory', [])
            if 'sword' in inventory:
                print("⚔️ Вы достаете меч, и существо отступает!")
            else:
                print("😨 Вам становится не по себе...")
        
        case 2:  # Ловушка
            current_room = game_state['current_room']
            inventory = game_state.get('player_inventory', [])
            if current_room == 'trap_room' and 'torch' not in inventory:
                print("⚠️ Вы чувствуете опасность...")
                trigger_trap(game_state)


def show_help():
    """Отображение справки по командам с красивым форматированием"""
    print("\nДоступные команды:")
    for cmd, description in COMMANDS_HELP.items():
        print(f"  {cmd:<16} - {description}")


def parse_command(user_input):
    """Разбор введенной пользователем команды"""
    if not user_input:
        return None, None
    
    parts = user_input.lower().strip().split()
    command = parts[0]
    argument = parts[1] if len(parts) > 1 else None
    
    return command, argument


def is_valid_command(command):
    """Проверка валидности команды"""
    for cmd_type, cmd_list in COMMANDS.items():
        if command in cmd_list:
            return True
    return False


def get_command_type(command):
    """Определение типа команды"""
    for cmd_type, cmd_list in COMMANDS.items():
        if command in cmd_list:
            return cmd_type
    return None


def is_valid_direction(direction):
    """Проверка валидности направления"""
    valid_directions = ['north', 'south', 'east', 'west']
    return direction in valid_directions



def display_welcome():
    """Отображение приветственного сообщения"""
    print("=" * 50)
    print(MESSAGES['welcome'])
    print("=" * 50)


def format_room_description(description):
    """Форматирование описания комнаты"""
    print("\n" + "=" * 50)
    print(description)
    print("=" * 50)


def clear_screen():
    """Очистка экрана (кроссплатформенная)"""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')


def show_map(player):
    """Показать карту с посещенными комнатами"""
    from .constants import ROOMS
    
    print("\n--- КАРТА ЛАБИРИНТА ---")
    for room_name in player.visited_rooms:
        room_data = ROOMS.get(room_name, {})
        exits = room_data.get('exits', {})
        
        marker = "★" if room_name == player.current_room else "○"
        print(f"{marker} {room_name}: {', '.join(exits.keys())}")
    print("★ - ваше текущее положение")


def describe_current_room(game_state):
    """
    Описывает текущую комнату игрока
    """
    from .constants import ROOMS
    
    current_room_name = game_state['current_room']
    room_data = ROOMS.get(current_room_name, {})
    
    # Вывод названия комнаты в верхнем регистре
    print(f"\n== {current_room_name.upper()} ==")
    
    # Вывод описания комнаты
    description = room_data.get('description', 'Неизвестная комната.')
    print(description)
    
    # Вывод списка предметов
    items = room_data.get('items', [])
    if items:
        print("\nЗаметные предметы:", ", ".join(items))
    
    # Вывод доступных выходов
    exits = room_data.get('exits', {})
    if exits:
        print("\nВыходы:", ", ".join(exits.keys()))
    
    # Сообщение о наличии загадки
    puzzle = room_data.get('puzzle')
    if puzzle and not room_data.get('puzzle_solved', False):
        print("\nКажется, здесь есть загадка (используйте команду solve).")


def attempt_open_treasure(game_state):
    """
    Пытается открыть сундук с сокровищами
    """
    current_room = game_state['current_room']
    room_data = ROOMS.get(current_room, {})
    inventory = game_state.get('player_inventory', [])
    
    # Проверяем, находимся ли мы в комнате с сокровищами
    if 'treasure_chest' not in room_data.get('items', []):
        print("Здесь нет сундука с сокровищами.")
        return False
    
    # Проверка наличия ключа
    if 'treasure_key' in inventory:
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        
        # Удаляем сундук из комнаты
        room_data['items'].remove('treasure_chest')
        
        # Объявляем победу
        print("В сундуке сокровище! Вы победили!")
        game_state['game_over'] = True
        return True
    
    # Если ключа нет, предлагаем ввести код
    print("Сундук заперт. У вас нет ключа.")
    choice = input("Ввести код? (да/нет): ").strip().lower()
    
    if choice == 'да':
        # Получаем код от пользователя
        user_code = input("Введите код: ").strip()
        
        # Проверяем код (используем загадку из комнаты как код)
        puzzle = room_data.get('puzzle')
        if puzzle and user_code == puzzle[1]:  # puzzle[1] - правильный ответ
            print("Код верный! Сундук открыт!")
            
            # Удаляем сундук из комнаты
            room_data['items'].remove('treasure_chest')
            
            # Объявляем победу
            print("В сундуке сокровище! Вы победили!")
            game_state['game_over'] = True
            return True
        else:
            print("Неверный код. Сундук остается запертым.")
            return False
    else:
        print("Вы отступаете от сундука.")
        return False


def solve_puzzle(game_state):
    """
    Решает загадку в текущей комнате с улучшенной логикой
    """
    current_room = game_state['current_room']
    room_data = ROOMS.get(current_room, {})
    puzzle = room_data.get('puzzle')
    
    # Проверяем, есть ли загадка в комнате
    if not puzzle:
        print("Загадок здесь нет.")
        return False
    
    # Проверяем, не решена ли уже загадка
    if room_data.get('puzzle_solved', False):
        print("Вы уже решили загадку в этой комнате.")
        return True
    
    # Выводим вопрос загадки
    question, correct_answer = puzzle
    print(f"💡 Загадка: {question}")
    
    # Получаем ответ от пользователя
    user_answer = input("Ваш ответ: ").strip().lower()
    
    # Проверяем альтернативные варианты ответов
    correct_answers = [correct_answer.lower()]
    if current_room in PUZZLES and len(PUZZLES[current_room]) > 1:
        correct_answers.extend(PUZZLES[current_room][1:])
    
    # Сравниваем ответ с правильным
    if user_answer in correct_answers:
        print("✅ Правильно! Загадка решена!")
        
        # Помечаем загадку как решенную
        room_data['puzzle_solved'] = True
        
        # Добавляем награду игроку
        reward = room_data.get('reward')
        if reward:
            if 'player_inventory' not in game_state:
                game_state['player_inventory'] = []
            game_state['player_inventory'].append(reward)
            print(f"🎁 Вы получили награду: {reward}")
        
        return True
    else:
        print("❌ Неверно. Попробуйте снова.")
        # В trap_room неверный ответ активирует ловушку
        if current_room == 'trap_room':
            trigger_trap(game_state)
        return False


# Дополнительные константы для красивой справки
COMMANDS_HELP = {
    "north/south/east/west": "перейти в направлении",
    "go <direction>": "перейти в направлении",
    "look": "осмотреть текущую комнату",
    "take <item>": "поднять предмет",
    "use <item>": "использовать предмет",
    "inventory": "показать инвентарь",
    "solve": "решить загадку",
    "quit": "выйти из игры",
    "help": "показать это сообщение"
}