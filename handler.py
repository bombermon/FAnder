from telegram import ReplyKeyboardMarkup, KeyboardButton, Bot, Update
from validator import Validator
import logging
import random


class Handler:
    def __init__(self, lang):
        self.lang = lang
        self.valr = Validator()
        self.logger = logging.getLogger(__name__)
        self.markup = {
            'sexChoice_user': ReplyKeyboardMarkup([[KeyboardButton(self.lang['man']),
                                              KeyboardButton(self.lang['woman'])]],
                                             resize_keyboard=True, one_time_keyboard=True),
            'sexChoice': ReplyKeyboardMarkup([[KeyboardButton(self.lang['man']),
                                               KeyboardButton(self.lang['woman'])],
                                              [KeyboardButton(self.lang['friends'])]],
                                             resize_keyboard=True, one_time_keyboard=True),
            'markChoice': ReplyKeyboardMarkup(
                [[KeyboardButton(self.lang['like']), KeyboardButton(self.lang['dislike'])], [KeyboardButton(self.lang['go_menu'])]],
                row_width=2, resize_keyboard=True, one_time_keyboard=False),
            'mainMenu': ReplyKeyboardMarkup([[KeyboardButton(self.lang['menu_continue'])],
                                             [KeyboardButton(self.lang['menu_stop'])],
                                             [KeyboardButton(self.lang['menu_delete'])],
                                             [KeyboardButton(self.lang['menu_edit'])],
                                             [KeyboardButton(self.lang['menu_show'])]], resize_keyboard=True, one_time_keyboard=True),
            'frozenMenu': ReplyKeyboardMarkup([[KeyboardButton(self.lang['menu_continue'])],
                                             [KeyboardButton(self.lang['menu_delete'])],
                                             [KeyboardButton(self.lang['menu_edit'])],
                                             [KeyboardButton(self.lang['menu_show'])]], resize_keyboard=True, one_time_keyboard=True),
            'confirmReg': ReplyKeyboardMarkup(
                [[KeyboardButton(self.lang['confirm_reg'])],
                 [KeyboardButton(self.lang['repeat_reg'])]],
                resize_keyboard=True, one_time_keyboard=True),
            'continue': ReplyKeyboardMarkup(
                [[KeyboardButton(self.lang['menu_continue'])]],
                resize_keyboard=True, one_time_keyboard=False)
        }

    def getLang(self):
        return self.lang

    # Print next suitable account which we haven't rate
    def printNext(self, db, bot, update):
        uid = update.message.from_user.id
        cid = update.message.chat_id
        user = db.getUserByID(uid)
        for i in random.sample(range(0, len(db.getUsers())),len(db.getUsers())):
            if self.valr.checkPartner(user, db.getUsers()[i]):
                partner = db.getUsers()[i]
                db.updateUserData(uid, 'last_profile', partner['id'])
                bot.sendPhoto(cid, partner['photo'], reply_markup=self.markup['markChoice'],
                              caption=self.lang['account_info'] % (
                              partner['name'], partner['age'], partner['desc']), )
                return
        bot.sendMessage(cid, self.lang['no_partners'], reply_markup=self.markup['mainMenu'])

    def printMe(self, db, bot, update):
        uid = update.message.from_user.id
        cid = update.message.chat_id
        user = db.getUserByID(uid)
        bot.sendPhoto(cid, user['photo'],
                      caption=self.lang['account_info'] % (user['name'], user['age'], user['desc']),
                      reply_markup=self.markup['mainMenu'])

    def handle(self, db, bot, update):
        uid = update.message.from_user.id
        cid = update.message.chat_id
        user = db.getUserByID(uid)
        status = user['dialog_status']

        # Enter username
        if status == 'privacy_policy_acception':
            if update.message.text == self.lang["acception"]:
                db.updateUserData(uid, 'dialog_status', 'write_name')
                bot.sendMessage(cid, self.lang['greeting_new'], reply_markup=None)
            else:
                bot.sendMessage(cid, self.lang['not_understand'])
        elif status == 'write_name':
            if self.valr.validName(update.message.text):
                db.updateUserData(uid, 'name', str(update.message.text).strip())
                db.updateUserData(uid, 'dialog_status', 'write_age')
                bot.sendMessage(cid, self.lang['write_age'] % (update.message.text))
            else:
                bot.sendMessage(cid, self.lang['invalid_name'])

        # Enter age
        elif status == 'write_age':
            if self.valr.validAge(update.message.text):
                db.updateUserData(uid, 'age', int(update.message.text))
                db.updateUserData(uid, 'dialog_status', 'write_sex')
                bot.sendMessage(cid, self.lang['write_sex'], reply_markup=self.markup['sexChoice_user'])
            else:
                bot.sendMessage(cid, self.lang['invalid_age'])

        # Enter city
        elif status == 'write_city':
            db.updateUserData(uid, 'city', str(update.message.text))
            db.updateUserData(uid, 'dialog_status', 'write_sex')
            bot.sendMessage(cid, self.lang['write_sex'], reply_markup=self.markup['sexChoice_user'])

        # Choose gender
        elif status == 'write_sex':
            if update.message.text == self.lang['man']:
                db.updateUserData(uid, 'sex', 0)
            elif update.message.text == self.lang['woman']:
                db.updateUserData(uid, 'sex', 1)
            else:
                bot.sendMessage(cid, self.lang['incorrect_answer'])
                return
            db.updateUserData(uid, 'dialog_status', 'write_desc')
            bot.sendMessage(cid, self.lang['write_desc'], reply_markup=None)

        # Write description
        elif status == 'write_desc':
            db.updateUserData(uid, 'desc', str(update.message.text))
            db.updateUserDatalogger = logging.getLogger(__name__)
            db.updateUserData(uid, 'dialog_status', 'write_contact')
            bot.sendMessage(cid, self.lang['write_contact'])
        # Write contacts
        elif status == 'write_contact':
            db.updateUserData(uid, 'contact', str(update.message.text))
            db.updateUserData(uid, 'dialog_status', 'write_p_sex')
            bot.sendMessage(cid, self.lang['write_p_sex'], reply_markup=self.markup['sexChoice'])

        # Choose partner's gender
        elif status == 'write_p_sex':
            if update.message.text == self.lang['man']:
                db.updateUserData(uid, 'p_sex', 0)
            elif update.message.text == self.lang['woman']:
                db.updateUserData(uid, 'p_sex', 1)
            elif update.message.text == self.lang['friends']:
                db.updateUserData(uid, 'p_sex', 2)
            else:
                bot.sendMessage(cid, self.lang['incorrect_answer'])
                return
            db.updateUserData(uid, 'dialog_status', 'write_p_min_age')
            bot.sendMessage(cid, self.lang['write_p_min_age'], remove_keyboard=True)

        # Enter min partner's age
        elif status == 'write_p_min_age':
            if self.valr.validAge(update.message.text):
                db.updateUserData(uid, 'p_min_age', int(update.message.text))
                db.updateUserData(uid, 'dialog_status', 'write_p_max_age')
                bot.sendMessage(cid, self.lang['write_p_max_age'])
            else:
                bot.sendMessage(cid, self.lang['invalid_age'])

        # Enter max partner's age
        elif status == 'write_p_max_age':
            user = db.getUserByID(uid)
            if self.valr.validAge(update.message.text) and int(update.message.text) >= user['p_min_age']:
                db.updateUserData(uid, 'p_max_age', int(update.message.text))
                db.updateUserData(uid, 'dialog_status', 'send_photo')
                bot.sendMessage(cid, self.lang['send_photo'], remove_keyboard=True)
            else:
                bot.sendMessage(cid, self.lang['invalid_age'])

        # Handle the photo and ask if all right
        elif status == 'send_photo':
            photo = update.message.photo[2]
            if self.valr.validPhoto(photo):

                db.updateUserData(uid, 'dialog_status', 'registered')
                db.updateUserData(uid, 'photo', photo.file_id)

                self.printMe(db, bot, update)
                bot.sendMessage(cid, self.lang['registered'], reply_markup=self.markup['confirmReg'])
            else:
                bot.sendMessage(cid, self.lang['invalid_photo'])


        # Start giving accounts
        elif status == 'registered':
            if update.message.text == self.lang['confirm_reg']:
                db.updateUserData(uid, 'dialog_status', 'process')
                db.saveUser(uid)
                self.printNext(db, bot, update)
            elif update.message.text == self.lang['repeat_reg']:
                db.updateUserData(uid, 'dialog_status', 'write_name')
                bot.sendMessage(cid, self.lang['rewrite'], remove_keyboard=True)
            else:
                bot.sendMessage(cid, self.lang['incorrect_answer'], remove_keyboard=True)

        # Search cycle
        elif status == 'process':
            user = db.getUserByID(uid)
            # Account's rate
            if update.message.text == self.lang['like']:
                mutually = db.addLiked(uid, bot, update)
                db.updateUserData(uid, 'liked', user['liked'])
                if mutually is not None:
                    bot.sendMessage(uid, self.lang['mutually'] % (mutually['name'], mutually['contact']),
                                    reply_markup=self.markup['continue'])
                    bot.sendPhoto(mutually['id'], user['photo'],
                                  caption=self.lang['mutually'] % (user['name'], user['contact']),
                                  reply_markup=self.markup['continue'])
                else:
                    self.printNext(db, bot, update)
            elif update.message.text == self.lang['dislike']:
                db.addDisliked(uid, bot, update)
                db.updateUserData(uid, 'disliked', user['disliked'])
                self.printNext(db, bot, update)
            elif update.message.text == self.lang['go_menu']:
                db.updateUserData(uid, 'dialog_status', 'in_menu')
                bot.sendMessage(cid, self.lang['in_menu'], reply_markup=self.markup['mainMenu'])


            elif update.message.text == self.lang['menu_continue']:
                db.updateUserData(uid, 'dialog_status', 'process')
                self.printNext(db, bot, update)
            elif update.message.text == self.lang['menu_stop']:
                db.updateUserData(uid, 'dialog_status', 'freezed')
                bot.sendMessage(cid, self.lang['profile_freezed'], reply_markup=self.markup['frozenMenu'])
            elif update.message.text == self.lang['menu_delete']:
                bot.sendMessage(cid, self.lang['profile_removed'], reply_markup='')
                db.removeUser(uid)
            elif update.message.text == self.lang['menu_edit']:
                db.updateUserData(uid, 'dialog_status', 'write_name')
                bot.sendMessage(cid, self.lang['rewrite'], reply_markup='')
            elif update.message.text == self.lang['menu_show']:
                self.printMe(db, bot, update)
            else:
                bot.sendMessage(cid, self.lang['incorrect_answer'], reply_markup=self.markup['mainMenu'])
                # Main menu
        elif status == 'in_menu':
            if update.message.text == self.lang['menu_continue']:
                db.updateUserData(uid, 'dialog_status', 'process')
                self.printNext(db, bot, update)
            elif update.message.text == self.lang['menu_stop']:
                db.updateUserData(uid, 'dialog_status', 'freezed')
                bot.sendMessage(cid, self.lang['profile_freezed'], reply_markup=self.markup['frozenMenu'])
            elif update.message.text == self.lang['menu_delete']:
                bot.sendMessage(cid, self.lang['profile_removed'], reply_markup='')
                db.removeUser(uid)

            elif update.message.text == self.lang['menu_edit']:
                db.updateUserData(uid, 'dialog_status', 'write_name')
                bot.sendMessage(cid, self.lang['rewrite'], reply_markup='')
            elif update.message.text == self.lang['menu_show']:
                self.printMe(db, bot, update)
            else:
                bot.sendMessage(cid, self.lang['incorrect_answer'], reply_markup=self.markup['mainMenu'])

        # Account is freezed
        elif status == 'freezed':
            if update.message.text == self.lang['menu_continue']:
                db.updateUserData(uid, 'dialog_status', 'process')
                self.printNext(db, bot, update)
            elif update.message.text == self.lang['menu_delete']:
                bot.sendMessage(cid, self.lang['profile_removed'], reply_markup='')
                db.removeUser(uid)

            elif update.message.text == self.lang['menu_edit']:
                db.updateUserData(uid, 'dialog_status', 'write_name')
                bot.sendMessage(cid, self.lang['rewrite'], reply_markup='')
            elif update.message.text == self.lang['menu_show']:
                self.printMe(db, bot, update)
            else:
                bot.sendMessage(cid, self.lang['incorrect_answer'], reply_markup=self.markup['mainMenu'])
        # Other situations
        else:
            bot.sendMessage(cid, self.lang['not_understand'])
