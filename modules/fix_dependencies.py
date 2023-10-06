# DEPENDENCY FILE FOR MAIN APP

import subprocess
import os
from cryptography.fernet import Fernet

def decrypt(key_file_path, env_file_path): 
    try:   
        # Check if the files exist before proceeding
        if not (os.path.exists(key_file_path) and os.path.exists(env_file_path)):
            print("Error: 'ekey.key' or 'eenv' files not found.")
            return
    
        with open(key_file_path, 'rb') as key_file:
            key = key_file.read()

        cipher_suite = Fernet(key)
        # Read the encrypted .env file
        with open(env_file_path, 'rb') as file:
            encrypted_contents = file.read()

        # Decrypt the contents
        decrypted_contents = cipher_suite.decrypt(encrypted_contents)

        # Convert the decrypted contents to a string and parse it into environment variables
        env_lines = decrypted_contents.decode('utf-8').splitlines()

        for line in env_lines:
            if '=' in line:
                key, value = line.split('=', 1)
                # Set the environment variables in your application
                os.environ[key] = value
        
    except Exception as e:
        print("An error occurred during decryption:", str(e))

########     INSTALL 7ZIP APP IF NOT FOUND    ########
def install_sevenzip():
    sevenzip_exe_file = r"C:\Program Files\7-Zip\7z.exe"
    sevenzip_installer = None
    
    ########     DECRYPT ENVIRONMENT VARIABLES      ########
    decrypt("ekey.key", "eenv")
    
    # install 7zip    
    try:
        if not os.path.exists(sevenzip_exe_file):            
            
            # Install 7zip FROM PATH
            sevenzip_installer = os.environ.get('sevenzip_installer_path')[1:-1]
            if sevenzip_installer is not None:
                try:
                    if not os.path.exists(sevenzip_installer):
                        raise FileNotFoundError(f"The 7z.exe file was not found at the specified path: {sevenzip_exe_file}")
                    
                    # Use subprocess to run the installer
                    subprocess.run(sevenzip_installer, check=True)
                    print(".exe file executed successfully.")
                except subprocess.CalledProcessError as e:
                    print(f"Error while executing the .exe file (process canceled by user): {e}")
                except FileNotFoundError as e:
                    print(e)
                except Exception as e:
                    print(f"An error occurred: {e}")
            else:
                print("The 7z.exe file was not found at the specified not found in 'C:/Program Files/7-Zip'. Try runnning the app in ADMIN mode to install it!")
        else:
            pass
    except Exception as e:        
        print(f"Error with path: {sevenzip_exe_file}, error: {e}")
