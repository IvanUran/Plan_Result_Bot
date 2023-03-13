import logging
from time import sleep
import datetime
import telebot
from aiogram import Bot, Dispatcher, executor, types
from Keyboards import choose_fighter_reply, yes_no_inline, plan_inline4
from Addition_func import attributes_receiving_message, attributes_receiving_call, \
    plan_change, feelings_motivation_sleep_handler, chart_create, mode_of_plan_handler
from File_check_functions import plan_write_check, mode_of_plan_check, keyb_check, num_of_do_check, statistics_check

token = Впишите токен
bot_telebot = telebot.TeleBot(token)
bot_main = Bot(token)
# mode_of_plan_check(username, "w", text="None")
usernames_with_indices = {}  # Словарь, содержащий имена пользователей, что будут содержать в себе списки, в которых через пробел: энергия, мотивация, количество сна, дата

dispatcher = Dispatcher(bot_main)


@dispatcher.message_handler(content_types=['text'])
async def main_function(message):
    global usernames_with_indices
    add_text = ""
    plan_inline = None
    send_mes = False
    # print(message)
    mes_text, username, from_chat, message_id, plan, plan_lines = attributes_receiving_message(message)

    if not username in usernames_with_indices:
        usernames_with_indices[username] = ""
    if username == None: username = "None"  # Когда у пользователя нет своего id, возникает тонна ошибок, это их исправление
    print(f'Новое сообщение({message_id}) в', message.date, f'с текстом "{mes_text}" от {username, type(username)} из чата', from_chat)
    if mes_text == 'ПЛАН':
        plan_write_check(username, "w", "False")
        mode_of_plan_check(username, "w", text="None")
    plan_write = plan_write_check(username, "r")
    if plan_write:
        try:
            await bot_main.delete_message(from_chat, message_id - 1)
            await bot_main.delete_message(from_chat, message_id)
            send_mes = True
        except Exception as ex:
            print(f"Произошёл {ex} у плана")
    mode_of_plan = mode_of_plan_check(username, "r")
    if mode_of_plan != "None":
        usernames_with_indices, plan, send_mes, plan_inline, add_text = await mode_of_plan_handler(bot_main, message, mode_of_plan, usernames_with_indices)

    # =======================БЛОК====ПРОВЕРКИ====ТЕКСТА====СООБЩЕНИЙ==================================================================

    if mes_text == "Мои показатели":
        response = chart_create(username)
        if response == None:
            await bot_main.send_message(chat_id=from_chat, text="У тебя нет никаких показателей, ты ещё не написал ни одного плана")
        else:
            await bot_main.send_photo(chat_id=from_chat, photo=open(f'vars/{username}/statistics.png', "rb"), caption="@" + username)
    if mes_text == "/start" or mes_text == "/start@Plan_Result_Bot":
        await bot_main.send_message(chat_id=from_chat, text="Выбери своего 🗡бойца🛡️️", reply_markup=choose_fighter_reply)
    if mes_text == "ИТОГ(не нажимай на меня)":
        await bot_main.send_message(chat_id=from_chat, text="А вот не сделаю я тебе итог, а что ты хотел, чуда какого-нибудь? Ещё не готово, довольствуйся планом")
    if mes_text == "ПЛАН":
        num_of_do_check(username, "w", 0)
        keyb_check(username, "w", "1")
        plan_write_check(username, "w", True)
        now = datetime.datetime.now()

        mode_of_plan_check(username, "w", text="feelings")
        if username is None:
            username = "None"
        if username == "None":
            addd_text = "(рекомендую поставить себе имя во избежание багов)"
        else:
            addd_text = ""
        plan = f"*#пландня @{username + addd_text}* от `{now.strftime('%d.%m_%H:%M')}`"
        plan_inline = None
        await bot_main.send_messёage(chat_id=from_chat, text=plan, reply_markup=plan_inline, parse_mode="Markdown")
        await bot_main.send_message(chat_id=from_chat, text="Как себя чувствуешь(от 1 до 100)?")
        send_mes = False

    if send_mes:
        if plan_inline == None:
            await bot_main.send_message(chat_id=from_chat, text=plan, parse_mode="Markdown")
        elif plan_inline != None:
            await bot_main.send_message(chat_id=from_chat, text=plan, reply_markup=plan_inline, parse_mode="Markdown")
    if add_text != "":
        await bot_main.send_message(chat_id=from_chat, text=add_text)

    with open(f'vars/{username}/plan.txt', 'w') as f:
        f.write(str(plan))


@dispatcher.callback_query_handler(lambda callback_query: True)
async def osnova_callback(call: types.CallbackQuery):
    global usernames_with_indices

    # print(call)
    mes_text, username, from_chat, message_id, plan = attributes_receiving_call(call)
    foo = mes_text[:20].replace("\n", "\\n")
    print(f'Новый запрос с текстом "{foo}..." от {username} из чата', from_chat)

    if call.data == 'complete':
        await bot_main.send_message(chat_id=from_chat, text="Ты уверен, что готов закончить план?", reply_markup=yes_no_inline)
    if call.data == 'yes' or call.data == 'no' or call.data == 'del':
        await bot_main.delete_message(from_chat, message_id)
        await bot_main.delete_message(from_chat, message_id - 1)

        if call.data == 'yes':
            usernames_with_indices[username] += call.message.date.strftime("%d.%m.%Y") + "\n"
            statistics_check(username, "a", text=usernames_with_indices[username])
            plan_write_check(username, "w", False)
            mode_of_plan_check(username, "w", text="None")
            await bot_main.send_message(chat_id=from_chat, text=plan, parse_mode="Markdown")
        elif call.data == 'no':
            await bot_main.send_message(chat_id=from_chat, text=plan, reply_markup=keyb_check(username, "r"), parse_mode="Markdown")
        elif call.data == 'del':
            plan_write_check(username, "w", False)
            mode_of_plan_check(username, "w", text="None")

    await bot_main.answer_callback_query(call.id)


if __name__ == "__main__":
    executor.start_polling(dispatcher)
