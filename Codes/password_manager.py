import json
import hashlib
import getpass
import sys
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os
import secrets
import string

def hash_password(password):
    """Hash the password using SHA256."""
    return hashlib.sha256(password.encode()).hexdigest()

def register():
    """Register a new user."""
    username = input('Enter your username: ')
    master_password = getpass.getpass('/,Enter your master password: ')
    master_password_hash = hash_password(master_password)

    with open('user_data.json', 'w') as file:
        json.dump({'username': username, 'master_password': master_password_hash}, file)
        print('\n[+] Registration Completed!!\n')

def login(username, entered_password):
    """Login to the password manager."""
    try:
        with open('user_data.json', 'r') as file:
            user_data = json.load(file)
            stored_password = user_data.get('master_password')
            entered_password_hash = hash_password(entered_password)

            if entered_password_hash == stored_password and username == user_data.get('username'):
                print('\n[+] Login Successful...\n')
                return True
            else:
                print('\n[+] Invalid Login Credentials... Login Failed!!\n')
                print('\n[+] Use the registered credentials to login')
                sys.exit()
    except Exception:
        print('\n[+] You must register to begin...!!!\n')
        sys.exit()

def generate_key(master_password):
    """Generate a key using PBKDF2HMAC."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=b'salt',
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))
    return key

def encrypt_password(password, key):
    """Encrypt the password using Fernet."""
    f = Fernet(key)
    return f.encrypt(password.encode())

def decrypt_password(encrypted_password, key):
    """Decrypt the password using Fernet."""
    f = Fernet(key)
    return f.decrypt(encrypted_password).decode()

def generate_password(length=12):
    """Generate a random password."""
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password

def save_password(website, username, password, key):
    """Save a password for a website."""
    encrypted_password = encrypt_password(password, key)
    try:
        with open('password.json', 'r') as file:
            passwords = json.load(file)
    except FileNotFoundError:
        passwords = {}
    
    passwords[website] = {
        'username': username,
        'password': encrypted_password.decode()
    }

    with open('password.json', 'w') as file:
        json.dump(passwords, file)
        print(f'\n[+] Password saved for {website}...\n')

def view_saved_websites(key):
    """View saved websites and their passwords."""
    try:
        with open('password.json', 'r') as file:
            passwords = json.load(file)
            print("Websites you saved...")
            for website, data in passwords.items():
                encrypted_password = data['password'].encode()
                decrypted_password = decrypt_password(encrypted_password, key)
                print(f"Website: {website}")
                print(f"Username: {data['username']}")
                print(f"Password: {decrypted_password}\n")
    except FileNotFoundError:
        print('\n[+] No passwords saved yet...\n')

def main():
    while True:
        print('---Welcome to Password Manager---')
        print('--------------------------------------------------------------------------------------------------------------------------------')
        print('1.Register \n2.Login \n3.Quit')
        choice = input ('Enter a choice...: ')
        
        if choice == '1':
            register()
        elif choice == '2':
            username = input('Enter your username: ')
            entered_password = getpass.getpass('Enter your master password: ')
            if login(username, entered_password):
                master_key = generate_key(entered_password)
                while True:
                    print('\n---Password Manager Menu---')
                    print('1.Save Password \n2.View Saved Passwords \n3.Generate Password \n4.Back')
                    action = input ('Enter a choice...: ')
                    
                    if action == '1':
                        website = input('Enter the website: ')
                        username = input('Enter the username: ')
                        password = getpass.getpass('Enter the password: ')
                        save_password(website, username, password, master_key)
                    elif action == '2':
                        view_saved_websites(master_key)
                    elif action == '3':
                        length = int(input('Enter the desired password length (default is 12): ') or 12)
                        generated_password = generate_password(length)
                        print(f'\nGenerated Password: {generated_password}\n')
                    elif action == '4':
                        break
                    else:
                        print('Invalid input... Please try again!')
        elif choice == '3':
            print('Thanks for using Password Manager...Bye!!!')
            break
        else:
            print('Invalid input... Please try again!')

if __name__ == "__main__":
    main()