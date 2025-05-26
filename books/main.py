import tkinter as tk
from user_interface import user_login_register
from admin_interface import admin_login
from admin_interface import cashier_login

def main_menu():
    root = tk.Tk()
    root.title("Добро пожаловать в систему книжного магазина")

    tk.Label(root, text="Выберите режим").pack(pady=10)

    tk.Button(root, text="Покупатель", width=30, command=lambda: [root.destroy(), user_login_register()]).pack(pady=5)
    tk.Button(root, text="Кассир", width=30, command=lambda: [root.destroy(), cashier_login()]).pack(pady=5)
    tk.Button(root, text="Администратор", width=30, command=lambda: [root.destroy(), admin_login()]).pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main_menu()