import tkinter as tk
from tkinter import ttk
from tkinter import *
import os
import re

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

        self.Makro = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        self.buttonID = 0

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
            ("", "end", 1, "Śniadanie", (str(self.Makro[1][0]), str(self.Makro[1][1]),str(self.Makro[1][2]),str(self.Makro[1][3]))),
            ("", "end", 2, "Drugie Śniadanie", (str(self.Makro[2][0]), str(self.Makro[2][1]),str(self.Makro[2][2]),str(self.Makro[2][3]))),
            ("", "end", 3, "Obiad", (str(self.Makro[3][0]), str(self.Makro[3][1]),str(self.Makro[3][2]),str(self.Makro[3][3]))),
            ("", "end", 4, "Przekąska", (str(self.Makro[4][0]), str(self.Makro[4][1]),str(self.Makro[4][2]),str(self.Makro[4][3]))),
            ("", "end", 5, "Kolacja", (str(self.Makro[5][0]), str(self.Makro[5][1]),str(self.Makro[5][2]),str(self.Makro[5][3]))),
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

        button1 = ttk.Button(add_frame, text="Śniadanie",command=lambda:[self.LookForMeal(),self.whichButton(1)])
        button1.grid(row=0, column=0, padx=10, pady=0)

        button2 = ttk.Button(add_frame, text="Drugie śniadanie",command=lambda:[self.LookForMeal(),self.whichButton(2)])
        button2.grid(row=0, column=1, padx=10, pady=0)

        button3 = ttk.Button(add_frame, text="Obiad",command=lambda:[self.LookForMeal(),self.whichButton(3)])
        button3.grid(row=0, column=2, padx=10, pady=0)

        button4 = ttk.Button(add_frame, text="Przekąska",command=lambda:[self.LookForMeal(),self.whichButton(4)])
        button4.grid(row=1, column=0, padx=10, pady=10)

        button5 = ttk.Button(add_frame, text="Kolacja",command=lambda:[self.LookForMeal(),self.whichButton(5)])
        button5.grid(row=1, column=1, padx=10, pady=10)

        options_frame = ttk.LabelFrame(self,text="Opcje")
        options_frame.place(x=0,y=0,width=250,height=170)

        Settings_button = ttk.Button(options_frame, text="Ustawienia" )
        Settings_button.pack(side="left", padx=10, pady=0)

        Calendar_button = ttk.Button(options_frame, text="Kalendarz")
        Calendar_button.pack(side="left", padx=10, pady=0)

        macro_frame = ttk.LabelFrame(self,text="Makro")
        macro_frame.place(x=250,y=0,width=250,height=170)

        kcal_label = ttk.Label(macro_frame, text="Kcal: " + str(self.Makro[0][0]))
        kcal_label.pack(side="top", padx=10, pady=10)

        B_label = ttk.Label(macro_frame, text="Białko: " + str(self.Makro[0][1]))
        B_label.pack(side="top", padx=10, pady=10)

        T_label = ttk.Label(macro_frame, text="Tłuszcze: " + str(self.Makro[0][2]))
        T_label.pack(side="top", padx=10, pady=10)

        W_label = ttk.Label(macro_frame, text="Węglowodany: " + str(self.Makro[0][3]))
        W_label.pack(side="top", padx=10, pady=10)
    
    def whichButton(self,Button):
        if Button == 1:
            self.buttonID = 1
        elif Button == 2:
            self.buttonID = 2
        elif Button == 3:
            self.buttonID = 3
        elif Button == 4:
            self.buttonID = 4
        elif Button == 5:
            self.buttonID = 5    

    def clear_entry(self, event, entry):
        if entry.get() in ["Wyszukaj produkt", "0"]:
            entry.delete(0, tk.END)

    def LookForMeal(self):
        window = self
        window.withdraw()
        new_window = tk.Toplevel(self)
        new_window.title("Szukaj produktu")
        new_window.geometry('%dx%d+%d+%d' % (self.width, self.height, self.x, self.y))
        self.folder_path = os.path.join(os.path.dirname(__file__), "Dania")
        if not os.path.exists(self.folder_path):
            os.makedirs(self.folder_path)
        
        search_frame = ttk.LabelFrame(new_window,text="Szukaj produktu")
        search_frame.place(x=0,y=0,width=500,height=130)

        entry = ttk.Entry(search_frame, width=100)
        self.selected = ""

        def searchMeals(event):
            for widget in result_frame.winfo_children():
                widget.destroy()
            product = entry.get()
            matching_files = [file for file in os.listdir(self.folder_path) if re.search(product, file, re.IGNORECASE)]
            if matching_files:
                for file in matching_files:
                    label = ttk.Label(result_frame, text=file[:-4])
                    label.pack(side="top", padx=10, pady=10)
                    label.bind("<Button-1>", lambda event, new_window=new_window, file=file: self.AddProduct(event, new_window, file[:-4]))
            else:
                label = ttk.Label(result_frame, text="Brak wyników wyszukiwania. Dodaj produkt.")
                label.pack(side="top", padx=10, pady=10)


        entry.insert(0, "Wyszukaj produkt")
        entry.bind("<FocusIn>", lambda event, entry=entry: self.clear_entry(event, entry))
        entry.bind("<Return>", searchMeals)
        entry.pack(side="left", padx=100, pady=10)

        result_frame = ttk.LabelFrame(new_window,text="Wyniki wyszukiwania")
        result_frame.place(x=0,y=140,width=500,height=400)

        Scroll = ttk.Scrollbar(result_frame)
        Scroll.pack(side="right", fill="y")

        options_frame = ttk.LabelFrame(new_window,text="Dodaj nowy posiłek")
        options_frame.place(x=0,y=550,width=500,height=150)

        AddMeal = ttk.Button(options_frame, text="Dodaj nowy produkt",command=lambda:[self.CreateNewProduct(new_window)])
        AddMeal.pack(side="left",padx=60, pady=10)

        ScanMeal = ttk.Button(options_frame, text="Zeskajnuj produkt")
        ScanMeal.pack(side="left",padx=50, pady=10)

        new_window.protocol("WM_DELETE_WINDOW", lambda: self.on_closing(window,new_window))
    

    def AddProduct(self,event,window,name):
        window.withdraw()
        new_window = tk.Toplevel(self)
        new_window.title("Dodaj produkt")
        new_window.geometry('%dx%d+%d+%d' % (self.width, self.height, self.x, self.y))

        ProductName = ttk.Label(new_window,text=name,justify="center",font=("Arial", 25))
        ProductName.pack(side="top",padx=30,pady=20)

        options_frame = ttk.LabelFrame(new_window,text="Wybierz wartość")
        options_frame.place(x=0,y=80,width=500,height=200)

        ProductInfo = ttk.Label(new_window,text="Wartości odżywcze",justify="center")
        ProductInfo.pack(side="top",padx=30,pady=210)


        def show_file_content():
            file_path = os.path.join(self.folder_path, name + ".txt")
            with open(file_path, 'r') as f:
                content = f.read()
                ProductInfo.config(text=content)
            
        ProductInfo.bind("<Button-1>", lambda event: show_file_content())

        file_path = os.path.join(self.folder_path, name + ".txt")
        with open(file_path, "r") as f:
            lines = f.readlines()
            for line in lines:
                if line.find('Opakowanie') != -1:
                    pack_g = [int(s) for s in re.findall(r'\b\d+\b', line)]
                    pack_g = pack_g[0]
                elif line.find('kcal') != -1:
                    kcal_100g = [int(s) for s in re.findall(r'\b\d+\b', line)]
                    kcal_100g = kcal_100g[0]
                elif line.find('Tłuszcze:') != -1:
                    Tłu_100g = [int(s) for s in re.findall(r'\b\d+\b', line)]
                    Tłu_100g = Tłu_100g[0]
                elif line.find('Węglowodany') != -1:
                    Węgl_100g = [int(s) for s in re.findall(r'\b\d+\b', line)]
                    Węgl_100g=Węgl_100g[0]
                elif line.find('Białka') != -1:
                    Biał_100g = [int(s) for s in re.findall(r'\b\d+\b', line)]
                    Biał_100g=Biał_100g[0]
        
        def display_selected(variable):
            option = variable.get()
            how_much = entry.get()
            if option == " Opakowanie ":
                chosen_kcal = pack_g * kcal_100g / 100 * float(how_much)
            elif option == " g":
                chosen_kcal = float(how_much) * kcal_100g / 100
            label_chosen_kcal.config(text=str(chosen_kcal))
        
        def print_selected_option():
            return (chosen_option.get())

        chosen_kcal = 0
        chosen_option = tk.IntVar(value=2)
        validation = new_window.register(self.only_numbers)
        option_menu_list = ["", " Opakowanie ", " g"]
        texts = [["1x Opakowanie", pack_g, pack_g*kcal_100g/100, ""], ["100 g", "100 g", kcal_100g, ""], ["200 g", "200 g", 2*kcal_100g, ""], ["entry", "choose", "chosen_kcal", ""]]
        variable = tk.StringVar(value=option_menu_list[1])
        
        for i in range(len(texts)):
            for j in range(len(texts[i])):
                if texts[i][j] == "":
                    Radiobutton = ttk.Radiobutton(options_frame, text="", variable=chosen_option, value=i, command=print_selected_option)
                    Radiobutton.grid(row=i, column=j)
                elif texts[i][j] == "entry":
                    entry = tk.Entry(options_frame,validate="key", validatecommand=(validation, '%S'),justify="center")
                    entry.grid(row=i, column=j,padx=10)
                    entry.insert(0, "0")
                    entry.bind("<FocusIn>", lambda event, entry=entry: self.clear_entry(event, entry))
                    entry.bind("<Return>", lambda event: display_selected(variable))
                elif texts[i][j] == "choose":
                    optionmenu = ttk.OptionMenu(options_frame, variable, *option_menu_list, command=lambda choice: display_selected(variable))
                    optionmenu.grid(row=i, column=j, sticky="nsew")
                elif texts[i][j] == "chosen_kcal":
                    label_chosen_kcal = tk.Label(options_frame, text=str(chosen_kcal), height=2, width=15)
                    label_chosen_kcal.grid(row=i, column=j)
                else: 
                    label = tk.Label(options_frame, text=str(texts[i][j]), height=2, width=15)
                    label.grid(row=i, column=j)

        def MacroProduct(chosen_option):
            if(chosen_option==0):
                print(0)
            elif(chosen_option==1):
                print(1)
            elif(chosen_option==2):
                print(2)
            elif(chosen_option==3):
                print(3)

        SaveMeal = ttk.Button(new_window, text="Zapisz wybór",command=lambda: MacroProduct(print_selected_option()))
        SaveMeal.pack(side="bottom",padx=50, pady=0)

        new_window.protocol("WM_DELETE_WINDOW", lambda: self.on_closing(window,new_window))

    def on_closing(self,window,new_window):
            window.deiconify()
            window.buttonID = 0
            new_window.destroy()
    
    def only_numbers(self,char):
            return char.isdigit()

    def CreateNewProduct(self,window):
        window.withdraw()
        new_window = tk.Toplevel(self)
        new_window.title("Dodaj nowy produkt")
        new_window.geometry('%dx%d+%d+%d' % (self.width, self.height, self.x, self.y))

        frame1 = ttk.LabelFrame(new_window,text="Informacje")
        frame1.place(x=0,y=0,width=500,height=620)

        self.label_texts = ["Nazwa","Wartości odżywcze na 100g:","Opakowanie ma", "Wartość energetyczna","Tłuszcze","Tłuszcze nasycone","Węglowodany","Cukry","Błonnik","Białka","Sól"]
        self.label_texts2 = ["","","g/ml","kcal","g","g","g","g","g","g","g"]


        validation = new_window.register(self.only_numbers)

        for i, text in enumerate(self.label_texts):
            label = tk.Label(frame1, text=text,height=3,width=30)
            label.grid(row=i, column=0)

            if text != "Wartości odżywcze na 100g:":
                if text == "Nazwa":
                    entry = tk.Entry(frame1)
                    entry.grid(row=i, column=1)
                else:
                    entry = tk.Entry(frame1,validate="key", validatecommand=(validation, '%S'))
                    entry.grid(row=i, column=1)
                    entry.insert(0, "0")
                    entry.bind("<FocusIn>", lambda event, entry=entry: self.clear_entry(event, entry))
            
            label2 = tk.Label(frame1, text=self.label_texts2[i],height=3,width=10)
            label2.grid(row=i, column=2)

        SaveButton = ttk.Button(new_window, text="Zapisz produkt",command=lambda:[self.SaveProduct(frame1),self.on_closing(window,new_window)])
        SaveButton.pack(side="bottom",padx=60, pady=20)

        new_window.protocol("WM_DELETE_WINDOW", lambda: self.on_closing(window,new_window))

    def SaveProduct(self, frame):
        filename = ""
        entries = []

        for child in frame.winfo_children():
            if isinstance(child, tk.Label) and child["text"] == "Nazwa":
                for subchild in frame.winfo_children():
                    if isinstance(subchild, tk.Entry) and subchild.master == child.master:
                        filename = subchild.get()
                        break
                break

        if filename != "":
            file_path = os.path.join(self.folder_path, filename + ".txt")
            with open(file_path, "w") as f:
                for child in frame.winfo_children():
                    if isinstance(child, tk.Label) and child["text"] != "Nazwa" and child["text"] in self.label_texts:
                        text = child["text"]
                        row_num = child.grid_info()["row"]
                        for subchild2 in frame.winfo_children():
                            if isinstance(subchild2, tk.Label) and subchild2["text"] in self.label_texts2 and subchild2.grid_info()["row"] == row_num:
                                text2=" "+subchild2["text"]
                                for subchild in frame.winfo_children():
                                    if isinstance(subchild, tk.Entry) and subchild.master == child.master and subchild.grid_info()["row"] == row_num:
                                        f.write(text + ": " + subchild.get() + text2 +"\n")
                                        break




if __name__ == "__main__":
    app = App()
    app.set_window_position()
    app.set_theme()
    app.menu()
    app.mainloop()