import os
import tkinter as tk
from tkinter import messagebox
import webbrowser

class MyGUI:

    def __init__(self):

        self.listOfWebpages = []
        self.listOfLinks = []
        self.checkedPages = []
        self.checkedStates = []
        self.numOfPages = 0

        self.root = tk.Tk()

        #Dimensions and Title
        self.root.geometry("300x800")
        self.root.title("Webpages to Open")

        #Menu
        self.menubar = tk.Menu(self.root)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Close & Save", command=self.on_closing)
        self.menubar.add_cascade(menu=self.filemenu, label="File")
        self.root.config(menu=self.menubar)

        #Create Bottom Buttons
        self.addPage = tk.Button(self.root, text = "+", font = ('Arial', 18), command = self.add_page)
        self.addPage.place(x=0, y=750, height = 50, width=50)
        self.deletePage = tk.Button(self.root, text = "-", font = ('Arial', 18), command = self.delete_page)
        self.deletePage.place(x=50, y=750, height = 50, width=50)
        self.execute = tk.Button(self.root, text = "Open Tabs", font = ('Arial', 18), command = self.open_tabs)
        self.execute.place(x=100, y=750, height = 50, width=200)

        file_path = "SavedWebpages.txt"

        # Check if file exists and load data
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                self.numOfPages = int(file.readline().strip())
                for i in range(self.numOfPages):
                    self.status = file.readline().strip()
                    self.listOfWebpages.append(file.readline().strip())
                    self.listOfLinks.append(file.readline().strip())
                    self.add_page_3(i, self.status)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def add_page(self):
        popup = tk.Toplevel(self.root)
        popup.title("Webpage Details")
        popup.geometry("300x200")

        tk.Label(popup, text="Webpage Name:").pack(pady=10)
        webpageName = tk.Entry(popup)
        webpageName.pack(pady=5)

        tk.Label(popup, text="Webpage Link:").pack(pady=10)
        link = tk.Entry(popup)
        link.pack(pady=5)

        def on_submit():
            name = webpageName.get()
            self.listOfWebpages.append(name)
            self.listOfLinks.append(link.get())
            self.add_page_2()
            popup.destroy()

        submit_button = tk.Button(popup, text="Enter", command=on_submit)
        submit_button.pack(pady=20)

    def add_page_2(self):
        self.check_state = tk.IntVar()
        self.checkedStates.append(self.check_state)
        self.check = tk.Checkbutton(self.root, text= self.listOfWebpages[self.numOfPages], font=('Arial', 16), variable = self.check_state, command = self.update_checked_pages)
        self.check.grid(row=self.numOfPages, column=0, sticky = "w")
        self.numOfPages += 1

    def add_page_3(self, i, state):
        self.check_state = tk.IntVar()
        if state == "Checked": 
            self.check_state.set(1)
        self.checkedStates.append(self.check_state)
        self.check = tk.Checkbutton(self.root, text= self.listOfWebpages[i], font=('Arial', 16), variable = self.check_state, command = self.update_checked_pages)
        self.check.grid(row=i, column=0, sticky = "w")

    def update_checked_pages(self):
        self.checkedPages.clear()
        for i in range(self.numOfPages):
            if self.checkedStates[i].get() == 1:
                self.checkedPages.append(self.listOfLinks[i])
            if self.listOfLinks[i] in self.checkedPages and self.checkedStates[i].get() == 0:
                self.checkedPages.remove(self.listOfLinks[i])
    
    
    def delete_page(self):
        popup = tk.Toplevel(self.root)
        popup.title("Delete Command")
        popup.geometry("300x200")

        tk.Label(popup, text="Webpage Name:").pack(pady=10)
        webpageName = tk.Entry(popup)
        webpageName.pack(pady=5)

        def on_submit():
            name = webpageName.get()
            if name in self.listOfWebpages:
                index = self.listOfWebpages.index(name)
                self.listOfWebpages.pop(index)
                self.listOfLinks.pop(index)
                self.numOfPages -= 1
                messagebox.showinfo("Notice", "Web Page will be deleted upon script closing.")
            else:
                messagebox.showerror("Error", "Webpage not found.")
            popup.destroy()

        submit_button = tk.Button(popup, text="Enter", command=on_submit)
        submit_button.pack(pady=20)
    

    def open_tabs(self):
        for link in self.checkedPages:
            webbrowser.open_new_tab(link)
        self.save_data()
        

    def on_closing(self):
        if messagebox.askyesno(title="Quit?", message="Do you really want to quit?"):
            self.save_data()


    def save_data(self):
        file_path = "SavedWebpages.txt"
        with open(file_path, 'w') as file:
            file.write(str(self.numOfPages) + "\n")
            for i in range(self.numOfPages):
                if self.listOfLinks[i] in self.checkedPages:
                    file.write("Checked\n")
                else:
                    file.write("Unchecked\n")
                file.write(self.listOfWebpages[i] + "\n")
                file.write(self.listOfLinks[i] + "\n")
        self.root.destroy()

MyGUI()