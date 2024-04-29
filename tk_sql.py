from tkinter import *
import tkinter as tk
import mysql.connector as sql
from mysql.connector import Error
from tkinter import messagebox
import webbrowser

class Main:
    def menu_bar(self):
        menu_bar = tk.Menu(root)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Help", command=self.help_of_self)
        menu_bar.add_cascade(label="Menu", menu=file_menu)
        root.config(menu=menu_bar)

    def help_of_self(self):
        url = 'https://github.com/E-cyborg'
        webbrowser.open(url)

    def main(self):
        global root
        root = tk.Tk()
        root.geometry("1500x800")
        self.first_window(root)
        self.menu_bar()
        root.mainloop()

    def first_window(self, root):
        intro = tk.Label(text="Welcome to SQL program", font=("TkDefaultFont", 20))
        intro.pack(fill=tk.BOTH, expand=True)
        intro.place(x=600, y=250)

        a = tk.Label(text="Host Name", font=("TkDefaultFont", 10))
        b = tk.Label(text="User Name", font=("TkDefaultFont", 10))
        c = tk.Label(text="Password", font=("TkDefaultFont", 10))
        a.place(x=650, y=300)
        b.place(x=650, y=320)
        c.place(x=650, y=340)

        h_name = tk.Entry(root)
        U_name = tk.Entry(root)
        global pasword
        pasword = tk.Entry(root, show="*")
        h_name.insert(0, "localhost")
        U_name.insert(0, "root")
        pasword.insert(0,'rgwejgccg&!**&YRY')
        h_name.place(x=750, y=300)
        U_name.place(x=750, y=320)
        pasword.place(x=750, y=340)

        global pass_button
        pass_button = tk.Button(text="Show", command=self.show_hide)
        pass_button.place(x=900, y=340)

        sub = tk.Button(text="Submit", width=20, command=lambda: self.getting_the_entered_info(h_name, U_name, pasword))
        sub.place(x=700, y=400)

    def show_hide(self):
        if pasword.cget("show") == "":
            pasword.config(show="*")
            pass_button.config(text="Show")
        else:
            pasword.config(show="")
            pass_button.config(text="Hide")

    def getting_the_entered_info(self, h, u, p):
        host = h.get()
        user = u.get()
        passwrd = p.get()
        self.sql_check(host, user, passwrd)

    def sql_check(self, h, u, p):
        global connection, cursor  
        try:
            connection = sql.connect(host=h, user=u, passwd=p)
            cursor = connection.cursor()
            messagebox.showinfo("Success", "Connected to MySQL Database!")
            self.clear_the_screen()
            table_calling_instance = table()
            table_calling_instance.second_window()
        except Error as e:
            messagebox.showerror("Error", str(e))

    def clear_the_screen(self):
        for item in root.winfo_children():
            item.destroy()

class table:
    def second_window(self):
        main_class_instance = Main()
        main_class_instance.menu_bar()
        data_label = tk.Label(root, text="Database", font=("TkDefaultFont", 15))
        data_label.place(x=0, y=0)
        cursor.execute('SHOW DATABASES')
        databases = cursor.fetchall()

        dbase = Listbox(root)
        for index, db in enumerate(databases):
            dbase.insert(index, db[0])
        dbase.bind("<<ListboxSelect>>", self.selected_database)
        dbase.place(x=0, y=25)
        
    def selected_database(self, event):
        selected_index = event.widget.curselection()
        if selected_index:
            global selected_db
            selected_db = event.widget.get(selected_index[0])
            self.show_table(selected_db)

    def show_table(self, s_db):
        table_label = tk.Label(root, text="Tables", font=("TkDefaultFont", 15))
        table_label.place(x=0, y=190)
        table_list = Listbox(root)
        if s_db:
            cursor.execute(f'USE {s_db}')
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            for index, table in enumerate(tables):
                table_list.insert(index, table[0])
        else:
            table_list.insert(0, "Database not selected")
        table_list.bind("<<ListboxSelect>>", self.selected_table)
        table_list.place(x=0, y=230)

    def selected_table(self, event):
        selected_index = event.widget.curselection()
        
        if selected_index:
            global selected_tb
            selected_tb = event.widget.get(selected_index[0])
            self.text_of_second_window(selected_db, selected_tb)

    def attributes_of_table(self):
        colum_lable=tk.Label(text="Columns", font=("TkDefaultFont", 15))
        colum_lable.place(x=0,y=400)
        global column_names
        query = f"SELECT column_name FROM information_schema.columns WHERE table_schema = '{selected_db}' AND table_name = '{selected_tb}'"
        cursor.execute(query)
        columns = cursor.fetchall()
        column_names = [column[0] for column in columns]
        attribut=tk.Listbox(root)
        for index,col in enumerate(column_names):
            attribut.insert(index,col)
        attribut.place(x=0,y=450)


    def run_of_second_window(self):
        self.run_button = tk.Button(text="Run", command=self.getting_the_text)
        self.run_button.place(x=1400, y=0,width=120)

    def text_of_second_window(self, s_db, s_t):
        self.code_text = Text(root, height=20, width=150, background="lightblue")
        self.code_text.place(x=150, y=50)
        self.run_of_second_window()

        
    def getting_the_text(self):   
        global code  
        code = self.code_text.get("1.0", "end-1c")
        self.running_the_input_code()

    def running_the_input_code(self):
        try:
            cursor.execute(code)
        except Error as e:
            messagebox.showerror('Error', str(e))

    def close_connection(self):
        global connection, cursor
        cursor.close()
        connection.close()

if __name__ == "__main__":
    a = Main()
    a.main()
