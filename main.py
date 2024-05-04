"""
Игра крестики/нолики.
3 на 3.
1. отображение состояние игры

1 __|__|__
2 __|__|__
3   |  |
  1  2  3

2. хранение состояние игры  
2-й массив: 3 строки и 3 столбца

3. два игрока: человек и компьютер(ПК)
   у человека спрашиваем координаты ячейки: 
   компьтера сам выбирает ячейку: случайным образом из свободных

4. выбор кто начинает игру: человек или ПК
5. после завершение игры спрашивать: выход или продолжить. 
6. после каждого шага проверять конец игры или нет
7. сделать статистика по игрокам

8. поиск опасной ячейки
9. сделать более умный ход, если нет опасной ячейки
10. попытка завершить игру, когда у ПК уже есть две ячейки

"""
import random

rows = 3  # количество строк
cols = rows  # количество столбцов

select_player = False  # F = человеке T = ПК

# заполнение ячейки
user_code = "x"
pc_code = "o"
free_code = " "

# Статистика ика игры
# кол-во игр
games = 0
# кол-во побед человека
games_user_win = 0
# количество ничьих
games_draw = 0

game_array = None


# Хранилище состояние ячеек(игры). Матрицы rows*cols

def create_array():
    """
    функция создания матрицы.
    :return:
    возращает новую матрицу
    """
    new_array = []

    for i in range(rows):
        col = []

        for j in range(cols):
            col.append(None)

        new_array.append(col)

    return new_array


def clear_array(code: str = free_code):
    """
    Очистка массива
    code: чем заполняем, а по умолчанию free_code
    """
    for row in range(rows):
        for col in range(cols):
            game_array[row][col] = code


def print_array():
    """
    вывод матрицы на экран.
    отабражаем на экране сетку и состояние ячеек.
    :return:
    """
    for row in range(rows):
        print(row + 1, end="")
        for col in range(cols):
            #print("___", end="|")
            print("_", end="")

            print(game_array[row][col], end="")

            print("_", end="|")

        print("")

    print(" ", end="")
    for col in range(cols):
        #print("___", end="|")
        print("_", end="")

        print(col + 1, end="")

        print("_", end="|")

    print("")
    print("")


def user_step():
    """
    Пользователь делает один шаг.
    :return:
    """
    while True:
        # 1.  начало цикла, ввод строки и столбца 
        print("введите координаты ячейки: строка столбец (2 3) ")
        data = input().split(sep=" ")
        row = int(data[0]) - 1
        col = int(data[1]) - 1

        # 2. проверка на правильность данных

        if row >= rows or row < 0 or col >= cols or col < 0:
            # 3. данные некорректы , переход в начало 1.
            print("Данные введены неккоректно!")
            continue

        # 4. шаг игрока: заполним ячейку
        if game_array[row][col] == free_code:
            game_array[row][col] = user_code

        # 5. выход
        break


def is_even(n) -> bool:
    """
    Определяет четное ли число
    """
    return n % 2 == 0


def is_odd(n) -> bool:
    """
    Определяет нечетное ли число
    :param n: число
    :return: True если нечетное, False если иначе
    """
    return n % 2 == 1


def test_center() -> bool:
    """
    проверяет ячейку по центру  и если она свободна тоделаем умный ход.
    :return:
    """
    if is_even(rows):
        return False
    # строка и столбей центральной ячейки 
    center = rows // 2

    # заполнена ли ячейка

    if game_array[center][center] != free_code:
        return False

    if count_cells(0, user_code) > 0:
        game_array[center][center] = pc_code
        return True

    if count_cells(rows - 1, user_code) > 0:
        game_array[center][center] = pc_code
        return True

    if count_cells_col(0, user_code) > 0:
        game_array[center][center] = pc_code
        return True

    if count_cells_col(cols - 1, user_code) > 0:
        game_array[center][center] = pc_code
        return True
    return False


def pc_step():
    """
    ПК делает свой ход.
    :return:
    """
    # 1 поиск завершения игры

    if find_danger(pc_code):
        # ячейка найдена и заполнена
        # т.е шаг сделан, выходим из функции
        return

    # 2 умная проверка, поиск опасной ячейки
    if find_danger(user_code):
        # ячейка найдена и заполнена
        # т.е шаг сделан, выходим из функции
        return
    # 3 умный ход кода есть 2 свободные и одна занятая: что бы на след-м ходу выиграть
    if find_danger(free_code, pc_code):
        # ячейка найдена и заполнена
        # т.е шаг сделан, выходим из функции
        return
    # проверка центральной ячейки
    if test_center():
        # если ее нашли и заполнили, то выходим из функции т.к. шаг сделан
        return

    # поиск  свободных ячеек.
    free_cells = []

    for row in range(rows):
        for col in range(cols):

            if game_array[row][col] == free_code:
                free_cells.append([row, col])

    if len(free_cells) >= 0:
        # из списка свободных ячеек выбираем случайным образом одну ячейку.
        free_index = random.randint(0, len(free_cells) - 1)

        data = free_cells[free_index]

        row = data[0]
        col = data[1]

        game_array[row][col] = pc_code


def get_select_player() -> bool:
    """
    Выбор первого игрока.
    # F = человек T = ПК

    """
    return input("Выберете кто начинает игру: 1 если ПК, иначе человек ") == "1"


def count_cells(row, code):
    """
    Подсчет занятых ячеек по по строке
    """

    counter = 0

    for col in range(cols):

        if game_array[row][col] == code:
            counter += 1
    return counter


def count_cells_col(col, code):
    """
    Подсчет занятых ячеек по столбцу
    """

    counter = 0

    for row in range(rows):

        if game_array[row][col] == code:
            counter += 1
    return counter


def count_cells_diag_1(code):
    """
    Подсчет занятых ячеек по диагонали
    """
    counter = 0

    for row in range(rows):

        if game_array[row][row] == code:
            counter += 1
    return counter


def count_cells_diag_2(code):
    """
    Подсчет занятых ячеек по диагонали*
    """
    counter = 0

    for row in range(rows):

        if game_array[row][cols - 1 - row] == code:
            counter += 1
    return counter


def is_free() -> bool:
    """
    Есть ли хотя бы одна свободная ячейка?

    """
    for row in range(rows):
        for col in range(cols):
            if game_array[row][col] == free_code:
                return True
    return False


def print_game_result(code):
    """
    Вывод результата игры
    """
    if code == 1:
        print("Ничья")
    elif code == 2:
        print("Вы выйграли")
    elif code == 3:
        print("Вы проиграли")


def get_game_result() -> int:
    """
    Результат игры:
    0 - не закончена
    1 - ничья
    2 - победитель человек
    3 - победитель ПК

    """

    # проверка по строкам

    for row in range(rows):

        counter = count_cells(row, user_code)

        if counter == cols:
            return 2

        counter = count_cells(row, pc_code)

        if counter == cols:
            return 3

    # проверка по столбцам
    for col in range(cols):

        counter = count_cells_col(col, user_code)

        if counter == cols:
            return 2

        counter = count_cells_col(col, pc_code)

        if counter == cols:
            return 3

    # проверка по диагоналям

    counter = count_cells_diag_1(user_code)
    if counter == cols:
        return 2
    counter = count_cells_diag_2(user_code)
    if counter == cols:
        return 2

    counter = count_cells_diag_1(pc_code)
    if counter == cols:
        return 3
    counter = count_cells_diag_2(pc_code)
    if counter == cols:
        return 3

    if is_free():
        return 0
    else:
        return 1


def continue_game() -> bool:
    """
    спрашиваем пользователя о продолжении игры.
    return: True - если играем новую игру, False - если завершаем
    """
    # получаем строку от пользователь и сохраняем в переменную
    string_from_user = input("Будем играть ещё или нет ? 1 если продолжить ")

    # если строка равно 'yes' то фукция должна вернуть True, иначе False

    return string_from_user == "1"


def print_statistic():
    """
    функция выводит кол-во игр, побед, ничьих.
    """
    print("кол-во игр         ", games)
    print("кол-во ничьих      ", games_draw)
    print("кол-во ваших побед ", games_user_win)


def set_first_for_row(row, code):
    """
    в указанной строке найти свободную ячейку и заполнить кодом
    """
    for col in range(cols):
        if game_array[row][col] == free_code:
            game_array[row][col] = code
            return


def set_first_for_col(col, code):
    """
    в указанном cтолбце найти свободную ячейку и заполнить кодом
    """
    for row in range(rows):
        if game_array[row][col] == free_code:
            game_array[row][col] = code
            return


def set_first_for_diag_1(code):
    """
    в указанной диагонали найти свободную ячейку и заполнить кодом
    """
    for row in range(rows):
        if game_array[row][row] == free_code:
            game_array[row][row] = code
            return


def set_first_for_diag_2(code):
    """
    в указанной  диагонали найти свободную ячейку и заполнить кодом
    """
    for row in range(rows):
        if game_array[row][rows - row - 1] == free_code:
            game_array[row][rows - row - 1] = code
            return


def find_danger(code_2: str = user_code, code_1: str = free_code) -> bool:
    """
    функция поиска строки где code_2 2 яч., code_1 заполнены 1 яч.
    если найдена то происходит заполнение пустой ячейки и функция возврат. true,
    иначе функция возврат. false
    #code_2: состояние двух ячеек: user_code, free_code или pc_code
    #code_1: состояние одной ячейки: free_code или pc_code
    """

    for i in range(rows):
        user_count = count_cells(i, code_2)
        free_count = count_cells(i, code_1)

        if user_count == 2 and free_count == 1:
            # заполняем свободую ячейку 
            set_first_for_row(i, pc_code)
            # и выходим из функции
            return True

    for i in range(cols):
        user_count = count_cells_col(i, code_2)
        free_count = count_cells_col(i, code_1)

        if user_count == 2 and free_count == 1:
            # заполняем свободую ячейку 
            set_first_for_col(i, pc_code)
            # и выходим из функции
            return True

    # поиск по 1 диагонали        
    user_count = count_cells_diag_1(code_2)
    free_count = count_cells_diag_1(code_1)

    if user_count == 2 and free_count == 1:
        # заполняем свободую ячейку 
        set_first_for_diag_1(pc_code)
        # и выходим из функции
        return True

        # поиск по 2 диагонали

    user_count = count_cells_diag_2(code_2)
    free_count = count_cells_diag_2(code_1)

    if user_count == 2 and free_count == 1:
        # заполняем свободую ячейку 
        set_first_for_diag_2(pc_code)
        # и выходим из функции
        return True

    return False

# начало игры. создание хранилища.
game_array = create_array()
clear_array()
print_array()

# выбор первого игрока
select_player = get_select_player()
games += 1

# игра продолжается пока мы не выйдем.
while True:

    # получение результата игры
    result = get_game_result()

    if result == 0:
        # игра продолжается

        if select_player:
            pc_step()
            print_array()
        else:
            user_step()
            print_array()

        # следующий шаг у другого игрока
        select_player = not select_player

    else:

        # игра завершена

        print_game_result(result)

        # обновляем статистику игр

        if result == 1:
            games_draw += 1
        elif result == 2:
            games_user_win += 1

        # выводим на экран статистику игр
        print_statistic()

        # cпрашиваем пользователя о продолжении игры

        if not continue_game():
            # выход из игры
            break

        # начинаем новую игру

        select_player = get_select_player()

        clear_array()
        print_array()
        games += 1
