from telebot import types
import telebot
import random
import json

from menus import goto_menu

try:
    from loadconfig import __telegramtoken__
except ImportError:
    exit('set __telegramtoken__ ')

bot = telebot.TeleBot(__telegramtoken__)

players = []
# Список с активными игроками
class HangM:


    ID = 0
    HP = 1
    WORD = 2
    GUESS = 3
    LETTERS = 4
    THEME = 5

    CATEGORIES_PATH = 'JSON/categories.json'
    categories_words = ["Животные", "Еда", "Дом", "Одежда", "Школа", "Музыка", "Тело", "Спорт", "Компьютер", "Природа", "Профессии"]

    ABC = 'А Б В Г Д Е Ж З И Й К Л М Н О П Р С Т У Ф Х Ц Ч Ш Щ Ъ Ы Ь Э Ю Я'.split()

    def new_player(self, message, word, theme):
        if self.player_founder(message)[self.HP] == 0:
            players.remove(self.player_founder(message)) #ID

            hp = 6
            guess = []
            letters = list(self.ABC)

            for i in range(0, len(word)):
                if not word[i] == '_':
                    guess.append("_")
                else:
                    guess.append(" ")
                    word[i] = ' '

            # blanks = ''.join('_' if c.isalpha() else ch for ch in word)
            # blanks = re.sub('[A-Za-z]', '_', word)

            player = [message.chat.id, hp, word, guess, letters, theme]
            # ID - 0, HP - 1, WORD - 2, GUESS - 3, LETTERS - 4
            bot.send_message(message.chat.id, "Тема: " + theme)

            players.append(player)

        else:
            bot.send_message(message.chat.id, 'Игра уже идёт, 🚫 - выход')
            bot.send_message(message.chat.id, "Тема: " + self.player_founder(message)[5])
        self.letters_buttons(message)

    # Найти игрока по ID
    def player_founder(self, message):
        while True:
            for player in players:
                if player[self.ID] == message.chat.id:
                    return player
            players.append([message.chat.id, 0, [], [], []])


    def hp_visual(self, message):
        hp = self.player_founder(message)[self.HP]
        if hp > 0:
            with open('JSON/categories.json', "r", encoding="utf8") as read:
                if hp == 6:
                    bot.send_message(message.chat.id, json.load(read)["FIRST_POSITION"])
                elif hp == 5:
                    bot.send_message(message.chat.id, json.load(read)["SECOND_POSITION"])
                elif hp == 4:
                    bot.send_message(message.chat.id, json.load(read)["THIRD_POSITION"])
                elif hp == 3:
                    bot.send_message(message.chat.id, json.load(read)["FOURTH_POSITION"])
                elif hp == 2:
                    bot.send_message(message.chat.id, json.load(read)["FIFTH_POSITION"])
                elif hp == 1:
                    bot.send_message(message.chat.id, json.load(read)["SIXTH_POSITION"])

            tmp = []
            i = 1
            while i <= 6:
                tmp.append('[')
                if hp >= i:
                    tmp.append('❤️')
                else:
                    tmp.append('🖤')
                tmp.append('] ')
                i += 1
            bot.send_message(message.chat.id, ''.join(tmp))

    # клавиатура для игры
    def letters_buttons(self, message):
        # Готовим клавиатуру
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=5)
        # Список кнопок
        buttons_added = ["Выбрать букву"]
        # И добавляем в неё кнопки
        # for letter in self.player_founder(message)[self.LETTERS]:
        #     tmp = types.KeyboardButton(letter)
        #     buttons_added.append(tmp)
        keyboard.add(*buttons_added, types.KeyboardButton("🚫️"))
        self.hp_visual(message)
        if not buttons_added == []:
            bot.send_message(message.chat.id, ' '.join(self.player_founder(message)[self.GUESS]), reply_markup=keyboard)

    def guess_changer(self, message):
        tmp_player = self.player_founder(message)
        for i in range(0, len(tmp_player[self.WORD])):
            if message.text == tmp_player[self.WORD][i]:
                tmp_player[self.GUESS][i] = message.text


hm = HangM()
# Обработчик сообщений


def get_text_messages(tg, message):
        ABC = 'А Б В Г Д Е Ж З И Й К Л М Н О П Р С Т У Ф Х Ц Ч Ш Щ Ъ Ы Ь Э Ю Я'.split()
        letters = list(ABC)
        if message.text == "Играть" or message.text == "играть" or message.text == "/play":
            if hm.player_founder(message)[hm.HP] == 0:
                players.remove(hm.player_founder(message))
                # Создаём кнопки
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=5)
                # Кнопки с категориями
                keyboard.add(*hm.categories_words)
                tg.send_message(message.chat.id, 'Выбери категорию: ', reply_markup=keyboard)
            else:
                tg.send_message(message.chat.id, 'Игра уже идёт, 🚫 - выход')
                tg.send_message(message.chat.id, "Тема: " + hm.player_founder(message)[hm.THEME])
                hm.letters_buttons(message)

        elif message.text in hm.categories_words:
            with open(hm.CATEGORIES_PATH, "r", encoding="utf8") as read:
                word = list(random.choice(json.load(read)[message.text][0]))
                hm.new_player(message, word, message.text)

        elif message.text in hm.player_founder(message)[hm.LETTERS]:
            # Находи нашего игрока в списке players
            tmp_player = hm.player_founder(message)
            # Удалить букву-кнопку
            tmp_player[hm.LETTERS].remove(message.text)
            # Если игрок угадал
            if message.text in tmp_player[hm.WORD]:
                hm.guess_changer(message)
                if tmp_player[hm.WORD] == tmp_player[hm.GUESS]:
                    keyboard = types.ReplyKeyboardRemove()
                    bot.send_message(message.chat.id, 'Ты выиграл 🥳', reply_markup=keyboard)
                    bot.send_message(message.chat.id, 'Правильное слово - ' + ''.join(tmp_player[hm.WORD]))
                    players.remove(tmp_player)
                else:
                    hm.letters_buttons(message)
            # Если игрок ошибся
            else:
                if tmp_player[hm.HP] <= 1:
                    keyboard = types.ReplyKeyboardRemove()
                    bot.send_message(message.chat.id, '💀')
                    bot.send_message(message.chat.id, 'Ты проиграл 😞', reply_markup=keyboard)
                    bot.send_message(message.chat.id, 'Правильное слово - ' + ''.join(tmp_player[hm.WORD]))
                    players.remove(tmp_player)
                else:
                    tmp_player[hm.HP] -= 1
                    hm.letters_buttons(message)

        elif message.text == "🚫️":
            # Убираем клавиатуру
            goto_menu(bot, message.chat.id, "Главное меню")
            players.remove(hm.player_founder(message))
            return
        else:
            print(message.text)
