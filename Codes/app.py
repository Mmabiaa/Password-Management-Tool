# app.py
# Author - Mmabiaa

import getpass
from password_manager import *

# Function to print in green
def print_green(text):
    print("\033[32m" + text + "\033[0m")



def check_user_choice(choice):

    if choice == '1':
        register()

    elif choice == '2':
        check_login()

    elif choice == '3':
        print_green('Thanks for using Password Manager...Bye!!!')

    else:
        print_green('Invalid input... Please try again!')



def check_login():
    username = input('Enter your username: ')
    entered_password = getpass.getpass('Enter your master password: ')

    if login(username, entered_password):

            master_key = generate_key(entered_password)

            print_green('\n---Password Manager Menu---')
            print_green('1.Save Password \n2.View Saved Passwords \n3.Generate Password \n4.Back')
            action = input ('Enter a choice...: ')

            check_action(action, master_key)

    else:
        print_green('Invalid username or password... Please try again!')


def check_action(action, master_key):
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
        print_green(f'\nGenerated Password: {generated_password}\n')

    elif action == '4':

        print('/n/n/n/n/n')
        main()

    else:
        print_green('Invalid input... Please try again!')



def display_title():
    print_green("""
    ██████╗ ███████╗██████╗ ████████╗██████╗  █████╗ ███╗   ██╗███████╗██████╗ 
    ██╔══██╗██╔════╝██╔══██╗╚══██╔══╝██╔══██╗██╔══██╗████╗  ██║██╔════╝██╔══██╗
    ██████╔╝█████╗  ██████╔╝   ██║   ██████╔╝███████║██╔██╗ ██║█████╗  ██████╔╝
    ██╔═══╝ ██╔══╝  ██╔══██╗   ██║   ██╔══██╗██╔══██║██║╚██╗██║██╔══╝  ██╔══██╗
    ██║     ███████╗██║  ██║   ██║   ██║  ██║██║  ██║██║ ╚████║███████╗██║  ██║
    ╚═╝     ╚══════╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝
    """)



def main():

        display_title()
        print_green('---Welcome to Password Manager---')
        print_green('--------------------------------------------------------------------------------------------------------------------------------')
        print_green('1.Register \n2.Login \n3.Quit')
        choice = input ('Enter a choice...: ')

        check_user_choice(choice)

if __name__ == "__main__":
    main()
# Author - Mmabiaa
