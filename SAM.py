########     MODULES    ########
from modules import organize_folders as org
from modules import fix_env_vars as fix
from dotenv import load_dotenv
import tkinter as tk
from tkinter import MULTIPLE, filedialog, ttk, messagebox
from tkinter.messagebox import askyesno
from PIL import ImageTk, Image
import shutil
import os
import zipfile


########     LOAD ENVIRONMENT VARIABLES      ########
load_dotenv()
proj_path = f"{os.getenv('proj_path')}"


########     FIX MISSING PLUGINS AND ADD ENV PATHS      ########
fix.set_environment_variables()
fix.install_unrar()


########       MAIN APP        ########
class App(tk.Tk):
    
    WIDTH = 360
    HEIGHT = 600  
    
    def __init__(self):
        super().__init__()
        self.title("SAM - Smart Assets Manager")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.resizable(False, False)
        self.iconbitmap(proj_path + "/assets/SAM.ico")

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

    ###     FUNCTIONS FOR WRAPPER - FILES / FOLDER CLEANUP    ###

    # Load and resize each image loaded
    def load_and_resize_image(self, file_path, max_width, max_height):
        try:
            # Load the image using Pillow
            image = Image.open(file_path)

            # Resize the image to fit within the specified maximum dimensions while preserving aspect ratio
            image.thumbnail((max_width, max_height), Image.LANCZOS)

            # Convert the image to RGB mode to ensure it has a valid transparency mask
            image = image.convert("RGBA")

            # Create a PhotoImage object from the resized image and return it
            photo = ImageTk.PhotoImage(image)
            return photo
        except Exception as e:
            print(f"Error loading image: {e}")
            return None

    # Change properties of button on hover
    def changeOnHover(self, button, colorOnHover, colorOnLeave):
        # adjusting background of the widget
        # background on entering widget
        button.bind("<Enter>", func=lambda e: button.config(background=colorOnHover))

        # background color on leving widget
        button.bind("<Leave>", func=lambda e: button.config(background=colorOnLeave))

    def browse_folders(self):
        try:
            global path_with_folders
            path_with_folders = filedialog.askdirectory(initialdir="/")

            global subFolders
            subFolders = [
                str(itm)
                for itm in os.listdir(path_with_folders)
                if os.path.isdir(os.path.join(path_with_folders, itm)) and os.path.exists(os.path.join(path_with_folders, itm))
            ]
            
            # remove items in list
            self.listbox.delete(0, "end")
            
            # add new items to list
            if len(subFolders) > 0:
                for i in range(len(subFolders)):
                    self.listbox.insert(i, subFolders[i])

            else:
                self.listbox.insert(0, "No Subfolders Found in Specified Location")
                print("No Subfolders found")

        except FileNotFoundError:
            print("Loading path canceled by user")
        except NameError:
            print("Name error on path")
        except PermissionError:
            print("Permisions not allowed by admin")
    
    def refresh_list(self):
        try:
            if path_with_folders:
                subFolders = [
                    str(itm)
                    for itm in os.listdir(path_with_folders)
                    if os.path.isdir(os.path.join(path_with_folders, itm)) and os.path.exists(os.path.join(path_with_folders, itm))
                ]
                # remove items in list
                self.listbox.delete(0, "end")
                
                # add new items to list
                if len(subFolders) > 0:
                    for i in range(len(subFolders)):
                        self.listbox.insert(i, subFolders[i])
                else:
                    self.listbox.insert(0, "No Subfolders Found in Specified Location")
                    print("No Subfolders found")
            else:
                print("Error with the path")
        except NameError:
            print('"path_with_folders" is not defined')

    def selected_item(self):
        try:
            for i in self.listbox.curselection():
                local_folder_path = os.path.join(path_with_folders, self.listbox.get(i))

                org.organize_folder(local_folder_path)

        except FileNotFoundError or NameError or PermissionError:
            pass

    def select_all(self):
        try:
            self.listbox.selection_set(0, tk.END)
        except NameError:
            pass

    def deselect_all(self):
        try:
            self.listbox.selection_clear(0, tk.END)
        except NameError:
            pass

    def remove_junk(self):
        try:
            if len(self.listbox.curselection()) > 0:
                for i in self.listbox.curselection():
                    junk_folder = f"{path_with_folders}\\{self.listbox.get(i)}\\junk"

                    try:
                        shutil.rmtree(junk_folder)
                    except Exception as e:
                        print(e)

            else:
                messagebox.showinfo("Information", "Please select the folders")

        except NameError or PermissionError:
            pass

    def remove_bk(self):
        try:
            if len(self.listbox.curselection()) > 0:
                for i in self.listbox.curselection():
                    local_bk_folder = (
                        f"{path_with_folders}\\{self.listbox.get(i)}\\local_backup"
                    )

                    try:
                        shutil.rmtree(local_bk_folder)
                    except Exception as e:
                        print(e)

            else:
                messagebox.showinfo("Information", "Please select the folders")

        except NameError or PermissionError:
            pass

    def extract_archives(self):
        try:
            if len(self.listbox.curselection()) > 0:
                for i in self.listbox.curselection():
                    root_folder = os.path.join(path_with_folders, self.listbox.get(i))
                    try:
                        archives_found = [
                            os.path.join(root, filename)
                            for root, dirs, files in os.walk(root_folder)
                            for filename in files
                            if filename.endswith(".rar") or filename.endswith(".zip")
                        ]
                        # extract archives found in root folder
                        for arch in archives_found:
                            self.extract_recursively(arch, root_folder)

                    except Exception as e:
                        # Handle any exceptions that occur during the extraction process
                        print(
                            "An error occurred while extracting the archives:", str(e)
                        )

        except Exception as e:
            # Handle any exceptions that occur during selection process
            print("An error occurred while extracting the archives:", str(e))


    def extract_recursively(self, archive_path, output_folder):
        # Get extracted folder
        extract_folder = os.path.join(output_folder, os.path.splitext(archive_path)[0])
        
        try:
            from unrar import rarfile
            
            with rarfile.RarFile(archive_path, "r") as archive:
                # Extract all files in the archive
                archive.extractall(extract_folder)

        except ImportError:            
            print("RAR module not found. You may need to install it.")
                
            
        try:
            if not os.path.exists(extract_folder):
                # Create the output folder if it doesn't exist
                os.mkdir(extract_folder)
        except OSError as e:
            print(f"Error when creating folder {extract_folder}, error: {e}")

        # Filter archives in child folder
        child_archives = [
            os.path.join(root, filename)
            for root, _, filenames in os.walk(extract_folder)
            for filename in filenames
            if os.path.splitext(filename)[1][1:].lower() in ["zip", "rar"]
        ]
        if len(child_archives) > 0:
            
            for child in child_archives:
                nested_output_folder = os.path.dirname(child)

                if child.endswith("rar"):
                    self.extract_recursively(child, nested_output_folder)
                elif child.endswith("zip"):
                    with zipfile.ZipFile(archive_path, "r") as zip_archive:
                        # Extract all files in the archive
                        zip_archive.extractall(nested_output_folder)

    # open selected folder
    def open_dir(self):
        selected_indices = self.listbox.curselection()
        if len(selected_indices) == 1:
            selected_folder = self.listbox.get(selected_indices[0])
            basis_folder = os.path.join(path_with_folders, selected_folder)
            if os.path.exists(basis_folder):
                os.startfile(basis_folder)
        else:
            messagebox.showinfo("Information", "Please select one folder!")

    def confirm_remove_bk(self):
        answer = askyesno(
            title="confirmation",
            message='Are you sure that you want to delete "Local Backup" folders in selected directories?',
        )
        if answer:
            self.remove_bk()

    def confirm_remove_junk(self):
        answer = askyesno(
            title="confirmation",
            message='Are you sure that you want to delete "Junk" folders in selected directories?',
        )
        if answer:
            self.remove_junk()


if __name__ == "__main__":
    app = App()
    app.mainloop()
