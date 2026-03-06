from src.backend.database import authenticateUser, createUser


def getCredentials():
    username = input("Username: ")
    pw = input("Password: ")
    return username, pw

def logIn():
    username, pw = getCredentials()
    user = authenticateUser(username, pw)
    if user is None:
        print("user not found, creating user")
        user = createUser(username, pw)
        print("user created")
        if user is None:
            print("user still not found")
            return None
    return user