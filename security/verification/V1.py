from sqlite3 import SQLITE_DBCONFIG_LEGACY_ALTER_TABLE
import collections
from src.backend.main import app
import unittest
from fastapi.testclient import TestClient
import random
from pathlib import Path
import os
from src.backend.database import deleteUser



class TestVulnerabilities(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.users = []
        self.files = []


    def testCookieTampering(self):
        filename = "test.txt"
        cookie1 = self.createUser("V1_user1")
        code = str(random.randint(1,1000000))
        self.uploadFile(cookie1, code, filename)

        cookie2 = self.createUser("V1_user2")
        self.assertIn("No data", self.client.get("/dashboard").text)
        self.uploadFile(cookie1, "-1", filename)
        self.assessIntegrity(cookie1, code, filename)

    def testPathTraversal(self):
        filename = "traversal.txt"
        cookie3 = self.createUser("V1_user3")
        self.uploadFile("..", "test", filename)
        self.assertTrue(Path(f"{filename}.encrypted").exists())
        self.files.append(f"{filename}.encrypted")

    """helper"""

    def createUser(self, username):
        response = self.client.post("/login", data = {"username":username, "password": "123", "action": "register"})
        cookie = response.cookies.get("user_id")
        self.users.append(cookie)
        return cookie
    
    def uploadFile(self, cookie, text, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(text)
        with open(filename, "rb") as f:
            self.client.post("/upload", cookies = {"user_id":str(cookie)}, files = {"file":f})
        self.files.append(filename)
    
    def assessIntegrity(self, cookie, code, filename):
        self.client.cookies.set("user_id", str(cookie))
        response = self.client.get(f"/download/{filename}")
        self.assertNotEqual(response.text, code)



    
    def tearDown(self):

        """to be implemeted, first create method to delete user"""
        for filename in self.files:
            os.remove(filename)
        for user in self.users:
            deleteUser(user)

if __name__ == "__main__":
    unittest.main()




        
        
        
    