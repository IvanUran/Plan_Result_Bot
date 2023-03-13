"""
В этом файле производится обращение ко всем файлам с долговременными переменными, новые переменные добавлять сюда.
"""


from Keyboards import plan_inline1, plan_inline2, plan_inline3, plan_inline4

def plan_write_check(username, mode, text=False):
    """Если mode = 'w', записывает в переменную plan_write_check переменную text, если mode = 'r', выводит значение этой переменной"""
    return file_check(f'vars/{str(username)}/plan_write.txt', mode, bool, text)


def mode_of_plan_check(username, mode, text=""):
    """Если mode = 'w', записывает в переменную mode_of_plan переменную text, если mode = 'r', выводит значение этой переменной"""
    return file_check(f'vars/{str(username)}/mode_of_plan.txt', mode, str, text)


def num_of_do_check(username, mode, text=""):
    """Если mode = 'w', записывает в переменную num_of_do переменную text, если mode = 'r', выводит значение этой переменной"""
    return file_check(f'vars/{str(username)}/num_of_do.txt', mode, int, text)


def keyb_check(username, mode, text=""):
    """Если mode = 'w', записывает в переменную mode_of_plan переменную text, если mode = 'r', выводит значение этой переменной"""
    response = file_check(f'vars/{str(username)}/keyb.txt', mode, int, text)
    if mode == "r":
        if response == 1:
            return plan_inline1
        elif response == 2:
            return plan_inline2
        elif response == 3:
            return plan_inline3
        elif response == 4:
            return plan_inline4


def statistics_check(username, mode, text=""):
    """Если mode = 'a', добавляет в переменную statistics переменную text(если такого файла ещё нет, то создаёт его), если mode = 'r', выводит значение этой переменной"""
    response = file_check(f'vars/{str(username)}/statistics.txt', mode, str, text)
    if response == "": return ""
    if mode == "r":
        feelings_list, motivation_list, sleep_list, date_list = [], [], [], []
        days = response.split('\n')
        for i in range(len(days)-1):
            # Здесь стоит len(days)-1 потому что последний элемент всегда пустой, так как в конце файла стоит символ новой строки
            foo_list = days[i].split(" ")  # Временный список, нужный только для того, чтобы заполнить необходимые 4 списка
            feelings_list.append(int(foo_list[0]))
            motivation_list.append(int(foo_list[1]))
            sleep_list.append(float(foo_list[2]))
            date_list.append(foo_list[3])
        return feelings_list, motivation_list, sleep_list, date_list


# ====STANDARD====FILES==========================STANDARD====FILES===============================STANDARD====FILES====================================STANDARD====FILES=============


def var_create(filename):
    with open(filename, 'w') as f:
        f.write("")


def file_check(filename, mode_of_handle, type_of_return, text):
    """
    Функция обрабатывает файл, либо записывая в него данные, либо возвращая его содержимое.
    Условные обозначения: (О) - обязательный аргумент, (нО) - необязательный аргумент

    :param filename: (О) имя файла с которым будут производиться манипуляции.
    :param mode_of_handle: (О) может принимать значения:
     'w' - записывает в переменную filename переменную text;
      'r', выводит значение этой переменной в формате, который выбирается в следующей переменной.
    :param type_of_return: (нО) режим вывода данных, может принимать значения типа str, int, bool, в каждом из выбранных вариантов выводит соответствующий тип данных
     работает только при выборе 'r' в mode_of_handle
    :param text: (нО) текст, который будет записан в файл при выборе 'w' в mode_of_handle
    """
    if mode_of_handle == 'r':
        try:
            with open(filename, 'r') as f:
                text_return = f.read()
        except:
            print(f"ФАЙЛ '{filename}' ОТСУТСТВУЕТ, СОЗДАЮ С БАЗОВЫМ ЗНАЧЕНИЕМ ПУСТОТЫ")
            var_create(filename)
            text_return = ""
        if type_of_return == bool:
            if text_return == "False":
                return False
            elif text_return == "True":
                return True
        elif type_of_return == str:
            return text_return
        elif type_of_return == int:
            return int(text_return)
        elif text_return == "":
            return ""
    elif mode_of_handle == 'w':
        with open(filename, 'w') as f:
            f.write(str(text))
    elif mode_of_handle == 'a':
        try:
            with open(filename, 'a') as f:
                f.write(str(text))
        except FileNotFoundError:
            print("FILE NOT FOUND ERROR")
            with open(filename, 'w') as f:
                f.write(str(text))
