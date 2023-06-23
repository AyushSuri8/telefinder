import os
import requests
from lxml import html
from tqdm import tqdm

def is_valid_username(username):
    if not username.isalnum() and "_" not in username:
        return False
    if len(username) < 5:
        return False
    return True

def check_username(username):
    if not is_valid_username(username):
        return False

    url = f"https://t.me/{username}"
    response = requests.get(url)
    tree = html.fromstring(response.content)
    user_icon = tree.xpath('//*[@class="tgme_icon_user"]')
    return len(user_icon) > 0

def main():
    valid_usernames = []
    file_path = os.path.join(os.path.dirname(__file__), "list.txt")
    valid_file_path = os.path.join(os.path.dirname(__file__), "valid.txt")
    
    # Verificar si el archivo existe
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            usernames = file.read().splitlines()
            progress_bar = tqdm(usernames, desc="Checking usernames", unit="username")
            for username in progress_bar:
                if check_username(username):
                    valid_usernames.append(username)
        
        with open(valid_file_path, "w") as valid_file:
            for username in valid_usernames:
                valid_file.write(username + "\n")
        
        print("Valid Usernames:")
        for username in valid_usernames:
            print(username)
    else:
        print(f"El archivo '{file_path}' no existe.")

if __name__ == "__main__":
    main()
