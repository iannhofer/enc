from src.backend.database import authenticate_user, create_user


def getCredentials():
    username = input("Username: ")
    pw = input("Password: ")
    return username, pw

def logIn():
    username, pw = getCredentials()
    user = authenticate_user(username, pw)
    if user is None:
        user = create_user(username, pw)
        if user is None:
            print("unknown error")
            return None
    return user