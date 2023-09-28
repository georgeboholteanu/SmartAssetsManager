# DEPENDENCY FILE FOR MAIN APP

import os
import shutil
import json
import zipfile
import pathlib
import stat
from dotenv import load_dotenv

load_dotenv()

def redo_with_write(redo_func, path, err):
    os.chmod(path, stat.S_IWRITE)
    redo_func(path)
    
def remove_folder_safely(folder_path):
    try:
        shutil.rmtree(folder_path, onerror=redo_with_write)
    except FileNotFoundError:
        print(f"Error: Cannot find folder '{folder_path}' to delete!")
        
def create_backup(targetPATH):
    try:
        os.mkdir(os.path.join(targetPATH, "local_backup"))
    except OSError:
        pass

    with zipfile.ZipFile(os.path.join(targetPATH, "local_backup", "local_backup.zip"), 'w') as myzip:
        try:
            directory = pathlib.Path(targetPATH)
            for file_path in directory.rglob("*"):
                if "local_backup" not in str(file_path):
                    myzip.write(file_path, arcname=file_path.relative_to(directory))
        except zipfile.BadZipFile as e:
            print(e)

def organize_folder(targetPATH):
    # Create backup folder
    create_backup(os.path.join(targetPATH))
    
    # Load the filters from the JSON file
    with open(f"{os.getenv('proj_path')}" + "/modules/filters.json") as f:
        global filters
        filters = json.load(f)

    # Create the necessary folders if they don't exist
    for folder in filters.keys(): 
        if folder != "MAX" and folder !="PREVIEWS":           
            os.makedirs(os.path.join(targetPATH, folder), exist_ok=True)

    # Get all extensions from the filters
    all_extensions = set(extension for extensions in filters.values() for extension in extensions)
    
    # Organize folder
    for root, dirnames, filenames in os.walk(targetPATH):
        for filename in filenames:
            extension = os.path.splitext(filename)[1][1:].lower()
            if extension not in all_extensions:
                source_path = os.path.join(root, filename)
                destination_path = os.path.join(os.path.join(targetPATH, "JUNK"), filename)
                shutil.move(source_path, destination_path)

            else:                      
                if "max" in filename.split('.')[-1].lower():
                    source_path = os.path.join(root, filename)
                    destination_path = os.path.join(targetPATH, filename)
                    if source_path != destination_path:
                        shutil.move(source_path, destination_path)
                
                else:                            
                    if filename.split('.')[-1] in filters.get("MAPS"):
                        if "preview" in filename.lower() or "render" in filename.lower() and filename.split('.')[-1].lower() in filters.get("PREVIEWS"):                            
                            source_path = os.path.join(root, filename)
                            destination_path = os.path.join(targetPATH, filename)
                            if source_path != destination_path:
                                shutil.move(source_path, destination_path)   
                        else:                                                                                         
                            source_path = os.path.join(root, filename)
                            destination_path = os.path.join(os.path.join(targetPATH, "MAPS"), filename)
                            shutil.move(source_path, destination_path)
                    elif filename.split('.')[-1].lower() in filters.get("EXPORT"):                                                                
                        source_path = os.path.join(root, filename)
                        destination_path = os.path.join(os.path.join(targetPATH, "EXPORT"), filename)
                        shutil.move(source_path, destination_path)
                    elif filename.split('.')[-1].lower()  in filters.get("ARCHIVES") and filename.split('.')[0] != "local_backup":                                                                
                        source_path = os.path.join(root, filename)
                        destination_path = os.path.join(os.path.join(targetPATH, "ARCHIVES"), filename)
                        shutil.move(source_path, destination_path)
                    elif filename.split('.')[-1].lower()  in filters.get("MISC"):                                                                
                        source_path = os.path.join(root, filename)
                        destination_path = os.path.join(os.path.join(targetPATH, "MISC"), filename)
                        shutil.move(source_path, destination_path)
                    elif filename.split('.')[-1].lower()  in filters.get("PROXIES"):                                                                
                        source_path = os.path.join(root, filename)
                        destination_path = os.path.join(os.path.join(targetPATH, "PROXIES"), filename)
                        shutil.move(source_path, destination_path)

    # Folders to keep
    retained_folders = ["MAPS", "EXPORT", "MISC", "ARCHIVES", "JUNK", "PROXIES", "local_backup"]
    
    # Clear irrelevant folders filtering the files out
    removed_folders = [os.path.join(targetPATH, folder) for folder in os.listdir(targetPATH) if os.path.isdir(os.path.join(targetPATH, folder)) and folder not in retained_folders]
    
    # Check if there are no remaining files in folders to be removed
    for folder in removed_folders:
        for root, _, filenames in os.walk(folder):
            if not filenames:
                remove_folder_safely(folder)
            else:
                print("Files still present in folder: %s" % folder)