import json
import os
import logging

class Database:
    def __init__(self, config):
        self.users = []
        self.logger = logging.getLogger(__name__)

        # load user profile from database
        if not os.path.exists("profiles"):
            os.mkdir('profiles')
        files = os.listdir('profiles')
        for i in range(len(files)):
            with open('profiles/'+files[i], 'r', encoding='utf-8') as fh:
                self.users.append(json.load(fh))
    
    def saveUser(self, id):
        for i in range(len(self.users)):
            if self.users[i]['id'] == id:
                with open('profiles/'+str(id)+'.json', 'w', encoding='utf_8') as fh:
                    fh.write(json.dumps(self.users[i], ensure_ascii=False))
        
    
    def addLiked(self, id, bot, update):
        liked_id = self.getUserByID(id)['last_profile']
        for i in range(len(self.users)):
            if self.users[i]['id'] == id:
                self.users[i]['liked'].append(liked_id)
                # check reciprocity
                partner = None
                for j in range(len(self.users)):
                    if self.users[j]['id'] == liked_id:
                        partner = self.users[j]
                if id in partner['liked']:
                    return partner
                else:
                    return None
    
    def addDisliked(self, id, bot, update):
        disliked_id = self.getUserByID(id)['last_profile']
        for i in range(len(self.users)):
            if(self.users[i]['id'] == id):
                self.users[i]['disliked'].append(disliked_id)

    def addReport(self, id, bot, update):   # мы репортнули
        Reported_id = self.getUserByID(id)['last_profile']
        for i in range(len(self.users)):
            if(self.users[i]['id'] == id):
                self.users[i]['reported'].append(Reported_id)

    def addReported(self, id, bot, update):   # нас репортнули
        Reported_id = self.getUserByID(id)['last_profile']
        for i in range(len(self.users)):
            if(self.users[i]['id'] == Reported_id):
                self.users[i]['reports'].append(id)
        return Reported_id

    
    def getUsers(self):
        return self.users
    
    def getChatIDs(self):
        data = []
        for i in range(len(self.users)):
            data.append(self.users[i]['id'])

    def addUser(self, user):
        self.users.append(user)
    
    def removeUser(self, id):
        for i in range(len(self.users)):
            if self.users[i].get("disliked") is not None:
                if id in self.users[i]["disliked"]:
                    temp_dis = []
                    for j in self.users[i]["disliked"]:
                        if j != id:
                            temp_dis.append(j)
                    self.users[i]["disliked"] = temp_dis
                    self.updateUserData(self.users[i]['id'], "disliked", self.users[i]["disliked"])

            if self.users[i].get("liked") is not None:
                if id in self.users[i]["liked"]:
                    temp_like = []
                    for j in self.users[i]["liked"]:
                        if j != id:
                            temp_like.append(j)
                    self.users[i]["liked"] = temp_like
                    self.updateUserData(self.users[i]['id'], "liked", self.users[i]["liked"])

        for i in range(len(self.users)):
            if self.users[i]['id'] == id:
                self.users[i]['dialog_status'] = "deleted"
                self.users[i]['liked'] = []
                self.updateUserData(self.users[i]['id'], "liked", self.users[i]['liked'])
                self.users[i]['disliked'] = []
                self.updateUserData(self.users[i]['id'], "disliked", self.users[i]['disliked'])
                self.updateUserData(self.users[i]['id'], "dialog_status", self.users[i]['dialog_status'])
                return

    def getUserByID(self, id):
        for i in range(len(self.users)):
            if self.users[i]['id'] == id:
                return self.users[i]
        return None
    
    def updateUserData(self, id, key, value):
        for i in range(len(self.users)):
            if self.users[i]['id'] == id:
                self.users[i][key] = value
        self.saveUser(id)
