import tkinter as tk
from tkinter import ttk
from tkinter import *
import os
import re
import json

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

        self.treeview = ttk.Treeview(treeFrame, selectmode="extended", yscrollcommand=treeScroll.set, columns=(1, 2, 3, 4), height=5)
        self.treeview.pack(expand=True, fill="both")
    
        treeScroll.config(command=self.treeview.yview)

        # Treeview columns
        self.treeview.column("#0", width=round(self.width/3))
        self.treeview.column(1, anchor="center", width=round(0.67*self.width/4.7))
        self.treeview.column(2, anchor="center", width=round(0.67*self.width/4.7))
        self.treeview.column(3, anchor="center", width=round(0.67*self.width/4.7))
        self.treeview.column(4, anchor="center", width=round(0.67*self.width/4.7))
       
        # Treeview headings
        self.treeview.heading("#0", text="Posiłek")
        self.treeview.heading(1, text="Kcal")
        self.treeview.heading(2, text="B")
        self.treeview.heading(3, text="T")
        self.treeview.heading(4, text="W")

        # Define treeview data
        treeview_data = [
            ("", "end", 1, "Śniadanie", (self.Makro[1][0], self.Makro[1][1],self.Makro[1][2],self.Makro[1][3])),
            ("", "end", 2, "Drugie Śniadanie", (self.Makro[2][0], self.Makro[2][1],self.Makro[2][2],self.Makro[2][3])),
            ("", "end", 3, "Obiad", (self.Makro[3][0], self.Makro[3][1],self.Makro[3][2],self.Makro[3][3])),
            ("", "end", 4, "Przekąska", (self.Makro[4][0], self.Makro[4][1],self.Makro[4][2],self.Makro[4][3])),
            ("", "end", 5, "Kolacja", (self.Makro[5][0], self.Makro[5][1],self.Makro[5][2],self.Makro[5][3])),
        ]

        # Insert treeview data
        for item in treeview_data:
            self.treeview.insert(parent=item[0], index=item[1], iid=item[2], text=item[3], values=item[4])
            if item[0] == "":
                self.treeview.item(item[2], open=True) # Open parents
                
        # Select and scroll
        self.treeview.selection_set(2)
        self.treeview.see(3)
        

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

        self.kcal_label = ttk.Label(macro_frame, text="Kcal: " + str(self.Makro[0][0]))
        self.kcal_label.pack(side="top", padx=10, pady=10)

        self.B_label = ttk.Label(macro_frame, text="Białko: " + str(self.Makro[0][1]))
        self.B_label.pack(side="top", padx=10, pady=10)

        self.T_label = ttk.Label(macro_frame, text="Tłuszcze: " + str(self.Makro[0][2]))
        self.T_label.pack(side="top", padx=10, pady=10)

        self.W_label = ttk.Label(macro_frame, text="Węglowodany: " + str(self.Makro[0][3]))
        self.W_label.pack(side="top", padx=10, pady=10)

    def update_macro_labels(self):
        sum_kcal = sum(item[0] for item in self.Makro[1:])
        sum_B = sum(item[1] for item in self.Makro[1:])
        sum_T = sum(item[2] for item in self.Makro[1:])
        sum_W = sum(item[3] for item in self.Makro[1:])

        self.kcal_label.config(text="Kcal: " + str(sum_kcal))
        self.B_label.config(text="Białko: " + str(sum_B))
        self.T_label.config(text="Tłuszcze: " + str(sum_T))
        self.W_label.config(text="Węglowodany: " + str(sum_W))
        
    
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
        self.folder_path = os.path.join(os.path.dirname(__file__), "Informacje")
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
            file_path = os.path.join(self.folder_path, "Produkty.json")
            if os.path.exists(file_path):
                with open(file_path, "r") as f:
                    data = json.load(f)
                    matching_products = [name for name in data.keys() if re.search(product, name, re.IGNORECASE)]
                    if matching_products:
                        for name in matching_products:
                            label = ttk.Label(result_frame, text=name)
                            label.pack(side="top", padx=10, pady=10)
                            label.bind("<Button-1>", lambda event, new_window=new_window, name=name: self.AddProduct(event, new_window, name))
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
            file_path = os.path.join(self.folder_path, "Produkty.json")
            with open(file_path, 'r') as f:
                data = json.load(f)
                if name in data:
                    content = json.dumps(data[name], indent=4)
                    ProductInfo.config(text=content)

        ProductInfo.bind("<Button-1>", lambda event: show_file_content())

        file_path = os.path.join(self.folder_path, "Produkty.json")
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                data = json.load(f)
                if name in data:
                    values = data[name]
                    pack_g = [int(s) for s in re.findall(r'\b\d+\b', str(values.get("Opakowanie ma", 0)))][0]
                    kcal_100g = [int(s) for s in re.findall(r'\b\d+\b', str(values.get("Wartość energetyczna", 0)))][0]
                    Tłu_100g = [int(s) for s in re.findall(r'\b\d+\b', str(values.get("Tłuszcze", 0)))][0]
                    Węgl_100g = [int(s) for s in re.findall(r'\b\d+\b', str(values.get("Węglowodany", 0)))][0]
                    Biał_100g = [int(s) for s in re.findall(r'\b\d+\b', str(values.get("Białka", 0)))][0]
        
        def display_selected(variable):
            option = variable.get()
            how_much = entry.get()
            if option == " Opakowanie ":
                self.chosen_kcal = pack_g * kcal_100g / 100 * float(how_much)
                self.chosen_B = pack_g * Biał_100g / 100 * float(how_much)
                self.chosen_T = pack_g * Tłu_100g / 100 * float(how_much)
                self.chosen_W = pack_g * Węgl_100g / 100 * float(how_much)
            elif option == " g":
                self.chosen_kcal = float(how_much) * kcal_100g / 100
                self.chosen_B = float(how_much) * Biał_100g / 100
                self.chosen_T = float(how_much) * Tłu_100g / 100
                self.chosen_W = float(how_much) * Węgl_100g / 100
            label_chosen_kcal.config(text=str(self.chosen_kcal)+" kcal")
        
        def print_selected_option():
            return (chosen_option.get())

        self.chosen_kcal = 0
        self.chosen_B = 0
        self.chosen_T = 0
        self.chosen_W = 0
        chosen_option = tk.IntVar(value=2)
        validation = new_window.register(self.only_numbers)
        option_menu_list = ["", " Opakowanie ", " g"]
        texts = [["1x Opakowanie", str(pack_g)+" g", str(pack_g*kcal_100g/100) + " kcal", ""], 
                 ["100 g", "100 g", str(kcal_100g) + " kcal", ""], 
                 ["200 g", "200 g", str(2*kcal_100g) + "kcal", ""], ["entry", "choose", "chosen_kcal", ""]]
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
                    label_chosen_kcal = tk.Label(options_frame, text=str(self.chosen_kcal) + " kcal", height=2, width=15)
                    label_chosen_kcal.grid(row=i, column=j)
                else: 
                    label = tk.Label(options_frame, text=str(texts[i][j]), height=2, width=15)
                    label.grid(row=i, column=j)

        def MacroProduct(chosen_option):
            if(chosen_option==0):
                self.product_kcal = pack_g * kcal_100g/100
                self.product_B = pack_g * Biał_100g/100
                self.product_T = pack_g * Tłu_100g/100
                self.product_W = pack_g* Węgl_100g/100
            elif(chosen_option==1):
                self.product_kcal = kcal_100g
                self.product_B = Biał_100g
                self.product_T = Tłu_100g
                self.product_W = Węgl_100g
            elif(chosen_option==2):
                self.product_kcal = 2*kcal_100g
                self.product_B = 2*Biał_100g
                self.product_T = 2*Tłu_100g
                self.product_W = 2*Węgl_100g
            elif(chosen_option==3):
                self.product_kcal = self.chosen_kcal
                self.product_B = self.chosen_B
                self.product_T = self.chosen_T
                self.product_W = self.chosen_W

            self.Makro[self.buttonID][0] += self.product_kcal
            self.Makro[self.buttonID][1] += self.product_B
            self.Makro[self.buttonID][2] += self.product_T
            self.Makro[self.buttonID][3] += self.product_W

            

            self.treeview.insert(parent=self.buttonID, index="end", iid=None, text=name, 
                                 values=(self.product_kcal, self.product_B, self.product_T, self.product_W))
            self.treeview.item(self.buttonID, values=(self.Makro[self.buttonID][0], self.Makro[self.buttonID][1],
                                            self.Makro[self.buttonID][2], self.Makro[self.buttonID][3]))

            self.treeview.update()
            self.update_macro_labels()
            
            

        SaveMeal = ttk.Button(new_window, text="Zapisz wybór",
                              command=lambda:[MacroProduct(print_selected_option()),self.on_closing(window,new_window)])
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

        self.label_texts = ["Nazwa","Wartości odżywcze na 100g:","Opakowanie ma", 
                            "Wartość energetyczna","Tłuszcze","Tłuszcze nasycone","Węglowodany","Cukry","Błonnik","Białka","Sól"]
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

        for child in frame.winfo_children():
            if isinstance(child, tk.Label) and child["text"] == "Nazwa":
                for subchild in frame.winfo_children():
                    if isinstance(subchild, tk.Entry) and subchild.master == child.master:
                        filename = subchild.get()
                        break
                break

        if filename != "":
            file_path = os.path.join(self.folder_path, "Produkty.json")

            if os.path.exists(file_path):
                with open(file_path, "r") as f:
                    try:
                        data = json.load(f)
                    except json.JSONDecodeError:
                        data = {}
            else:
                data = {}

            entries = {}

            for child in frame.winfo_children():
                if isinstance(child, tk.Label) and child["text"] != "Nazwa" and child["text"] in self.label_texts:
                    text = child["text"]
                    row_num = child.grid_info()["row"]
                    for subchild2 in frame.winfo_children():
                        if isinstance(subchild2, tk.Label) and subchild2["text"] in self.label_texts2 and subchild2.grid_info()["row"] == row_num:
                            text2 = " " + subchild2["text"]
                            for subchild in frame.winfo_children():
                                if isinstance(subchild, tk.Entry) and subchild.master == child.master and subchild.grid_info()["row"] == row_num:
                                    entries[text] = subchild.get() + text2
                                    break

            data[filename] = entries

            with open(file_path, "w") as f:
                json.dump(data, f, indent=4)






if __name__ == "__main__":
    app = App()
    app.set_window_position()
    app.set_theme()
    app.menu()
    app.mainloop()