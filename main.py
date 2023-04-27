# Organizator, créé par Chokokafé le 25/04/2023

from tkinter import*
from customtkinter import*
from PIL import Image
from drawgraph import*

plus_image = CTkImage(light_image=Image.open("plus-icon.png"),dark_image=Image.open("plus-icon.png"),size=(60,60))

save = open("save.txt","a+")
save.seek(0)
if save.readlines() == []:
    save.write("Nothing here!")
    save.close()

class App(CTk):
    def __init__(self):
        super().__init__()
        set_appearance_mode("dark")
        set_default_color_theme("blue")
        self.geometry("1000x600")
        self.title("Organizator")
        self.location = "start"

    def forget_all(self):
        if self.location=="start":
            self.startframe.destroy()
            self.labelframe.destroy()
            
    def window_config(self):
        if self.location == "start":
            self.rowconfigure(1,weight=5,minsize=100)
            self.columnconfigure(1,weight=1,minsize=1)
            self.columnconfigure(3,weight=1,minsize=1)
        if self.location == "new_project":
            self.rowconfigure(1,weight=1,minsize=1)
            self.rowconfigure(2,weight=1,minsize=1)
            self.columnconfigure(1,weight=1)
            self.columnconfigure(2,weight=1)
            self.columnconfigure(3,weight=0)
            
    def create_new_project(self,name):
        name_exists = 0
        save = open("save.txt", "r+")
        for i in save.readlines():
            if i == "name : {}\n".format(name):
                name_exists = 1
            else :
                continue
        if name_exists:
            print("Un projet sous le même nom existe déjà !")
        else :
            save.seek(0)
            if "Nothing here!" in save.readlines():
                save.close()
                save = open("save.txt",'w')
            save.write("name : {}\n".format(name))
            
    def create_new_task(self,project,name,follow,subtask,opt):
        self.update()
        if follow=='':
            follow="aucun"
        task = ["+"+name+"\n",str(follow) +"\n",str(subtask)+"\n",str(opt)+"\n"]
        name_exists = 0
        save = open("save.txt","r+")
        for i in save.readlines():
            if i == "+{}\n".format(name):
                name_exists = 1
            else:
                continue
        if name_exists:
            print("Une tâche sous le même nom existe déjà !")
        else :
            save.seek(0)
            while True:
                line = save.readline()
                if line == "name : {}\n".format(project):
                    break
            save.writelines(task)
            save.close()
        self.currenttaskList.append(name)
        self.followcombo.configure(values=self.currenttaskList)
        
    def GUI_start(self):
        self.window_config()
        self.startframe = CTkFrame(self,fg_color="transparent")
        self.labelframe = CTkFrame(self,fg_color="transparent")
        label = CTkLabel(self.labelframe,text = "Organizator",font=("Verdana",30))
        new1 = CTkButton(self.startframe,text = "New Project",width=150,height=60,corner_radius=30, command=lambda:self.GUI_NewProject())
        new2 = CTkButton(self.startframe,text = "Day Setup",width=150,height=60,corner_radius=30)
        view1 = CTkButton(self.startframe,text = "Graph View",width=150,height=60,corner_radius=30)
        view2 = CTkButton(self.startframe,text = "List View",width=150,height=60,corner_radius=30)
        view3 = CTkButton(self.startframe,text = "Projects",width=150,height=60,corner_radius=30)
        label.pack()
        new1.grid(row=1,column=1,pady=20)
        new2.grid(row=2,column=1,pady=20)
        view1.grid(row=3,column=1,pady=20)
        view2.grid(row=4,column=1,pady=20)
        view3.grid(row=5,column=1,pady=20)
        self.startframe.grid(row=2,column=2)
        self.labelframe.grid(row=1,column=2)
        
    def GUI_NewProject(self):
        follow=StringVar()
        subtask=IntVar()
        opt=IntVar()
        self.currenttaskList = []
        self.forget_all()
        self.location = "new_project"
        self.window_config()
        
        # Nameframe
        self.nameframe = CTkFrame(self, fg_color = "transparent")
        namelabel = CTkLabel(self.nameframe, text = "Nom du projet:")
        nameentry = CTkEntry(self.nameframe, placeholder_text = "Entrez un nom...",width=200)
        namebutton = CTkButton(self.nameframe, text = "OK", width=100, height=40, corner_radius=30, command = lambda:self.create_new_project(nameentry.get()))
        namelabel.pack()
        nameentry.pack()
        namebutton.pack(pady=20)
        self.nameframe.grid(row=1, column=1)
        # TaskFrame : tout ce qui concerne la création de tâche
        self.taskframe = CTkFrame(self, fg_color= "transparent")
        namelabel2 = CTkLabel(self.taskframe,text = "Nom de la tâche :")
        nameentry2 = CTkEntry(self.taskframe,placeholder_text = "Entrez un nom...",width=200)
        followlabel = CTkLabel(self.taskframe,text = "La tâche suit...")
        self.followcombo = CTkComboBox(self.taskframe, values = self.currenttaskList,variable=follow)
        subtasklabel = CTkLabel(self.taskframe,text = "Sous-tâche ?")
        subtaskcheck = CTkCheckBox(self.taskframe,text="",variable=subtask,onvalue=1,offvalue=0)
        optlabel = CTkLabel(self.taskframe,text = "Optionnel ?")
        optcheck = CTkCheckBox(self.taskframe,text="",variable=opt,onvalue=1,offvalue=0)
        addtask = CTkButton(self.taskframe,text="",image=plus_image, fg_color='transparent', bg_color='transparent',hover=False, command=lambda:self.create_new_task(nameentry.get(),nameentry2.get(),follow.get(),subtask.get(),opt.get()))
        namelabel2.grid(row=1, column=1, columnspan=2)
        nameentry2.grid(row=2, column=1, columnspan=2)
        followlabel.grid(row=3, column=1,columnspan=2)
        self.followcombo.grid(row=4,column=1,columnspan=2)
        subtasklabel.grid(row=5,column=1)
        subtaskcheck.grid(row=5,column=2)
        optlabel.grid(row=6,column=1)
        optcheck.grid(row=6,column=2)
        addtask.grid(row=7,column=1,columnspan=2)
        self.taskframe.grid(row=2,column=1)
        
        # ProjectFrame : Projection graphique du projet
        
        self.projectframe = CTkFrame(self,fg_color="transparent")
        
        
        
app = App()
app.GUI_start()
app.mainloop()