import sqlite3
from sqlite3 import Error
import os
import json

class Database:
    """
    Params:\n
    path - path to folder with sqlite3 db file.\n
    name - name of sqlite3 .db file.
    server_id - Discord server id (INT).
    """
    def __init__(self, path, name):
        self.name = name
        self.path = path
        self.connect()

    def create_all_databases(self):
        """
        This function creates .db' files, tables.
        """
        self.conn = sqlite3.connect(self.path + "responses.db")
        self.cursor = self.conn.cursor()
        return

    def create_tabels(self):
        """
        This function creates needed tables to get up with.
        """
        try:
            self.cursor.execute("CREATE TABLE Discord(id INTEGER PRIMARY KEY, server_id INT UNIQUE, admin_role STRING, locale STRING)")
            print("Table Discord created!")
        except Error as e:
            print(e)
        try:
            self.cursor.execute("CREATE TABLE Responses(id INTEGER PRIMARY KEY, server_id INT," +
                                "request_str STRING, response_str STRING, " + 
                                "FOREIGN KEY (server_id) REFERENCES Discord(id))")
            print("Table Responses created!")
        except Error as e:
            print(e)    
        return

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.path + self.name)
        except Error as e:
            print(e)
            self.create_all_databases()
            self.create_tabels()
        finally:
            self.cursor = self.conn.cursor()
        return

    def check_databases(self):
        with open(self.path + "databaselist.json", "r", encoding="utf-8") as fjson:
            self.databases = json.load(fjson)
            fjson.close()

    def get_response(self, server_id:int):
        """
        Params:\n
        server_id - Discord server id.
        request_str - requested string.
        """
        self.cursor.execute("SELECT t1.*, t2.* FROM Responses t1 LEFT JOIN Discord t2 ON t1.server_id=t2.id WHERE t2.server_id=?", (server_id,))
        entry = self.cursor.fetchall()
        if entry is None:
            print("No entry found")
        return entry

    def get_locale(self, server_id:int):
        self.cursor.execute("SELECT locale FROM Discord WHERE (server_id=?)", (server_id,))
        entry = self.cursor.fetchone()
        if entry[0] is None:
            print("No locale set. Setting locale.")
            self.cursor.execute("UPDATE Discord SET locale=? WHERE server_id=?", ("en", server_id))
            self.conn.commit()
            return "en"
        return entry[0]

    def get_roles(self, server_id:int):
        self.cursor.execute("SELECT role FROM Discord WHERE (server_id=?)", (server_id,))
        entry = self.cursor.fetchone()
        if entry[0] is None:
            return None
        return entry[0]

    def insert_response(self, server_id:int, request_str, response_str):
        """
        Params:\n
        request_str - requested string.
        response_str - response string.
        server_id - Discord server id.
        """
        self.insert_server(server_id=server_id)
        self.cursor.execute("INSERT INTO Responses(server_id, request_str, response_str) VALUES ((SELECT id FROM Discord WHERE server_id=?), ? ,?)", (server_id, request_str, response_str))
        self.conn.commit()

    def insert_role(self, server_id:int, role):
        self.roles = self.get_roles(server_id)
        if self.roles is None:
            role += ";"
        else:
            role = self.roles + role + ";"
        self.cursor.execute("UPDATE Discord SET role=? WHERE server_id=?", (role, server_id))
        self.conn.commit()
    
    def update_roles(self, server_id:int, roles):
        self.cursor.execute("UPDATE Discord SET role=? WHERE server_id=?", (roles, server_id))
        self.conn.commit()

    def insert_server(self, server_id:int):
        """
        Params:\n
        server_id (int) - Discord server id.
        """
        self.cursor.execute("SELECT * FROM Discord WHERE (server_id=?)", (server_id,))
        entry = self.cursor.fetchone()
        if entry is None:
            print("No entry found, inserting new entry")
            self.cursor.execute("INSERT INTO Discord (server_id, locale) VALUES (?, ?)", (server_id, "en"))
            self.conn.commit()
        else:
            print("Entry found")
        return

    def insert_locale(self, server_id:int, locale):
        self.cursor.execute("UPDATE Discord SET locale=? WHERE server_id=?", (locale, server_id))
        self.conn.commit()

    def remove_entry(self, idPrimKey:int):
        """
        Params:\n
        id (int) - Entry id.
        """
        self.cursor.execute("DELETE FROM Responses WHERE (id=?)", (idPrimKey,))
        self.conn.commit()

if __name__ == "__main__":
    path = os.path.normpath(os.getcwd() + "\\database\\") + "\\"
    name = "responses.db"
    server_id = 1234
    test = Database(path=path, name=name)
    test.create_tabels()
    test.insert_response(server_id=server_id, request_str="testR", response_str="testA")