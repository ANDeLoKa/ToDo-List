import customtkinter as Ctk
import json as Js
'''
       Class Overview

    +-----------------+
    |       GUI       |
    +-----------------+
    |  Colors : Dict  |
    |   Width : int   |
    |  Height : int   |
    +-----------------+
    | Font : CTkFont  |
    | selection_frame |
    |   : CTkFrame    |
    |activities_button|
    |   : CTkButton   |
    |
    |
    |

'''

class GUI(Ctk.CTk):
    
    '''
    dict_structure = {
        "activities" : [
            {
                "ID" : 0,
                "Description" : "Clean the House"
            },
            {
                "ID" : 0,
                "Description" : "Clean the House"
            }
        ]
    }
    '''

    Colors = {
        "Ash_Grey_Hover" : "#B9BEA5",
        "Ash_Grey" : "#A7AAA4",
        "Ash_Grey_Add_Task" : "#B0C7BD",
        "Ash_Grey_Add_Task_Hover" : "#B3CABF",
        "Black" : "#000000",
        "Cool_Gray" : "#202020",
        "Cool_Gray_Hover" : "#232323"
    }

    # geometry const
    width = 600
    height = 400

    IS_RESIZABLE = False

    DB_PATH = "data/database.json"

    def __init__(self):
        
        super().__init__()
        self.geometry(f"{self.width}x{self.height}")
        self.resizable(width=self.IS_RESIZABLE, height=self.IS_RESIZABLE)
        self.title("To-Do List by Andre")
        Ctk.set_appearance_mode("dark")

        self.Font = Ctk.CTkFont(family="Poppins", size=15, weight="bold")

        self.selection_frame = Ctk.CTkFrame(self, width=160)
        self.selection_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsw")

        self.task_frame = Ctk.CTkScrollableFrame(self, width=400, height=370, fg_color="transparent")
        self.task_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        activities_button = Ctk.CTkButton(self.selection_frame, text="Activities", font=self.Font, text_color=self.Colors["Black"], fg_color=self.Colors["Ash_Grey"], hover_color=self.Colors["Ash_Grey_Hover"], command=lambda:self._renderGroup("Activities"))
        activities_button.grid(row=0, column=0, padx=10, pady=5)

        today_button = Ctk.CTkButton(self.selection_frame, text="Today", font=self.Font, text_color=self.Colors["Black"], fg_color=self.Colors["Ash_Grey"], hover_color=self.Colors["Ash_Grey_Hover"], command=lambda:self._renderGroup("Today"))
        today_button.grid(row=1, column=0, padx=10, pady=5)

        self._renderGroup("Activities")

    def _readJson(self):
        file = open(self.DB_PATH, "r")
        string = file.read()
        file.close()

        # Dict
        return Js.loads(string)

    def _writeJson(self, db : dict):
        json = Js.dumps(db, indent=4)
        file = open(self.DB_PATH, "w")
        file.write(json)
        file.close()

    def _renderGroup(self, group):

        database = self._readJson()
        
        '''
        task structure = {
            "ID": int,
            "Description" : str
        }
        '''
        
        for child in self.task_frame.winfo_children():
            child.destroy()

        add_task_frame = Ctk.CTkFrame(self.task_frame, fg_color="transparent")
        add_task_frame.grid(row=0, column=0, padx=10, pady=3, sticky="wens")
        btn_add_task = Ctk.CTkButton(add_task_frame, text="Add a Task", command=lambda:self._addTask(group), fg_color=self.Colors["Ash_Grey_Add_Task"], hover_color=self.Colors["Ash_Grey_Add_Task_Hover"], font=self.Font, text_color=self.Colors["Black"])
        btn_add_task.grid(row=0, column=0, padx=5, pady=5, sticky="we")

        for i, task in enumerate(database[group], start=1):
            f = Ctk.CTkFrame(self.task_frame, height=40)
            f.grid(row=i, column=0, padx=10, pady=3, sticky="we")

            cb = Ctk.CTkCheckBox(f, text=task["Description"], fg_color=self.Colors["Ash_Grey"], hover_color=self.Colors["Ash_Grey_Hover"], command=lambda:self._deleteTask(task["ID"], group), width=350)
            cb.grid(row=0, column=0, padx=5, pady=5)
        
    def _addTask(self, group : str):
        database = self._readJson()
        
        input_dialog = Ctk.CTkInputDialog(title="New Task", text="Task Description:")
        new_task_desc = input_dialog.get_input()
        
        if not (new_task_desc.__eq__("")):
            for char in new_task_desc:
                if char.__eq__(" "):
                    pass
                    # fix for this type of input "      {string}       "
                else:
                    new_task = {
                        "ID" : database["Internal_Identifier"],
                        "Description" : new_task_desc
                    }
                    
                    database[group].append(new_task)
                    database["Internal_Identifier"] += 1
                    
                    self._writeJson(database)
                    self._renderGroup(group)
                    
                    break
        return None

    def _deleteTask(self, desc : str, group : str):
        
        database = self._readJson()
        print(desc)
        
        for task in database[group]:
            if task["Description"].__eq__(desc):
                del task

        self._writeJson(database)
        self._renderGroup(group)

    