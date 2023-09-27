
*A.  DESCRIPTION*

The app can be used to automate downloading and organising of multiple assests into individual specific folder structure. It uses **requests** module to login on hosting platform of the assets and download them from the selected URLs.


*B.  REQUIREMENTS*
* The application is compatible with machines running **WINDOWS 10/11 OS**.
* ***UnRARDLL*** is required to unpack ".rar" files.
* SAM application needs to be opened in ***Administrator mode*** for the ***first time*** in order to check if UnRARDLL is present on the local machine and if System Variable has beed created already in System Environment Variables. If their presence is not found they will be installed accordingly.
* System Variable parameters:
    - Variable Name: __UNRAR_LIB_PATH__
    - Variable Value: __C:\Program Files (x86)\UnrarDLL\x64\UnRAR64.dll__


*C.  UTILITIES*
*  In project root folder run __python setup.py build__ --> automatically incapsulates the app into an executable file using **setup.py** configuration file and **cx_Freeze** library. The command will create the app in the **build** folder


*D.  DEPENDENCIES*
* ***UnRARDLL-installer.exe*** is provided with the SAM installation file.
* SAM installation file will automatically ask for UnRARDLL installation on the local machine
* UnRARDLL installation files and extra information can be found on the [RARLAB](https://www.rarlab.com/rar_add.htm) website


*E.  COMPILERS*
* **INNO SETUP** has been used to create the installation file for the application
* Compiler settings have been saved in ***SAM-inno Setup.iss*** file
* On execution the compiler will export ***SAM - Installer.exe*** file in the ***SAM - Installer*** folder

*F.  MODULES*
* The following modules ***organize_folders.py*** and ***batch_download.py*** are responsible to organize the files in folders and login/download the required assets from the hosting platform.
* ***filters.json*** sets the folders structure and how the different file types will be spread in the root folder

*G.  USING THE APP*
* As a best practice is recommended to create a local Virtual Environment. This can be done by:
  * running **pip install virtualenv** to Install a Virtual Environment using Venv
  * To use venv in your project, in your terminal, create a new project folder (**mkdir projectABC**) in the terminal and run **python<version> -m venv <virtual-environment-name>** (**python3.11 -m venv env**)
  * cd in the terminal to the project folder (**cd projectABC**)
  * you will need to activate the virtual env (**source env/bin/activate** for MAC or **source/env/scripts/activate** for Windows)
  * running **pip list** should check if only base packages are present (pip and setup tools) in order for the activation to be correct
  * you can generate a text file listing all your project dependencies by running **pip freeze > requirements.txt**
  * to install the libararies required run **pip install -r requirements.txt**

**ORGANIZE FOLDERS**
* The first section of the app UI focuses on file management where the second one does the web crawling and downloads the data.
* Organzing multiple folders will require specifying their parent folder path when launching **Browse Location**. The folders that need to be organized must be selected in the **Organise Folders List**. 

!!! **Each folder should include at least an ***archive*** file with the asset and the ***preview*** as an image with 'preview' keyword present in the file name.**

* **Extract Archives** will unpack each archive found in corresponding folder
* **Run Organizer** will tidy the contents for the folders selected

**BATCH DOWNLOAD**
* You will be required to provide a ***.txt*** file that contains all the URLs in the **Links File**. You will need to specify the Download Folder and press **Download Links**.

* Pressing **Clear Junk** and **Clear Backup** buttons will remove these folders content in the parent folders specified.