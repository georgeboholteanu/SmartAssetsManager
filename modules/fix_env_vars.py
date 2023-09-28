# DEPENDENCY FILE FOR MAIN APP

import subprocess
import winreg
import os
from dotenv import load_dotenv


########     LOAD PROJECT ENVIRONMENT VARIABLES      ########
load_dotenv()
proj_path = os.getenv('proj_path')

########     SET SYSTEM ENVIRONMENT VARIABLES      ########
def set_environment_variables():
    # The name and value of the environment variable you want to set
    variable_name = "UNRAR_LIB_PATH"
    variable_value = r"C:\Program Files (x86)\UnrarDLL\x64\UnRAR64.dll"

    try:
        # Open the Windows Registry key for environment variables in read mode
        key = winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment",
            0,
            winreg.KEY_READ,
        )

        try:
            # Get the current value associated with variable_name
            existing_value, value_type = winreg.QueryValueEx(key, variable_name)

            # Compare the existing value with the value you want to set
            if existing_value == variable_value:
                pass
                # print(f"The environment variable '{variable_name}' already exists with the same value. OK!")
            else:
                # If the values don't match, you can set the environment variable
                key = winreg.OpenKey(
                    winreg.HKEY_LOCAL_MACHINE,
                    r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment",
                    0,
                    winreg.KEY_SET_VALUE,
                )
                winreg.SetValueEx(key, variable_name, 0, winreg.REG_SZ, variable_value)
                winreg.CloseKey(key)
                print(f"Environment variable '{variable_name}' set successfully.")
        except FileNotFoundError:
            # If the variable does not exist, you can set it
            key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment",
                0,
                winreg.KEY_SET_VALUE,
            )
            winreg.SetValueEx(key, variable_name, 0, winreg.REG_SZ, variable_value)
            winreg.CloseKey(key)
            print(f"Environment variable '{variable_name}' set successfully.")

        # Close the registry key
        winreg.CloseKey(key)
    except PermissionError:
        print("Permission error. Make sure you have administrator privileges.")
    except Exception as e:
        print(f"An error occurred: {e}")


########     INSTALL UNRARLL MODULE IF NOT FOUND    ########
def install_unrar():
    unrar_path = r"C:/Program Files (x86)/UnrarDLL/x64/UnRAR64.dll"
    try:
        if not os.path.exists(unrar_path):
            # Install UNRARDLL FROM PATH
            unrar_installer = os.getenv('unrar_installer_path')
            if unrar_installer:
                try:
                    if not os.path.exists(unrar_installer):
                        raise FileNotFoundError(f"The .exe file was not found at the specified path: {unrar_installer}")
                    
                    # Use subprocess to run the installer
                    subprocess.run(unrar_installer, check=True)
                    print(".exe file executed successfully.")
                except subprocess.CalledProcessError as e:
                    print(f"Error while executing the .exe file: {e}")
                except FileNotFoundError as e:
                    print(e)
                except Exception as e:
                    print(f"An error occurred: {e}")
            else:
                print("Environment variable 'unrar_installer_path' not set.")
        else:
            try:
                from unrar import rarfile
            except ImportError:
                print("RAR module not found. You may need to install it.")
    except Exception as e:
        print(f"Error with path: {unrar_path}, error: {e}")

