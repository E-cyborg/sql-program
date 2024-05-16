from tkinter import *
import tkinter as tk
import mysql.connector as sql
from mysql.connector import Error
from tkinter import messagebox
import webbrowser
import pyttsx3

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
    def clear_the_screen(self):
        for item in root.winfo_children():
            item.destroy()
        self.second_window()
        try:
            if code is not None:
                self.code_text.insert("1.0", code) 
        except NameError:
            pass 

        self.second_window()

    def second_window(self):
        main_class_instance = Main()
        main_class_instance.menu_bar()
        data_label = tk.Label(root, text="Database", font=("TkDefaultFont", 15))
        data_label.place(x=0, y=0)
        code_lable=tk.Label(root,text='code here')
        code_lable.place(x=150,y=30)
        cursor.execute('SHOW DATABASES')
        databases = cursor.fetchall()
        global dbase
        dbase = Listbox(root)
        for index, db in enumerate(databases):
            dbase.insert(index, db[0])
        dbase.bind("<<ListboxSelect>>", self.selected_database)
        dbase.place(x=0, y=25)
        self.text_of_second_window()
        self.reload_button()

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
        self.attributes_of_table()

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

    def text_of_second_window(self):
        global code_text
        self.code_text = Text(root, height=20, width=140, background="lightblue")
        self.code_text.place(x=150, y=50)
        self.run_of_second_window()

    def getting_the_text(self):   
        global code
        code = self.code_text.get("1.0", "end-1c")
        if 'select' in code:
            self.checking_the_select_command()
        self.running_the_input_code()

    def running_the_input_code(self):
        global output_error
        try:
            cursor.execute(code)
            cursor.fetchall()
            output_text_box.config(state='normal')
            output_text_box.insert(tk.END, 'Success' + '\n')
            output_text_box.config(state='disabled')
        except Error as e:
            output_error=e
            self.output_of_the_input_comm(e)
        except NameError:
            output_error="Success"
            self.output_of_the_input_comm(output_error)

    def output_of_the_input_comm(self,e):
        global output_text_box
        # if 'output_text_box' not in globals():
        output_text_box = tk.Text(root, height=10, width=140, background="lightyellow")
        output_text_box.config(state='normal')
        output_text_box.place(x=150, y=400)
        output_text_box.config(state='normal')
        output_text_box.insert(tk.END, str(e) + '\n')
        output_text_box.config(state='disabled')
        self.clear_button_of_output_box()

    def clear_button_of_output_box(self):
        clear_button=tk.Button(text='clear',command=self.clearing_output_box)
        clear_button.place(x=1400, y=30,width=120)

    def clearing_output_box(self):
        output_text_box.config(state='normal')
        output_text_box.delete("1.0", tk.END)
        output_text_box.config(state='disabled')

    def reload_button(self):
        global reload
        reload=tk.Button(root,text="full Reload",command=self.clear_the_screen)
        reload.place(x=1430,y=70)
        
    def checking_the_select_command(self):
        if 'select' in code:
            for line in code.split('\n'):
                if line.strip().lower().startswith('select'):
                    select = tk.Tk()
                    try:
                        cursor.execute(line)    
                        result = cursor.fetchall()
                        select_box = Text(select, height=20, width=150)
                        if result:
                            column_widths = [max(len(str(item)) for item in col) for col in zip(*result)]
                            select_box.insert(END, ' | '.join([f'{col:<{width}}' for col, width in zip(column_names, column_widths)]))
                            select_box.insert(END, '\n')
                            for row in result:
                                select_box.insert(END, ' | '.join([f'{str(item):<{width}}' for item, width in zip(row, column_widths)]))
                                select_box.insert(END, '\n')
                        else:
                            select_box.insert(END, 'Table is empty')
                        select_box.pack()
                        select_box.config(state='disabled')
                        select.mainloop()
                    except Error as e:
                        self.output_of_the_input_comm(e)

if __name__ == "__main__":
    announce = pyttsx3.init()
    announce.say("This program is made by E cyborg. If you have any questions, ask me on GitHub.")
    announce.runAndWait()
    a = Main()
    a.main()
