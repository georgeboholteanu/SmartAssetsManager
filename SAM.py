########     MODULES    ########
from dotenv import load_dotenv
import tkinter as tk
from tkinter import MULTIPLE, filedialog, ttk, messagebox
from tkinter.messagebox import askyesno
import os


########     LOAD ENVIRONMENT VARIABLES      ########
load_dotenv()
proj_path = os.getenv('PROJ_PATH')

########       MAIN APP        ########
class App(tk.Tk):
    
    WIDTH = 360
    HEIGHT = 600  
    
    def __init__(self):
        super().__init__()
        self.title("SAM - Smart Assets Manager")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.resizable(False, False)
        self.iconbitmap(os.path.join(proj_path, "SAM.ico"))

        # Load and resize multiple images
        self.image_all = self.load_and_resize_image(proj_path + "/assets/select_all.ico", 25, 25)
        self.image_none = self.load_and_resize_image(proj_path + "/assets/select_none.ico", 25, 25)
        self.image_dir = self.load_and_resize_image(proj_path + "/assets/open_folder.ico", 25, 25)

        # WRAPPER
        self.wrapper_top = ttk.LabelFrame(master=self)

        # Create label
        self.assets_organizer_lbl = tk.Label(self.wrapper_top, text="Organize Folders")
        self.assets_organizer_lbl.place(relx=0.02, rely=0, relheight=0.05)

        # Create buttons
        self.select_all_btn = tk.Button(
            self.wrapper_top,
            text="  All",
            image=self.image_all,
            compound="left",
            width=60,
            height=20,            
            highlightthickness=1,
            bg="SystemButtonFace",
            bd=0,
            command=self.select_all,
        )
        self.none_btn = tk.Button(
            self.wrapper_top,
            text="  None",
            image=self.image_none,
            compound="left",
            width=60,
            height=20,
            highlightthickness=1,
            bg="SystemButtonFace",
            bd=0,
            command=self.deselect_all,
        )
        self.open_dir_btn = tk.Button(
            self.wrapper_top,
            text="  Open",
            image=self.image_dir,
            compound="left",
            width=60,
            height=20,
            highlightthickness=1,
            bg="SystemButtonFace",
            bd=0,
            command=self.open_dir,
        )
        
        self.browse_btn = tk.Button(
            self.wrapper_top,
            text="Browse Location",
            width=13,
            fg="black",
            bg="#DAF7A6",
            command=self.browse_folders,
        )
        self.extract_btn = tk.Button(
            self.wrapper_top,
            text="Extract Archives",
            width=13,
            fg="black",
            bg="#FFC300",
            command=self.extract_archives,
        )
        self.runOrganizer_btn = tk.Button(
            self.wrapper_top,
            text="Run Organizer",
            width=13,
            fg="black",
            bg="#4CBB17",
            command=self.selected_item,
        )
        self.remove_local_bk = tk.Button(
            self.wrapper_top,
            text="Remove Backup",
            width=13,
            height=1,
            fg="black",
            bg="#d9dcdf",
            command=self.confirm_remove_bk,
        )
        self.remove_junk_folders = tk.Button(
            self.wrapper_top,
            text="Remove Junk",
            width=13,
            height=20,
            fg="black",
            bg="#d9dcdf",
            command=self.confirm_remove_junk,
        )        
        self.refresh = tk.Button(
            self.wrapper_top,
            text="Refresh List",
            width=13,
            height=20,
            fg="black",
            bg="#d9dcdf",
            command=self.refresh_list,
        )
        
        # Position buttons
        self.open_dir_btn.place(relx=0.35, rely=0, relheight=0.05, relwidth=0.2)
        self.none_btn.place(relx=0.55, rely=0, relheight=0.05, relwidth=0.2)
        self.select_all_btn.place(relx=0.75, rely=0, relheight=0.05, relwidth=0.2)
        
        self.browse_btn.place(relx=0.02, rely=0.87, relheight=0.05)
        self.extract_btn.place(relx=0.33, rely=0.87, relheight=0.05)
        self.runOrganizer_btn.place(relx=0.64, rely=0.87, relheight=0.05)

        self.remove_local_bk.place(relx=0.02, rely=0.93, relheight=0.05)
        self.remove_junk_folders.place(relx=0.33, rely=0.93, relheight=0.05)
        self.refresh.place(relx=0.64, rely=0.93, relheight=0.05)

        # Create listbox
        self.list_items = tk.StringVar(value=["" for i in range(10)])
        self.listbox = tk.Listbox(
            self.wrapper_top, selectmode=MULTIPLE, listvariable=self.list_items
        )
        self.listbox.place(relwidth=0.94, relheight=0.8, relx=0.02, rely=0.06)
        
        # Create scrollbar
        self.xscrollbar = ttk.Scrollbar(
            self.listbox, orient="horizontal", command=self.listbox.xview
        )
        self.xscrollbar.pack(side="bottom", fill=tk.X)

        self.yscrollbar = ttk.Scrollbar(
            self.listbox, orient="vertical", command=self.listbox.yview
        )
        self.yscrollbar.pack(side="right", fill=tk.Y)

        self.listbox.configure(xscrollcommand=self.xscrollbar.set)
        self.listbox.configure(yscrollcommand=self.yscrollbar.set)

        self.wrapper_top.pack(fill="both", expand="yes", padx=10, pady=10)

        # Adjust buttons hovering effect
        self.changeOnHover(self.select_all_btn, "#AFE1AF", "SystemButtonFace")
        self.changeOnHover(self.none_btn, "#AFE1AF", "SystemButtonFace")
        self.changeOnHover(self.open_dir_btn, "#AFE1AF", "SystemButtonFace")
        self.changeOnHover(self.browse_btn, "#A7C7E7", "#DAF7A6")
        self.changeOnHover(self.extract_btn, "#A7C7E7", "#FFC300")
        self.changeOnHover(self.runOrganizer_btn, "#A7C7E7", "#4CBB17")
        self.changeOnHover(self.remove_local_bk, "#A7C7E7", "#d9dcdf")
        self.changeOnHover(self.remove_junk_folders, "#A7C7E7", "#d9dcdf")
        self.changeOnHover(self.refresh, "#A7C7E7", "#d9dcdf")
        
