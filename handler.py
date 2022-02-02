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

            'filter': ReplyKeyboardMarkup([[KeyboardButton(self.lang['only_u']),
                                               KeyboardButton(self.lang['all'])],
                                              [KeyboardButton(self.lang['all_without'])]],
                                             resize_keyboard=True, one_time_keyboard=True),
            'markChoice': ReplyKeyboardMarkup(
                [[KeyboardButton(self.lang['like']), KeyboardButton(self.lang['dislike'])],
                 [KeyboardButton(self.lang['report'])], [KeyboardButton(self.lang['go_menu'])]],
                row_width=2, resize_keyboard=True, one_time_keyboard=False),
            'universityChoice': ReplyKeyboardMarkup(
                [[KeyboardButton(self.lang['financial_university']),
                  KeyboardButton(self.lang['ranepa'])],
                 [KeyboardButton(self.lang['msu']),
                  KeyboardButton(self.lang['bmstu'])],
                # [KeyboardButton(self.lang['rudn_university']),
                #  KeyboardButton(self.lang['rsmu'])],
                # [KeyboardButton(self.lang['moscow_state_pedagogical_university']),
                #  KeyboardButton(self.lang['rsuh'])]
                 ],
                row_width=2, resize_keyboard=True, one_time_keyboard=True),
            'facultyChoice': ReplyKeyboardMarkup(
                [[KeyboardButton(self.lang['faculty_of_information_technology_and_big_data_analysis']),
                  KeyboardButton(self.lang['faculty_of_finance'])],
                 [KeyboardButton(self.lang['higher_school_of_management']),
                  KeyboardButton(self.lang['faculty_of_international_economic_relations'])],
                 [KeyboardButton(self.lang['faculty_of_social_sciences_and_mass_communications']),
                  KeyboardButton(self.lang['faculty_of_economics_and_business'])],
                 [KeyboardButton(self.lang['faculty_of_law']),
                  KeyboardButton(self.lang['faculty_of_taxes_audit_and_business_analysis'])]],
                row_width=2, resize_keyboard=True, one_time_keyboard=True),
            'mainMenu': ReplyKeyboardMarkup([[KeyboardButton(self.lang['menu_continue'])],
                                             [KeyboardButton(self.lang['menu_stop'])],
                                             [KeyboardButton(self.lang['menu_delete'])],
                                             [KeyboardButton(self.lang['menu_edit'])],
                                             [KeyboardButton(self.lang['menu_show'])]], resize_keyboard=True,
                                            one_time_keyboard=True),
            'mainMenu_admin': ReplyKeyboardMarkup([[KeyboardButton(self.lang['menu_continue'])],
                                                   [KeyboardButton(self.lang['menu_stop'])],
                                                   [KeyboardButton(self.lang['menu_delete'])],
                                                   [KeyboardButton(self.lang['menu_edit'])],
                                                   [KeyboardButton(self.lang['menu_show'])],
                                                   [KeyboardButton(self.lang['menu_admin'])]], resize_keyboard=True,
                                                  one_time_keyboard=True),
            'adminMenu': ReplyKeyboardMarkup([[KeyboardButton(self.lang['show_all_reported'])],
                                              [KeyboardButton(self.lang['go_menu'])]], resize_keyboard=True,
                                             one_time_keyboard=True),
            'frozenMenu': ReplyKeyboardMarkup([[KeyboardButton(self.lang['menu_continue'])],
                                               [KeyboardButton(self.lang['menu_delete'])],
                                               [KeyboardButton(self.lang['menu_edit'])],
                                               [KeyboardButton(self.lang['menu_show'])]], resize_keyboard=True,
                                              one_time_keyboard=True),
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
        for i in random.sample(range(0, len(db.getUsers())), len(db.getUsers())):
            if self.valr.checkPartner(user, db.getUsers()[i]):
                partner = db.getUsers()[i]
                db.updateUserData(uid, 'last_profile', partner['id'])
                if user.get("admin"):
                    bot.sendPhoto(cid, partner['photo'], reply_markup=self.markup['markChoice'],
                                  caption=self.lang['account_info'] % (
                                      partner['name'], partner['age'], self.lang[partner['university']],
                                      partner['desc']) + '\n-------------' + '\nID: ' + str(
                                      partner['id']))

                else:
                    bot.sendPhoto(cid, partner['photo'], reply_markup=self.markup['markChoice'],
                                  caption=self.lang['account_info'] % (
                                      partner['name'], partner['age'], self.lang[partner['university']],
                                      partner['desc']), )
                return
        if user.get("admin"):
            bot.sendMessage(cid, self.lang['no_partners'], reply_markup=self.markup['mainMenu_admin'])
        else:
            bot.sendMessage(cid, self.lang['no_partners'], reply_markup=self.markup['mainMenu'])

    def printMe(self, db, bot, update, status='True'):
        uid = update.message.from_user.id
        cid = update.message.chat_id
        user = db.getUserByID(uid)
        if status == 'True':
            bot.sendPhoto(cid, user['photo'],
                          caption=self.lang['account_info'] % (
                          user['name'], user['age'], self.lang[user['university']],  user['desc']),
                          reply_markup=self.markup['mainMenu'])
        elif status == 'False':
            bot.sendPhoto(cid, user['photo'],
                          caption=self.lang['account_info'] % (
                              user['name'], user['age'], self.lang[user['university']],  user['desc']))
        elif status == 'frozen':
            bot.sendPhoto(cid, user['photo'],
                          caption=self.lang['account_info'] % (
                              user['name'], user['age'], self.lang[user['university']],  user['desc']),
                          reply_markup=self.markup['frozenMenu'])

    def showAllReported(self, cid, db, bot):
        users = db.getUsers()
        for user in users:
            reports = user.get('reports')
            if reports is not None:
                if len(reports) > 0 and user["dialog_status"] != "ban":
                    bot.sendPhoto(cid, user['photo'], caption=self.lang['account_info'] % (
                        user['name'], user['age'],
                        user['desc']) + "\n---------------------" + "\nID пользователя " + str(user.get('id')) +
                                                              "\nЖалоб: " + str(
                        len(reports)) + '\nПожаловались: ' + str(reports),
                                  reply_markup=self.markup['adminMenu'])

    def handle(self, db, bot, update):
        uid = update.message.from_user.id
        cid = update.message.chat_id
        user = db.getUserByID(uid)
        status = user['dialog_status']

        message = update.message.text
        if message is not None:
            words = message.split()
            if words[0] == "ban" and user.get("admin"):
                if len(words) > 1:
                    ban_id = int(words[1])
                    for user in db.getUsers():
                        if user.get('id') is not None and user.get('id') == ban_id:
                            if user.get("dialog_status") == "ban":
                                bot.sendMessage(cid, "этот пользователь уже забанен")
                                return
                            if user.get("admin"):
                                bot.sendMessage(cid, "нельзя банить админа")
                            else:
                                db.updateUserData(user.get('id'), 'dialog_status', 'ban')
                                bot.sendMessage(cid, "пользователь с Id " + words[1] + " забанен")
                                if len(words) > 2:
                                    bot.sendMessage(ban_id, "Вы заблокированы по причене:\n" + " ".join(words[2:]))
                            return
                    bot.sendMessage(cid, "пользователь с таким id не найден")
                    return
                else:
                    bot.sendMessage(cid,
                                    "не написан id человека, которого нужно забанить. Пример команды: 'ban 123456789'")
                return
            if words[0] == "unban" and user.get("admin"):
                if len(words) > 1:
                    unban_id = int(words[1])
                    for user in db.getUsers():
                        if user.get('id') is not None and user.get('id') == unban_id:
                            if user.get("dialog_status") == "ban":
                                db.updateUserData(user.get('id'), 'dialog_status', 'deleted')
                                bot.sendMessage(cid, "пользователь с Id " + words[1] + " разбанен")
                                bot.sendMessage(unban_id, "Вы разбанены, напишите '/start' для продолжения")
                            else:
                                bot.sendMessage(cid, "этот пользователь не забанен")
                            return

                    bot.sendMessage(cid, "пользователь с таким id не найден")
                    return
                else:
                    bot.sendMessage(cid,
                                    "не написан id человека, которого нужно забанить. Пример команды: 'ban 123456789'")
                return
            if words[0] == "sayeverybody" and user.get("admin"):
                for user in db.getUsers():
                    try:
                        send = user.get('id')
                        bot.sendMessage(send, " ".join(words[1:]))
                    except:
                        pass

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
            db.updateUserData(uid, 'dialog_status', 'write_university')
            bot.sendMessage(cid, self.lang['write_university'], reply_markup=self.markup['universityChoice'])

        # Write university
        elif status == 'write_university':
            if update.message.text == self.lang['financial_university']:
                db.updateUserData(uid, 'university', "financial_university")
            elif update.message.text == self.lang['ranepa']:
                db.updateUserData(uid, 'university', 'ranepa')
            elif update.message.text == self.lang['msu']:
                db.updateUserData(uid, 'university', 'msu')
            elif update.message.text == self.lang['bmstu']:
                db.updateUserData(uid, 'university', 'bmstu')
            else:
                bot.sendMessage(cid, self.lang['incorrect_answer'])
                return
            db.updateUserData(uid, 'dialog_status', 'write_desc')
            bot.sendMessage(cid, self.lang['write_desc'], reply_markup=None, remove_keyboard=True)
            #db.updateUserData(uid, 'dialog_status', 'write_faculty')
            #bot.sendMessage(cid, self.lang['write_faculty'], reply_markup=self.markup['facultyChoice'])

        # Write faculty (Факультет)
        #elif status == 'write_faculty':
        #    if update.message.text == self.lang['faculty_of_information_technology_and_big_data_analysis']:
        #        db.updateUserData(uid, 'faculty', "faculty_of_information_technology_and_big_data_analysis")
        #    elif update.message.text == self.lang['faculty_of_finance']:
        #        db.updateUserData(uid, 'faculty', 'faculty_of_finance')
        #    elif update.message.text == self.lang['higher_school_of_management']:
        #        db.updateUserData(uid, 'faculty', 'higher_school_of_management')
        #    elif update.message.text == self.lang['faculty_of_international_economic_relations']:
        #        db.updateUserData(uid, 'faculty', 'faculty_of_international_economic_relations')
        #    elif update.message.text == self.lang['faculty_of_social_sciences_and_mass_communications']:
        #        db.updateUserData(uid, 'faculty', 'faculty_of_social_sciences_and_mass_communications')
        #    elif update.message.text == self.lang['faculty_of_economics_and_business']:
        #        db.updateUserData(uid, 'faculty', 'faculty_of_economics_and_business')
        #    elif update.message.text == self.lang['faculty_of_law']:
        #        db.updateUserData(uid, 'faculty', 'faculty_of_law')
        #    elif update.message.text == self.lang['faculty_of_taxes_audit_and_business_analysis']:
        #        db.updateUserData(uid, 'faculty', 'faculty_of_taxes_audit_and_business_analysis')
        #    else:
        #        bot.sendMessage(cid, self.lang['incorrect_answer'])
        #        return
        #    db.updateUserData(uid, 'dialog_status', 'write_desc')
        #    bot.sendMessage(cid, self.lang['write_desc'], reply_markup=None, remove_keyboard=True)

        # Write description
        elif status == 'write_desc':
            db.updateUserData(uid, 'desc', str(update.message.text))
            db.updateUserDatalogger = logging.getLogger(__name__)
            db.updateUserData(uid, 'dialog_status', 'write_contact')
            bot.sendMessage(cid, self.lang['write_contact'], reply_markup=None, remove_keyboard=True)
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
            bot.sendMessage(cid, self.lang['write_p_min_age'], reply_markup=None, remove_keyboard=True)

        # Enter min partner's age
        elif status == 'write_p_min_age':
            if self.valr.validAge(update.message.text):
                db.updateUserData(uid, 'p_min_age', int(update.message.text))
                db.updateUserData(uid, 'dialog_status', 'write_p_max_age')
                bot.sendMessage(cid, self.lang['write_p_max_age'], reply_markup=None, remove_keyboard=True)
            else:
                bot.sendMessage(cid, self.lang['invalid_age'])

        # Enter max partner's age
        elif status == 'write_p_max_age':
            user = db.getUserByID(uid)
            if self.valr.validAge(update.message.text) and int(update.message.text) >= user['p_min_age']:
                db.updateUserData(uid, 'p_max_age', int(update.message.text))
                db.updateUserData(uid, 'dialog_status', 'filter')
                bot.sendMessage(cid, self.lang['filter'], reply_markup=self.markup['filter'])
            else:
                bot.sendMessage(cid, self.lang['invalid_age'])

        elif status == 'filter':
            if update.message.text == self.lang['only_u']:
                db.updateUserData(uid, 'filter', 0)
            elif update.message.text == self.lang['all']:
                db.updateUserData(uid, 'filter', 1)
            elif update.message.text == self.lang['all_without']:
                db.updateUserData(uid, 'filter', 2)
            else:
                bot.sendMessage(cid, self.lang['incorrect_answer'])
                return
            db.updateUserData(uid, 'dialog_status', 'send_photo')
            bot.sendMessage(cid, self.lang['send_photo'], reply_markup=None, remove_keyboard=True)

        elif status == 'reset_filter':
            if update.message.text == self.lang['only_u']:
                db.updateUserData(uid, 'filter', 0)
            elif update.message.text == self.lang['all']:
                db.updateUserData(uid, 'filter', 1)
            elif update.message.text == self.lang['all_without']:
                db.updateUserData(uid, 'filter', 2)
            else:
                bot.sendMessage(cid, self.lang['incorrect_answer'])
                return
            db.updateUserData(uid, 'dialog_status', 'process')
            db.saveUser(uid)
            self.printNext(db, bot, update)

        # Handle the photo and ask if all right
        elif status == 'send_photo':
            try:
                photo = update.message.photo[2]
            except IndexError:
                bot.sendMessage(cid, 'Это не фотография!')
            if self.valr.validPhoto(photo):

                db.updateUserData(uid, 'dialog_status', 'registered')
                db.updateUserData(uid, 'photo', photo.file_id)

                self.printMe(db, bot, update, status='False')
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
                if user.get("admin"):
                    bot.sendMessage(cid, self.lang['in_menu'], reply_markup=self.markup['mainMenu_admin'])
                else:
                    bot.sendMessage(cid, self.lang['in_menu'], reply_markup=self.markup['mainMenu'])
            elif update.message.text == self.lang['report']:
                db.addDisliked(uid, bot, update)
                db.addReport(uid, bot, update)

                reported_id = db.addReported(uid, bot, update)
                who_rep = db.getUserByID(reported_id)
                db.updateUserData(reported_id, 'reports', who_rep['reports'])

                db.updateUserData(uid, 'reported', user['reported'])
                db.updateUserData(uid, 'disliked', user['disliked'])
                self.printNext(db, bot, update)
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
                self.printMe(db, bot, update, status='True')
            elif update.message.text == self.lang['menu_admin'] and user.get("admin"):
                db.updateUserData(uid, 'dialog_status', 'in_admin_menu')
                bot.sendMessage(cid, self.lang['in_admin_menu'], reply_markup=self.markup['adminMenu'])
            else:
                if user.get("admin"):
                    bot.sendMessage(cid, self.lang['incorrect_answer'], reply_markup=self.markup['mainMenu_admin'])
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
            elif update.message.text == self.lang['menu_admin'] and user.get("admin"):
                db.updateUserData(uid, 'dialog_status', 'in_admin_menu')
                bot.sendMessage(cid, self.lang['in_admin_menu'], reply_markup=self.markup['adminMenu'])
            else:
                if user.get("admin"):
                    bot.sendMessage(cid, self.lang['incorrect_answer'], reply_markup=self.markup['mainMenu_admin'])
                else:
                    bot.sendMessage(cid, self.lang['incorrect_answer'], reply_markup=self.markup['mainMenu'])

                # admin menu
        elif status == 'in_admin_menu':
            if update.message.text == self.lang['go_menu']:
                db.updateUserData(uid, 'dialog_status', 'in_menu')
                if user.get("admin"):
                    bot.sendMessage(cid, self.lang['in_menu'], reply_markup=self.markup['mainMenu_admin'])
                else:
                    bot.sendMessage(cid, self.lang['in_menu'], reply_markup=self.markup['mainMenu'])
            elif update.message.text == self.lang['show_all_reported']:
                self.showAllReported(cid, db, bot)

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
                self.printMe(db, bot, update, status='frozen')
            else:
                bot.sendMessage(cid, self.lang['incorrect_answer'], reply_markup=self.markup['frozenMenu'])
        # Other situations

        elif status == 'ban':
            bot.sendMessage(cid, 'Вы заблокированы за нарушения правил сервиса.')
        else:
            bot.sendMessage(cid, self.lang['not_understand'])

