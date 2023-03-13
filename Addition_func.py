"""
Здесь хранятся все функции обработки, то есть почти весь background.
"""

import os.path
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from Keyboards import plan_inline4
from File_check_functions import var_create, statistics_check, mode_of_plan_check, num_of_do_check, keyb_check


def attributes_receiving_message(message):
    """Получает на входе message, а возвращает id основного чата, текст полученного сообщения, имя пользователя, id чата из которого было получено сообщение,
     id сообщения и значение переменной plan соответственно"""
    username = message["from"].username
    if not os.path.exists("vars/"+str(username)):
        os.mkdir("vars/"+str(username))
    from_chat = message.chat.id
    mes_text = message.text
    message_id = message.message_id
    try:
        with open(f'vars/{str(username)}/plan.txt', 'r') as f:
            plan = f.read()
    except FileNotFoundError:
        var_create(f'vars/{str(username)}/plan.txt')
        with open(f'vars/{str(username)}/plan.txt', 'r') as f:
            plan = f.read()
    with open(f'vars/{str(username)}/plan.txt', 'r') as f:
        plan_lines = f.readlines()
    return mes_text, str(username), from_chat, message_id, plan, plan_lines


def attributes_receiving_call(call):
    """Получает на входе message, а возвращает id основного чата, текст полученного сообщения, имя пользователя, id чата из которого было получено сообщение,
     id сообщения и значение переменной plan соответственно"""
    username = call["from"].username
    from_chat = call.message.chat.id
    mes_text = call.message.text
    message_id = call.message.message_id

    try:
        with open(f'vars/{str(username)}/plan.txt', 'r') as f:
            plan = f.read()
    except FileNotFoundError:
        var_create(f'vars/{str(username)}/plan.txt')
        with open(f'vars/{str(username)}/plan.txt', 'r') as f:
            plan = f.read()
    return mes_text, str(username), from_chat, message_id, plan


def chart_create(username):
    try:
        feelings_list, motivation_list, sleep_list, date_list = statistics_check(username, "r")
    except ValueError:
        return None
    # define colors to use
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
    col_health = colors[2]
    col_motivation = colors[3]
    col_sleep = colors[9]

    dates = []
    for d in date_list:
        dates.append(dt.datetime.strptime(d, '%d.%m.%Y').date())

    plt.rcParams['figure.figsize'] = [12, 7]
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%Y'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    ax1.plot(dates, feelings_list, label="Самочувствие", color=col_health)
    ax1.plot(dates, motivation_list, label="Мотивация", color=col_motivation)
    ax2.plot(dates, sleep_list, label="Часы сна", color=col_sleep)

    # Некоторые важные настройки графика для красоты отображения
    plt.gcf().autofmt_xdate()
    location = ['upper right', 'upper left', 'lower left',
                'lower right', 'right', 'center left',
                'center right', 'lower center', 'upper center', 'center']  # Список с возможными расположениями легенды
    plt.title("График показателей " + username, fontsize=30)
    ax1.legend(loc=location[2], shadow=True), ax2.legend(loc=location[3], shadow=True)  # Настраиваем легенды
    ax1.set_xlabel('Дата', fontsize=16), ax1.set_ylabel('Самочувствие и Мотивация', fontsize=12), ax2.set_ylabel('Часы сна', fontsize=16)  # Подписываем все оси
    ax1.minorticks_on(), ax2.minorticks_on()  # Включаем дополнительные отметки на осях для ax1 и ax2
    ax1.grid(which='major')  # линии основной сетки для ax1
    ax1.grid(which='minor', linestyle=':')  # включаем дополнительную сетку
    plt.tight_layout()  # оптимизируем поля и расположение объектов
    plt.savefig(fname=f'vars/{username}/statistics.png', format='png')  # Сохранение в файл statistics

    plt.close()
    return ""


def feelings_motivation_sleep_handler(usernames_with_indices, username, mes_text, mes_text_processed, text_to_mode, text_to_plan_change, position_to_plan_change, plan_lines):
    """
    Функция, которая делает общие действия для feelings, motivation и sleep. А именно:
        1) Добавляет в список под индексом username в словаре usernames_with_indices обработанный заранее mes_text_processed;
        2) Записывает в mode_of_plan text_to_mode;
        3) Выполняет функцию plan_change(подробнее о том, что она делать смотри в самой функции);
        4) Возвращает все полученные в результате работы функции переменные.
    """
    usernames_with_indices[username] += str(mes_text_processed) + " "
    mode_of_plan_check(username, "w", text=text_to_mode)
    plan, send_mes, plan_inline = plan_change(text_to_plan_change, position_to_plan_change, username, plan_lines, mes_text)
    return usernames_with_indices, plan, send_mes, plan_inline


def plan_change(text, position, username, plan_lines, mes_text):
    """
    Функция высчитывает обновлённый текст плана с учётом входных данных. Также определяет клавиатуру(или её отсутствие), с которой будет отправлено обновлённое сообщение плана.
    Все аргументы обязательны.

    :param str text: Текст, который надо будет добавить к плану.
    :param int position: Позиция в списке plan_lines, в которую будет добавлен text.
    :param str username: Текущий пользователь.
    :param list plan_lines: План построчно в виде списка.
    :param list mes_text: Текст полученного сообщения.

    :return: plan - полный текст обновлённого плана.
     send_mes - переменная, обозначающая, что необходимо отправить обновлённое сообщение плана, всегда True.
      plan_inline - Inline-клавиатура, с которой будет отправлено обновлённое сообщение плана(может принимать значение None).
    """
    mode_of_plan = mode_of_plan_check(username, "r")
    send_mes = True
    additional_text = ""
    # mode_of_plan_check(username, "w", text="None")
    if position == -1:
        position = len(plan_lines)
        num_of_do = num_of_do_check(username, "r") + 1
        text = f"{num_of_do}) "
        num_of_do_check(username, "w", num_of_do)
    elif position == 1:
        text = "\n" + text
    elif position == 3:
        additional_text = "_Буду делать:_\n"

    plan_lines.insert(position, text + mes_text + " \n" + additional_text)
    plan = ""
    for i in range(len(plan_lines)):
        plan += plan_lines[i]

    plan_inline = None
    if mode_of_plan == "feelings":
        keyb_check(username, "w", "2")
    elif mode_of_plan == "motivation":
        keyb_check(username, "w", "3")
    elif mode_of_plan == "sleep":
        keyb_check(username, "w", "4")
    elif mode_of_plan == "do":
        keyb_check(username, "w", "4")
        plan_inline = plan_inline4

    return plan, send_mes, plan_inline


async def mode_of_plan_handler(bot_main, message, mode_of_plan, usernames_with_indices):
    """В случае, если mode_of_plan не равно None, мы получаем """
    mes_text, username, from_chat, message_id, plan, plan_lines = attributes_receiving_message(message)
    add_text = ""
    if mode_of_plan != "do":
        try:
            await bot_main.delete_message(from_chat, message_id - 2)
        except Exception as ex:
            print(f"Произошёл {ex} у режима")

        try:
            mes_text_processed = mes_text.replace(",", ".")
            float(mes_text_processed)
            mes_text_not_number = False
        except ValueError:
            mes_text_not_number = True
            await bot_main.send_message(chat_id=from_chat, text="Отправь число")  # TODO опять же, из-за ошибки под номером 1 всё может перестать работать
    if mode_of_plan == "feelings":
        if not mes_text_not_number:
            mes_text_processed = int(mes_text_processed)
            code, text, number = "motivation", "_Как себя чувствую:_  ", 1
        add_text = "Как оцениваешь свою мотивацию(от 1 до 100)?"
    elif mode_of_plan == "motivation":
        if not mes_text_not_number:
            mes_text_processed = int(mes_text_processed)
            code, text, number = "sleep", "_Моя мотивацию:_  ", 2
        add_text = "Сколько сегодня спал?(целое число или десятичное число)"
    elif mode_of_plan == "sleep":
        if not mes_text_not_number:
            mes_text_processed = float(mes_text_processed)
            code, text, number = "do", "_Сегодня спал:_  ", 3
    elif mode_of_plan == "do":
        plan, send_mes, plan_inline = plan_change("", -1, username, plan_lines, mes_text)
    if mode_of_plan == "feelings" or mode_of_plan == "motivation" or mode_of_plan == "sleep":
        usernames_with_indices, plan, send_mes, plan_inline = \
            feelings_motivation_sleep_handler(usernames_with_indices, username, mes_text, mes_text_processed, code, text, number, plan_lines)
    return usernames_with_indices, plan, send_mes, plan_inline, add_text
