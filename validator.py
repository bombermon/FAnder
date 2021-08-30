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
            if 10 < age < 100:
                return True
            return False
        except:
            return False
    
    def checkPartner(self, user, partner):
        pCity = partner['city'].lower().strip()
        uCity = user['city'].lower().strip()
        if (partner['dialog_status'] == 'process') and (partner['id'] != user['id']) and (partner['age'] >= user['p_min_age']) and (partner['age'] <= user['p_max_age']) and (partner['sex'] == user['p_sex']) and (user['sex'] == partner['p_sex']) and ((partner['dialog_status'] == "process") or (partner['dialog_status'] == "freezed")):
            if (partner['id'] not in user['liked']) and (partner['id'] not in user['disliked']):
                return True
        return False