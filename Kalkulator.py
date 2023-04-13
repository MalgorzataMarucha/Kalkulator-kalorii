import tkinter as tk
from tkinter import ttk
from tkinter import *
import os

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Kalkulator kalorii")
        self.option_add("*tearOff", False)

    def set_window_position(self):
        self.height = 700
        self.width = 500
        screen_width = self.winfo_screenwidth()  
        screen_height = self.winfo_screenheight() 
        self.x = (screen_width/2) - (self.width/2)
        self.y = (screen_height/2) - (self.height/2)
        self.geometry('%dx%d+%d+%d' % (self.width, self.height, self.x, self.y))
        
    def set_theme(self):
        self.style = ttk.Style(self)
        file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "forest-dark.tcl")
        self.tk.call("source", file_path)
        self.style.theme_use("forest-dark")
    def menu(self):

        Makro = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]

        treeFrame = ttk.Frame(self)
        treeFrame.grid(pady=self.height/4)
        self.style.configure('Treeview',rowheight=70)
        
        treeScroll = ttk.Scrollbar(treeFrame)
        treeScroll.pack(side="right", fill="y")

        treeview = ttk.Treeview(treeFrame, selectmode="extended", yscrollcommand=treeScroll.set, columns=(1, 2, 3, 4), height=5)
        treeview.pack(expand=True, fill="both")
    
        treeScroll.config(command=treeview.yview)

        # Treeview columns
        treeview.column("#0", width=round(self.width/3))
        treeview.column(1, anchor="center", width=round(0.67*self.width/4.7))
        treeview.column(2, anchor="center", width=round(0.67*self.width/4.7))
        treeview.column(3, anchor="center", width=round(0.67*self.width/4.7))
        treeview.column(4, anchor="center", width=round(0.67*self.width/4.7))
       
        # Treeview headings
        treeview.heading("#0", text="Posiłek")
        treeview.heading(1, text="Kcal")
        treeview.heading(2, text="B")
        treeview.heading(3, text="T")
        treeview.heading(4, text="W")

        # Define treeview data
        treeview_data = [
            ("", "end", 1, "Śniadanie", (str(Makro[1][0]), str(Makro[1][1]),str(Makro[1][2]),str(Makro[1][3]))),
            ("", "end", 2, "Drugie Śniadanie", (str(Makro[2][0]), str(Makro[2][1]),str(Makro[2][2]),str(Makro[2][3]))),
            ("", "end", 3, "Obiad", (str(Makro[3][0]), str(Makro[3][1]),str(Makro[3][2]),str(Makro[3][3]))),
            ("", "end", 4, "Przekąska", (str(Makro[4][0]), str(Makro[4][1]),str(Makro[4][2]),str(Makro[4][3]))),
            ("", "end", 5, "Kolacja", (str(Makro[5][0]), str(Makro[5][1]),str(Makro[5][2]),str(Makro[5][3]))),
        ]

        # Insert treeview data
        for item in treeview_data:
            treeview.insert(parent=item[0], index=item[1], iid=item[2], text=item[3], values=item[4])
            if item[0] == "":
                treeview.item(item[2], open=True) # Open parents
                
        # Select and scroll
        treeview.selection_set(2)
        treeview.see(3)

        add_frame = ttk.LabelFrame(self, text="Dodaj posiłek")
        add_frame.place(x=0,y=590,width=500,height=110)

        button1 = ttk.Button(add_frame, text="Śniadanie",command=self.LookForMeal)
        button1.grid(row=0, column=0, padx=10, pady=0)

        button2 = ttk.Button(add_frame, text="Drugie śniadanie",command=self.LookForMeal)
        button2.grid(row=0, column=1, padx=10, pady=0)

        button3 = ttk.Button(add_frame, text="Obiad",command=self.LookForMeal)
        button3.grid(row=0, column=2, padx=10, pady=0)

        button4 = ttk.Button(add_frame, text="Przekąska",command=self.LookForMeal)
        button4.grid(row=1, column=0, padx=10, pady=10)

        button5 = ttk.Button(add_frame, text="Kolacja",command=self.LookForMeal)
        button5.grid(row=1, column=1, padx=10, pady=10)

        options_frame = ttk.LabelFrame(self,text="Opcje")
        options_frame.place(x=0,y=0,width=250,height=170)

        Settings_button = ttk.Button(options_frame, text="Ustawienia" )
        Settings_button.pack(side="left", padx=10, pady=0)

        Calendar_button = ttk.Button(options_frame, text="Kalendarz")
        Calendar_button.pack(side="left", padx=10, pady=0)

        macro_frame = ttk.LabelFrame(self,text="Makro")
        macro_frame.place(x=250,y=0,width=250,height=170)

        kcal_label = ttk.Label(macro_frame, text="Kcal: " + str(Makro[0][0]))
        kcal_label.pack(side="top", padx=10, pady=10)

        B_label = ttk.Label(macro_frame, text="Białko: " + str(Makro[0][1]))
        B_label.pack(side="top", padx=10, pady=10)

        T_label = ttk.Label(macro_frame, text="Tłuszcze: " + str(Makro[0][2]))
        T_label.pack(side="top", padx=10, pady=10)

        W_label = ttk.Label(macro_frame, text="Węglowodany: " + str(Makro[0][3]))
        W_label.pack(side="top", padx=10, pady=10)

    def LookForMeal(self):
        self.withdraw()
        new_window = tk.Toplevel(self)
        new_window.title("Szukaj produktu")
        new_window.geometry('%dx%d+%d+%d' % (self.width, self.height, self.x, self.y))
        folder_path = os.path.join(os.path.dirname(__file__), "Dania")
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        
        search_frame = ttk.LabelFrame(new_window,text="Szukaj produktu")
        search_frame.place(x=0,y=0,width=500,height=130)

        entry = ttk.Entry(search_frame, width=100)
        def clear_entry(event):
            if entry.get() == "Wyszukaj produkt":
                entry.delete(0, tk.END)

        def searchMeals(event):
            for widget in result_frame.winfo_children():
                widget.destroy()
            product = entry.get()
            file_path = os.path.join(folder_path, product+".txt")
            if os.path.exists(file_path):
                ttk.Label(result_frame, text=product).pack(side="top", padx=10, pady=10)
            else:
                ttk.Label(result_frame, text="Brak wyników wyszukiwania. Dodaj produkt.").pack(side="top", padx=10, pady=10)

        entry.insert(0, "Wyszukaj produkt")
        entry.bind("<FocusIn>", clear_entry)
        entry.bind("<Return>", searchMeals)
        entry.pack(side="left", padx=100, pady=10)

        result_frame = ttk.LabelFrame(new_window,text="Wyniki wyszukiwania")
        result_frame.place(x=0,y=140,width=500,height=400)

        options_frame = ttk.LabelFrame(new_window,text="Dodaj nowy posiłek")
        options_frame.place(x=0,y=550,width=500,height=150)

        AddMeal = ttk.Button(options_frame, text="Dodaj nowy produkt")
        AddMeal.pack(side="left",padx=60, pady=10)

        ScanMeal = ttk.Button(options_frame, text="Zeskajnuj produkt")
        ScanMeal.pack(side="left",padx=50, pady=10)


        def on_closing():
            self.deiconify()
            new_window.destroy()

        new_window.protocol("WM_DELETE_WINDOW", on_closing)

if __name__ == "__main__":
    app = App()
    app.set_window_position()
    app.set_theme()
    app.menu()
    app.mainloop()