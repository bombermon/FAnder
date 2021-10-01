class Validator:
    def validName(self, name):
        if 1 < len(name) < 30:
            return True
        return False
    
    def validPhoto(self, photo):
        return True
    
    def validAge(self, age):
        try:
            age = int(age)
            if 17 < age < 31:
                return True
            return False
        except:
            return False
    
    def checkPartner(self, user, partner):
        #pCity = partner['city'].lower().strip()
        #uCity = user['city'].lower().strip()
        if ((partner['dialog_status'] == "process") or (partner['dialog_status'] == "in_menu")):
            # ДОБАВИТЬ ЗДЕСЬ СТРОЧКУ ПРОВЕРКУ НА НАХОЖДЕНИЕ ЮЗЕРА В СПИСКЕ АДМИНОВ
            if (partner['id'] != user['id']) and (partner['age'] >= user['p_min_age']) and (partner['age'] <= user['p_max_age']):
                if (partner['id'] not in user['liked']) and (partner['id'] not in user['disliked']):
                    if (partner['p_sex'] == 2 and user['p_sex'] == 2) or ((user['sex'] == partner['p_sex']) and (user['p_sex'] == partner['sex'])) or (user['p_sex'] == 2 and (user['sex'] == partner['p_sex'])) or (partner['p_sex'] == 2 and (partner['sex'] == user['p_sex'])):
                        return True
        return False