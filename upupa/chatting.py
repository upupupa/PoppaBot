import os
import sys

sys.path.append(os.path)
from upupa.databasesqlite3 import Database

class Chatting:
    """
    Params:
    command - requseted command.
    server_id - discord server id.
    *args - requested string, response string.
    """
    def __init__(self, command, server_id:int):
        if os.name == "nt":
            self.path = os.path.normpath(os.getcwd() + "\\database\\") + "\\"
        else:
            self.path = os.path.normpath(os.getcwd() + "/database/") + "/"
        self.command = command
        self.server_id = server_id
        self.name = "responses.db"
        self.db = Database(path=self.path, name=self.name)

    def addResponse_str(self, *args):
        """
        Adds response for requested phrase to sqlite3 database.
        """
        self.request_str = args[0]
        if len(self.request_str) > 64:
            raise Exception("Request string is too long!")
        self.response_str = args[1]
        if len(self.response_str) > 128:
            raise Exception("Response string is too long!")
        self.db.insert_response(server_id=self.server_id, request_str=self.request_str, response_str=self.response_str)

    def getResponseEntry(self):
        entry = self.db.get_response(self.server_id)
        return entry

    def removeResponseEntry(self, idPrimKey):
        self.db.remove_entry(idPrimKey=idPrimKey)

    def setLang(self, lang):
        self.db.insert_locale(self.server_id, lang)
    
    def getLang(self):
        return self.db.get_locale(self.server_id)

    def insertRole(self, role):
        self.db.insert_role(self.server_id, role)

    def getRoles(self):
        roles = self.db.get_roles(self.server_id)
        if roles is None:
            return None
        return roles.split(";")

if __name__ == "__main__":    
    test = Chatting("add", "test")
    test.addResponse_str("string1", "string2")