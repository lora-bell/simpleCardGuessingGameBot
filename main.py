from telebot import TeleBot
from telebot import types
from random import choice
from config import TOKEN

'''
    Получить TOKEN можно в телеграмм-боте @BotFather
'''
TOKEN = TOKEN
COLOR_SUIT = {
    "♠": "⚫",  # black
    "♥": "🔴",  # red
    "♦": "🔴",  # red
    "♣": "⚫",  # black
}

# authorization
bot = TeleBot(TOKEN)
keyboard_finish = types.ReplyKeyboardMarkup().add(types.KeyboardButton("/start"))


# Welcome message
@bot.message_handler(commands=["start"])
def start(message):
    name = message.chat.first_name
    keyboard_start = types.ReplyKeyboardMarkup()  # клавиатура с кнопками
    keyboard_start.add(types.KeyboardButton("1⃣"))
    keyboard_start.add(types.KeyboardButton("2️⃣"))
    keyboard_start.add(types.KeyboardButton("3️⃣"))

    bot.send_message(
        message.chat.id,
        f"{name}, начнем игру!\nВыбери уровень сложности игры: \n"
        "1⃣ уровень: угадать цвет масти\n"
        "2️⃣ уровень: угадать масть карты\n"
        "3️⃣ уровень: угадать карту\n",
        reply_markup=keyboard_start)  # вернуть клавиатуру с кнопками выбора

    bot.register_next_step_handler(message, answer_level)


def generate_card():
    card_number = choice(["2", "3", "4", "5", "6", "7", "8", "9", "10", "Валет", "Дама", "Король", "Туз"])
    card_suit = choice(["♠", "♥", "♦", "♣"])
    return card_number, card_suit


def answer_level(message):
    card_number, card_suit = generate_card()

    if message.text in ["1⃣", "2️⃣", "3️⃣"]:
        if message.text == "1⃣":
            keyboard_level_1 = types.ReplyKeyboardMarkup().add(
                types.KeyboardButton("⚫"),  # black
                types.KeyboardButton("🔴")  # red
            )

            bot.send_message(
                message.chat.id,
                "Я загадал карту, а ты попробуй угадать какого цвета масть загаданной карты:\n ⚫ черная \n 🔴 красная ? \n",
                reply_markup=keyboard_level_1)

            bot.register_next_step_handler(message, answer_card_level_1, card_number, card_suit)

        elif message.text == "2️⃣":
            keyboard_level_2 = types.ReplyKeyboardMarkup()
            keyboard_level_2.add(types.KeyboardButton("♠"))  # пики
            keyboard_level_2.add(types.KeyboardButton("♣"))  # трефы
            keyboard_level_2.add(types.KeyboardButton("♦"))  # бубны
            keyboard_level_2.add(types.KeyboardButton("♥"))  # червы

            bot.send_message(
                message.chat.id,
                "Я загадал карту, а ты попробуй угадать ее масть:\n ♠ пики \n ♣ трефы\n ♦ бубны\n ♥ червы? \n",
                reply_markup=keyboard_level_2)

            bot.register_next_step_handler(message, answer_card_level_2, card_number, card_suit)

        else:
            buttons = ["Валет", "Дама", "Король", "Туз"]
            keyboard_level_3 = types.ReplyKeyboardMarkup().row("2", "3", "4", "5", "6", "7", "8", "9", "10")
            for button in buttons:
                keyboard_level_3.add(button)

            bot.send_message(
                message.chat.id,
                "Я загадал карту, а тебе надо её угадать. \nКакое значение карты ты выбираешь? \n(в ответе должна быть цифра от 2 до 10 или одно из значений: Валет, Дама, Король или Туз)",
                reply_markup=keyboard_level_3
            )

            bot.register_next_step_handler(message, answer_card_level_3, card_number, card_suit)

    else:
        bot.send_message(
            message.chat.id,
            "Такого уровня пока нет в игре. \nЕсли хочешь попробовать еще раз, то отправь /start")


def answer_card_level_1(message, card_number, card_suit):
    card_color = COLOR_SUIT[card_suit]
    answer_card = f"Я загадал карту: {card_number} {card_suit}\n"
    answer_start = "Если хочешь попробовать еще раз, то отправь /start"

    if message.text not in ["⚫", "🔴"]:
        answer = f"Масти такого цвета не существует. Масть загаданной карты {card_color}.\n" + answer_card + answer_start
    elif message.text == card_color:
        answer = "Ты угадал!\n" + answer_card + f"У нее {card_color} масть\n" + answer_start
    else:
        answer = "К сожалению, ты не угадал!\n" + answer_card + f"У нее {card_color} масть\n" + answer_start

    bot.send_message(message.chat.id, answer, reply_markup=keyboard_finish)


def answer_card_level_2(message, card_number, card_suit):
    answer_card = f"Я загадал карту: {card_number} {card_suit}\n"
    answer_start = "Если хочешь попробовать еще раз, то отправь /start"

    if message.text not in ["♠", "♣", "♦", "♥"]:
        answer = "Такой масти не существует.\n" + answer_card + answer_start
    else:
        if message.text == card_suit:
            answer = "Ты угадал! " + answer_card + answer_start
        else:
            answer = "К сожалению, ты не угадал!\n" + answer_card + answer_start

    bot.send_message(message.chat.id, answer, reply_markup=keyboard_finish)


def answer_card_level_3(message, card_number, card_suit, player_card=None):
    answer_card = f"Я загадал карту: {card_number} {card_suit}\n"
    answer_start = "Если хочешь попробовать еще раз, то отправь /start"

    if player_card is None:
        player_card = message.text
        buttons = ["♠", "♣", "♦", "♥"]
        keyboard_card_suit = types.ReplyKeyboardMarkup()
        for button in buttons:
            keyboard_card_suit.add(button)

        bot.send_message(
            message.chat.id,
            "Какой масти загаданная карта:\n ♠ пики \n ♣ трефы\n ♦ бубны\n ♥ червы? \n",
            reply_markup=keyboard_card_suit)

        bot.register_next_step_handler(message, answer_card_level_3, card_number, card_suit, player_card)

    else:
        player_suit = message.text

        if all([player_card.lower() == card_number.lower(),
                player_suit.lower() == card_suit]):
            answer = "Ты угадал карту полностью!\n"
        elif any([player_card.lower() == card_number.lower(),
                  player_suit.lower() == card_suit]):
            answer = f"Ты угадал карту частично - "
            if player_card.lower() == card_number.lower():
                answer += "только ее значение.\n"
            else:
                answer += "только ее масть.\n"
        else:
            answer = "К сожалению, ты не угадал мою карту!\n"

        answer += answer_card + answer_start
        bot.send_message(message.chat.id, answer, reply_markup=keyboard_finish)


bot.infinity_polling()
