########     MODULES    ########
from modules import fix_dependencies as fix
from modules import organize_folders as org
from modules import ws_data as ws_data
import tkinter as tk
from tkinter import MULTIPLE, filedialog, ttk, messagebox, StringVar
from tkinter.messagebox import askyesno
from PIL import ImageTk, Image
import shutil
import os
import subprocess


########     FIX MISSING PLUGINS     ########
fix.install_sevenzip()


########       MAIN APP        ########
class App(tk.Tk):
    WIDTH = 360
    HEIGHT = 740

    def __init__(self):
        super().__init__()
        self.title("SAM - Smart Assets Manager")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.resizable(False, False)
        self.iconbitmap("assets/SAM.ico")

        # Load and resize multiple images
        self.image_all = self.load_and_resize_image("assets/select_all.ico", 25, 25)
        self.image_none = self.load_and_resize_image("assets/select_none.ico", 25, 25)
        self.image_dir = self.load_and_resize_image("assets/open_folder.ico", 25, 25)

        # WRAPPER
        self.wrapper_top = ttk.LabelFrame(master=self)
        self.wrapper_bottom = ttk.LabelFrame(master=self)

        # Create labels
        self.assets_organizer_lbl = tk.Label(self.wrapper_top, text="ORGANIZER")

        self.batch_download_lbl = tk.Label(self.wrapper_bottom, text="GET DATA")
        self.download_folder_lbl = tk.Label(
            self.wrapper_bottom, text="Download Folder Path"
        )
        self.percent = StringVar()
        self.percent_lbl = tk.Label(self.wrapper_bottom, textvariable=self.percent)
        self.download_folder_entry = tk.Entry(self.wrapper_bottom, width=44)
        self.prog_bar = ttk.Progressbar(
            self.wrapper_bottom, orient="horizontal", mode="determinate"
        )

        # Create listbox
        self.list_items = tk.StringVar(value=["" for i in range(10)])
        self.listbox = tk.Listbox(
            self.wrapper_top, selectmode=MULTIPLE, listvariable=self.list_items
        )

        # Create scrollbar
        self.xscrollbar = ttk.Scrollbar(
            self.listbox, orient="horizontal", command=self.listbox.xview
        )
        self.xscrollbar.pack(side="bottom", fill=tk.X)

        self.yscrollbar = ttk.Scrollbar(
            self.listbox, orient="vertical", command=self.listbox.yview
        )
        self.yscrollbar.pack(side="right", fill=tk.Y)

        # Create buttons
        self.select_all_btn = tk.Button(
            self.wrapper_top,
            text="  All",
            image=self.image_all,
            compound="left",
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
            highlightthickness=1,
            bg="SystemButtonFace",
            bd=0,
            command=self.open_dir,
        )

        self.browse_btn = tk.Button(
            self.wrapper_top,
            text="Browse Location",
            fg="black",
            bg="#DAF7A6",
            command=self.browse_folders,
        )
        self.extract_btn = tk.Button(
            self.wrapper_top,
            text="Extract Archives",
            fg="black",
            bg="#FFC300",
            command=self.extract_archives,
        )
        self.run_organizer_btn = tk.Button(
            self.wrapper_top,
            text="Run Organizer",
            fg="black",
            bg="#4CBB17",
            command=self.selected_item_organize,
        )
        self.remove_local_bk = tk.Button(
            self.wrapper_top,
            text="Remove Backup",
            fg="black",
            bg="#d9dcdf",
            command=self.confirm_remove_bk,
        )
        self.remove_junk_folders = tk.Button(
            self.wrapper_top,
            text="Remove Junk",
            fg="black",
            bg="#d9dcdf",
            command=self.confirm_remove_junk,
        )
        self.refresh = tk.Button(
            self.wrapper_top,
            text="Refresh List",
            fg="black",
            bg="#d9dcdf",
            command=self.refresh_list,
        )

        self.select_text_file_urls_btn = tk.Button(
            self.wrapper_bottom,
            text="Select Links File",
            fg="black",
            bg="#DAF7A6",
            command=self.pick_text_file_urls,
        )
        # self.download_links_btn = tk.Button(
        #     self.wrapper_bottom,
        #     text="",
        #     fg="black",
        #     bg="#FFC300",
        #     command=self.test
        # )
        self.get_data = tk.Button(
            self.wrapper_bottom,
            text="GET -> Links File",
            fg="black",
            bg="#4CBB17",
            command=self.download_selected_urls,
        )
        self.setpath_btn = tk.Button(
            self.wrapper_bottom, text="...", width=3, command=self.set_download_folder
        )

        # Position buttons Wrapper Top
        self.assets_organizer_lbl.place(x=5, y=0, width=100, height=30)
        self.open_dir_btn.place(x=120, y=0, width=70, height=30)
        self.none_btn.place(x=190, y=0, width=70, height=30)
        self.select_all_btn.place(x=260, y=0, width=70, height=30)

        self.listbox.place(x=5, y=35, width=325, height=420)

        self.browse_btn.place(x=10, y=460, width=105, height=30)
        self.extract_btn.place(x=118, y=460, width=105, height=30)
        self.run_organizer_btn.place(x=225, y=460, width=105, height=30)

        self.remove_local_bk.place(x=10, y=493, width=105, height=30)
        self.remove_junk_folders.place(x=118, y=493, width=105, height=30)
        self.refresh.place(x=225, y=493, width=105, height=30)

        # Position buttons Wrapper Bottom
        self.batch_download_lbl.place(x=5, y=0, width=100, height=20)
        self.select_text_file_urls_btn.place(x=10, y=25, width=105, height=30)
        # self.download_links_btn.place(x=118, y=25, width=105, height=30)
        self.get_data.place(x=225, y=25, width=105, height=30)

        self.download_folder_lbl.place(x=10, y=60, width=130, height=20)
        self.download_folder_entry.place(x=10, y=85, width=270, height=20)
        self.setpath_btn.place(x=285, y=85, width=35, height=20)
        self.prog_bar.place(x=10, y=110, width=310, height=20)
        self.percent_lbl.place(x=10, y=130, width=40, height=20)

        self.listbox.configure(xscrollcommand=self.xscrollbar.set)
        self.listbox.configure(yscrollcommand=self.yscrollbar.set)

        # Adjust buttons hovering effect
        self.changeOnHover(self.select_all_btn, "#AFE1AF", "SystemButtonFace")
        self.changeOnHover(self.none_btn, "#AFE1AF", "SystemButtonFace")
        self.changeOnHover(self.open_dir_btn, "#AFE1AF", "SystemButtonFace")
        self.changeOnHover(self.browse_btn, "#A7C7E7", "#DAF7A6")
        self.changeOnHover(self.extract_btn, "#A7C7E7", "#FFC300")
        self.changeOnHover(self.run_organizer_btn, "#A7C7E7", "#4CBB17")
        self.changeOnHover(self.remove_local_bk, "#A7C7E7", "#d9dcdf")
        self.changeOnHover(self.remove_junk_folders, "#A7C7E7", "#d9dcdf")
        self.changeOnHover(self.refresh, "#A7C7E7", "#d9dcdf")
        self.changeOnHover(self.select_text_file_urls_btn, "#A7C7E7", "#DAF7A6")
        self.changeOnHover(self.get_data, "#A7C7E7", "#4CBB17")

        # Pack wrappers
        self.wrapper_top.pack(fill="both", expand="yes", padx=10)
        self.wrapper_top.config(height=390)
        self.wrapper_bottom.pack(fill="both", expand="yes", padx=10, pady=5)

    ###     FUNCTIONS FOR WRAPPER 1 - FILES / FOLDER CLEANUP    ###

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

    def open_dir(self):
        selected_indices = self.listbox.curselection()
        if len(selected_indices) == 1:
            selected_folder = self.listbox.get(selected_indices[0])
            basis_folder = os.path.join(root_location, selected_folder)
            if os.path.exists(basis_folder):
                os.startfile(basis_folder)
        else:
            messagebox.showinfo("Information", "Please select one folder!")

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
            global root_location

            # Use a temporary variable to store the selected folder path
            temp_root_location = filedialog.askdirectory(initialdir="/")

            # Check if the user selected a folder (temp_root_location is not empty)
            if temp_root_location:
                root_location = temp_root_location

                global root_child_folders
                root_child_folders = [
                    str(itm)
                    for itm in os.listdir(root_location)
                    if os.path.isdir(os.path.join(root_location, itm))
                    and os.path.exists(os.path.join(root_location, itm))
                ]

                # remove items in list
                self.listbox.delete(0, "end")

                # add new items to list
                if len(root_child_folders) > 0:
                    for i in range(len(root_child_folders)):
                        self.listbox.insert(i, root_child_folders[i])

                else:
                    self.listbox.insert(
                        0, "No root_child_folders Found in Specified Location"
                    )
                    print("No root_child_folders found")
            else:
                print("Folder selection canceled by user")

        except FileNotFoundError:
            # Handle other exceptions if necessary
            print("FileNotFoundError")
        except PermissionError:
            print("Permissions not allowed by admin")

    def refresh_list(self):
        try:
            # case where external links file is provided
            if "https://" in self.listbox.get(0):
                if textFileWithUrls:
                    with open(textFileWithUrls) as f:
                        content = f.readlines()

                    # remove whitespace characters like `\n` at the end of each line
                    global links_list
                    links_list = [x.strip() for x in content]
                    links_list = [
                        x
                        for x in links_list
                        if os.environ.get("links_app_url")[1:-1] in x
                        or os.environ.get("storage_app_url")[1:-1] in x
                    ]

                    self.listbox.delete(0, "end")

                    if len(links_list) > 0:
                        for i in range(len(links_list)):
                            self.listbox.insert(i, links_list[i])

            # case where local paths are loaded
            elif root_location:
                root_child_folders = [
                    str(itm)
                    for itm in os.listdir(root_location)
                    if os.path.isdir(os.path.join(root_location, itm))
                    and os.path.exists(os.path.join(root_location, itm))
                ]
                # remove items in list
                self.listbox.delete(0, "end")

                # add new items to list
                if len(root_child_folders) > 0:
                    for i in range(len(root_child_folders)):
                        self.listbox.insert(i, root_child_folders[i])
                else:
                    self.listbox.insert(
                        0, "No root_child_folders Found in Specified Location"
                    )
                    print("No root_child_folders found")
            else:
                print("Error with the path")
        except NameError:
            print('"root_location" is not defined')

    def selected_item_organize(self):
        try:
            for i in self.listbox.curselection():
                local_folder_path = os.path.join(root_location, self.listbox.get(i))

                org.organize_folder(local_folder_path)

        except FileNotFoundError or NameError or PermissionError:
            pass

    def remove_junk(self):
        try:
            if len(self.listbox.curselection()) > 0:
                for i in self.listbox.curselection():
                    junk_folder = f"{root_location}\\{self.listbox.get(i)}\\junk"

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
                        f"{root_location}\\{self.listbox.get(i)}\\local_backup"
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
                    root_folder = os.path.join(root_location, self.listbox.get(i))
                    try:
                        archives_found = [
                            os.path.join(root, filename)
                            for root, dirs, files in os.walk(root_folder)
                            for filename in files
                            if filename.endswith((".rar", ".zip", ".7z"))
                        ]
                        # Extract archives found in root folder
                        for arch_file in archives_found:
                            self.extract_recursively(arch_file, root_folder)

                    except Exception as e:
                        # Handle any exceptions that occur during the extraction process
                        print(
                            "An error occurred while extracting the archives:", str(e)
                        )

        except Exception as e:
            # Handle any exceptions that occur during the selection process
            print("An error occurred while extracting the archives:", str(e))

    def extract_recursively(self, archive_path, output_folder):
        # Get extracted folder
        extract_folder = os.path.join(output_folder, os.path.splitext(archive_path)[0])

        # Create the output folder if it doesn't exist
        try:
            if not os.path.exists(extract_folder):
                os.mkdir(extract_folder)
        except OSError as e:
            print(f"Error when creating folder {extract_folder}, error: {e}")

        # Extract first level archive
        try:
            subprocess.call(
                [
                    "C:/Program Files/7-Zip/7z.exe",
                    "x",
                    archive_path,
                    f"-o{extract_folder}",
                    "-y",
                ]
            )
        except OSError as e:
            # Handle the specific exception [WinError 5] Access is denied
            if e.winerror == 5:
                print("Access to the file is denied. Check permissions.")
            elif e.winerror == 2:
                print(
                    f"Error when accessing '7z.exe' file {extract_folder}, error: {e}"
                )
            # Handle other OSError exceptions if necessary
            else:
                print(f"An OSError occurred: {e}")

        # Filter archives in child folder
        child_archives = [
            os.path.join(root, filename)
            for root, _, filenames in os.walk(extract_folder)
            for filename in filenames
            if os.path.splitext(filename)[1][1:].lower() in ["zip", "rar", "7z"]
        ]
        if len(child_archives) > 0:
            for child in child_archives:
                nested_output_folder = os.path.dirname(child)

                self.extract_recursively(child, nested_output_folder)

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

    ###     FUNCTIONS FOR WRAPPER 2 - WEBSCRAPE DATA     ###

    def pick_text_file_urls(self):
        try:
            global textFileWithUrls
            textFileWithUrls = filedialog.askopenfilename(
                initialdir="/",
                title="Select File",
                filetypes=(("text files", "*.txt"), ("all files", "*.*")),
            )
            with open(textFileWithUrls) as f:
                content = f.readlines()

            # remove whitespace characters like `\n` at the end of each line
            global links_list
            links_list = [x.strip() for x in content]

            links_list = [
                x
                for x in links_list
                if os.environ.get("links_app_url")[1:-1] in x
                or os.environ.get("storage_app_url")[1:-1] in x
            ]

            self.listbox.delete(0, "end")

            if len(links_list) > 0:
                for i in range(len(links_list)):
                    self.listbox.insert(i, links_list[i])

        except FileNotFoundError or NameError:
            pass

    def set_download_folder(self):
        self.download_folder_entry.delete(0, tk.END)

        global downloadPATH
        downloadPATH = filedialog.askdirectory(initialdir="/")

        self.download_folder_entry.insert(0, downloadPATH)

    # download urls
    def download_selected_urls(self):
        try:
            if downloadPATH and textFileWithUrls:
                selected_indices = self.listbox.curselection()
                selected_urls = [self.listbox.get(i) for i in selected_indices]

                if selected_urls and len(selected_urls) > 0:
                    if os.environ.get("storage_app_url")[1:-1] in selected_urls[0]:
                        ws_data.download_cloud_urls(downloadPATH, selected_urls)
                    elif os.environ.get("links_app_url")[1:-1] in selected_urls[0]:
                        ws_data.webscrape_urls(downloadPATH, selected_urls)
                else:
                    messagebox.showinfo("Information", "No URLs selected")
            else:
                if not downloadPATH:
                    messagebox.showinfo(
                        "Information", "Download folder path not specified"
                    )
                if not textFileWithUrls:
                    messagebox.showinfo(
                        "Information", "Text file with URLs not specified"
                    )
        except Exception as e:
            messagebox.showinfo("Error", f"An error occurred: {str(e)}")


if __name__ == "__main__":
    app = App()
    app.mainloop()
