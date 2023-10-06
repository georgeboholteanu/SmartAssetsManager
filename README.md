[![python3.10.6](https://img.shields.io/badge/Python-3660AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/downloads/release/python-3106/)
[![mail me](https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:george.boholteanu@gmail.com)
![](https://img.shields.io/badge/web--scraping-1452A.svg)
![](https://img.shields.io/badge/files--encryption-27282D.svg)
![](https://img.shields.io/badge/files--management-13245A.svg)


*A.  DESCRIPTION*

The app can be used to automate downloading and organising of multiple assests into individual specific folder structure.

It uses **requests** module to login on hosting platform of the assets and download them from the selected URLs.

<img src="./assets/app_mockup.jpg" alt="SAM" width="300">


*B.  REQUIREMENTS*
* The application is compatible with machines running **WINDOWS 10/11 OS**.
* ***7 Zip*** is required to unpack archive files.
* SAM application can check if ***7 Zip*** is present on the local machine if is opened in ***Administrator mode***. If their presence is not found they will be installed accordingly.

*C.  UTILITIES*
*  In project root folder run __python setup.py build__ --> automatically freezes the app into an executable file using **setup.py** configuration file and **cx_Freeze** library. The command will create the app in the **build** folder


*D.  DEPENDENCIES*
* ***7 Zip Installer*** is provided with the SAM installation file.
* SAM installation file will automatically ask for 7 Zip installation on the local machine
* 7 Zip installation files and extra information can be found on the [7ZIP](https://www.7-zip.org/) website


*E.  COMPILERS*
* **INNO SETUP** can be used to create the installation file for the application
* 

*F.  MODULES*
* The following modules ***organize_folders.py*** and ***ws_data.py*** are responsible to organize the files in folders and login/download the required assets from the hosting platform.
* ***filters.json*** sets the folders structure and how the different file types will be spread in the root folder

*G.  USING THE APP*  

  As a best practice is recommended to create a local Virtual Environment. This can be done by:
  * running **pip install virtualenv** to Install a Virtual Environment using Venv
  * To use venv in your project, in your terminal, create a new project folder (**mkdir projectABC**) in the terminal and run **python<version> -m venv <virtual-environment-name>** (**python3.10 -m venv env**)
  * cd in the terminal to the project folder (**cd projectABC**)
  * you will need to activate the virtual env (**source env/bin/activate** for MAC or **source/env/scripts/activate** for Windows)
  * running **pip list** should check if only base packages are present (pip and setup tools) in order for the activation to be correct
  * to install the libraries required run **pip install -r requirements.txt**
  * in case you want to make changes and add use custom libraries you can generate a requirements text file listing all your project dependencies by running **pip freeze > requirements.txt**

**ORGANIZE FOLDERS**
* The first section of the app UI focuses on file management where the second one does the web crawling and downloads the data.
* Organzing multiple folders will require specifying their parent folder path when launching **Browse Location**. The folders that need to be organized must be selected in the **Organise Folders List**. 

!!! **Each folder should include at least an ***archive*** file with the asset and the ***preview*** as an image with 'preview' keyword present in the file name.**

* **Extract Archives** will unpack each archive found in corresponding folder
* **Run Organizer** will tidy the contents for the folders selected
* Pressing **Clear Junk** and **Clear Backup** buttons will remove these folders content in the parent folders specified.


**Getting the data**
* You will be required to provide a ***.txt*** file that contains all the URLs in the **Links File**. You will need to specify the Download Folder and press **Get ->Links File**.

