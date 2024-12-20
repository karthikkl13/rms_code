import time
import os
import mysql.connector as sql
from pyfiglet import Figlet

try:
    mycon = sql.connect(host='localhost', user='root', password='karthikkl13', database='achu')
    cur = mycon.cursor()
except sql.Error as err:
    print(f"Error: Could not connect to database. {err}")
    exit()

def login():
    os.system('cls')
    f = Figlet(font='ANSI_Shadow')
    print(f.renderText('LOGIN'))
    print('1. For admin')
    print('2. For user')
    print('3. Exit')
    print('-----------------')
    a = input('Enter your choice(1-3): ')
    if a=='3':
        print('\nExiting the program')
        exit()
    pwd=input('Enter password : ')

    if a=='2' and pwd=='123':
        client()
    elif a=='1' and pwd=='123':
        admin()
    else:
        os.system('cls')
        print('invalid credentials. please try again')
        time.sleep(1)
        os.system('cls')
        login()
def admin():
    while True:
        try:
            os.system('cls')
            f = Figlet(font='ANSI_Shadow')
            print(f.renderText('RMS (ADMIN)'))
            print('1. Add new item to menu')
            print('2. change the price of an item')
            print('3. Delete item from menu')
            print('4. return to login')
            print('5. exit')
            a = int(input('\nEnter your choice (1-5): '))

            if a == 1:
                os.system('cls')
                create()
            elif a == 2:
                os.system('cls')
                update_price()
            elif a == 3:
                os.system('cls')
                delete()
            elif a == 4:
                os.system('cls')
                login()
            elif a == 5:
                print('\nExiting the program')
                break
            else:
                print('\nInvalid choice. Please choose a valid option')
                time.sleep(1.8)

        except:
            print("Invalid input. Please enter a number between 1 and 5.")
            time.sleep(1.8)


def client():
    while True:
        try:
            os.system('cls')
            f = Figlet(font='ANSI_Shadow')
            print(f.renderText('RMS (USER)'))
            print('1. Create new bill')
            print('2. Return to the login page')
            print('3. Exit')
            a = int(input('\nEnter your choice (1-3): '))

            if a == 1:
                os.system('cls')
                order()
            elif a == 2:
                os.system('cls')
                login()
            elif a == 3:
                print('\nExiting the program')
                break
            elif a>=4:
                print("Invalid input. Please enter a number between 1 and 3.")
                time.sleep(1.7)
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 3.")
            time.sleep(1.7)
        except Exception as e:
            print(f"An error occurred: {e}")
            time.sleep(1.7)

def order():
    try:
        cur.execute("CREATE TABLE IF NOT EXISTS _order(item_id INT, item_name CHAR(40), qty CHAR(2), price INT(4))")
        cur.execute("SELECT item_id, ITEM_NAME, PRICE FROM Menu")
        d = cur.fetchall()
        c = 0

        while True:
            f = Figlet(font='ANSI_Shadow')
            print(f.renderText('MENU'))
            for i in d:
                print(i[0], '-', i[1], '->', '₹', i[2])
            c += 1

            a = input('\nEnter the item number (or type "exit" to return to main menu): ')
            if a.lower() == "exit":
                print("\nReturning to main menu.")
                return  # Exit to the main menu

            cur.execute("SELECT ITEM_NAME, PRICE FROM Menu WHERE item_id=%s", (a,))
            q = cur.fetchall()
            if not q:
                os.system('cls')
                print("\nInvalid item number.")
                time.sleep(1)
                os.system('cls')
                continue

            it = q[0][0]
            quan = int(input('Enter quantity: '))
            pri = q[0][1] * quan
            cur.execute("INSERT INTO _order VALUES (%s, %s, %s, %s)", (c, it, quan, pri))
            mycon.commit()

            ch = input('\nAdd more items? (y/n): ')
            if ch.lower() == 'n':
                break
            os.system('cls')

        os.system('cls')
        f = Figlet(font='ANSI_Shadow')
        print(f.renderText('BILL'))
        cur.execute('SELECT item_id, item_name, price, qty FROM _order')
        order = cur.fetchall()
        for i in order:
            print(i[0], i[1], 'x' + i[3], '->', '₹', i[2])
        
        print('---------------------')
        print('Total', '->', '₹', sum(i[2] for i in order))

        cur.execute("DROP TABLE _order")
        mycon.commit()

        input('\nPress Enter to continue')
    except sql.Error as e:
        print(f"Database error: {e}")
    except ValueError:
        print("Invalid input. Please enter a valid quantity.")
        time.sleep(1.8)
    except Exception as e:
        print(f"An error occurred: {e}")
        time.sleep(1.8)


def create():
    try:
        while True:
            os.system('cls')
            cur.execute("SELECT * FROM menu")
            f = cur.fetchall()
            q = 1 + len(f)
            a = input('\nEnter the item to be added: ')
            p = int(input('Enter price: '))
            cur.execute('INSERT INTO menu VALUES (%s, "%s", %s)'% (q, a, p))
            mycon.commit()
            print('\nItem added successfully.')
            ch = input('\nAdd more items? (y/n): ')
            if ch.lower() == 'n':
                break
    except sql.Error as e:
        print(f"Database error: {e}")
    except ValueError:
        print("Invalid input. Price must be a number.")
    except Exception as e:
        print(f"An error occurred: {e}")

def update_price():
    try:
        os.system('cls')
        cur.execute('SELECT item_name, price FROM menu')
        items = cur.fetchall()

        if not items:
            print("No items in the menu to update.")
            return


        f = Figlet(font='ANSI_Shadow')
        print(f.renderText('MENU'))
        for item in items:
            print(f"{item[0]} - ₹{item[1]}")

        item_name = input('\nEnter the name of the item to update the price: ')
        cur.execute("SELECT * FROM menu WHERE item_name=%s", (item_name,))
        item = cur.fetchone()

        
        if item:
            
            new_price = int(input('Enter the new price: '))
            Z=input('Are you sure want to change (enter to confirm)')
            cur.execute("UPDATE menu SET price=%s WHERE item_name=%s", (new_price, item_name))
            mycon.commit()
            print(f"\nPrice of '{item_name}' updated to ₹{new_price}.")
        else:
            print("\nItem not found in the menu.")

        input('\nPress Enter to continue')
    except sql.Error as e:
        print(f"Database error: {e}")
    except ValueError:
        print("Invalid input. Price must be a number.")
    except Exception as e:
        print(f"An error occurred: {e}")
        time

def delete():
    try:
        cur.execute('SELECT item_name FROM menu')
        c = cur.fetchall()
        if not c:
            print("No items in the menu to delete.")
            return

        for i in c:
            print(i[0])

        d = input('Enter the item to be deleted: ')
        Z=input('Are you sure want to change (enter to confirm)')

        found = False
        for i in c:
            if d in i:
                cur.execute('DELETE FROM menu WHERE item_name=%s', (d,))
                mycon.commit()
                print('\nItem deleted.')
                found = True
                break
        if not found:
            print('\nItem not found.')

        input('Press Enter to continue')
    except sql.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

time.sleep(0.5)
login()  
