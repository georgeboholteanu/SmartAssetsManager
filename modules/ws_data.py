# DEPENDENCY FILE FOR MAIN APP
import requests
import time
from bs4 import BeautifulSoup
import os
from modules import fix_dependencies as fix

########     LOAD PROJECT ENVIRONMENT VARIABLES      ########
fix.decrypt("ekey.key", "eenv")


# REPLACE/REMOVE SPECIAL CHARACTERS FROM STRING
def transform_string(input_string):
    # Define a list of characters to replace with hyphens or to be removed
    characters_to_replace = ["\\", "/", "|", ".", ",", ":"]
    characters_to_remove = [
        "?",
        "=",
        "!",
        "<",
        ">",
        "+",
        "%",
        "&",
        "$",
        "&amp;",
        "^",
        "#",
        "~",
    ]

    # Remove special characters in the string
    for char in characters_to_remove:
        input_string = input_string.replace(char, " ")

    # Replace each character in the input string with a hyphen
    for char in characters_to_replace:
        input_string = input_string.replace(char, "-")

    # input_string = ' '.join(input_string.split()) # already done earlier

    if input_string[-1] == "-":
        return input_string[:-2]
    else:
        return input_string


# CHECK STATUS OF URL
def check_url_status(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content

    else:
        print(f"Failed to fetch URL: {url}")
        return None


# EXTRACT ITEM NAME
def extract_item_name(url):
    if check_url_status(url):
        html_content = check_url_status(url)
        soup = BeautifulSoup(html_content, "html.parser")
        # Find the <div> with class "title"
        title_div = soup.find("div", class_="title")

        # Check if the <div> with class "title" exists
        if title_div:
            # Find the <a> tag within the <div>
            a_tag_name = title_div.find("a").text

            # Check if the <a> tag exists
            if not a_tag_name:
                print('No <a> tag found within the <div> with class "title".')
            else:
                item_name = " ".join(a_tag_name.split())

                # Replace/remove unwanted characters
                item_name = transform_string(item_name)

                # Trim the string to the last word with a maximum length of 50 characters
                if len(item_name) > 50:
                    item_name = item_name[:50]
                    last_space_index = item_name.rfind(" ")
                    if last_space_index != -1:
                        item_name = item_name[:last_space_index]

                return item_name
        else:
            print('No <div> with class "title" found in the HTML.')

    else:
        print("Error: Invalid CLOUD URL")


# EXTRACT ITEM URL
def extract_item_img_url(url):
    html_content = check_url_status(url)

    if html_content:
        soup = BeautifulSoup(html_content, "html.parser")

        # Define a list of target classes to look for
        target_classes = [
            "alignnone size-full aligncenter",
            "alignnone aligncenter",
            "alignnone",
        ]

        # Loop through the target classes
        for class_name in target_classes:
            # Find the element with the current class
            img_tag = soup.find("img", class_=class_name)

            # If the element with the current class is found, get its 'src'
            if img_tag:
                img_tag_url = img_tag["src"]
                return img_tag_url

            else:
                print(f"No <img> tag with the class '{class_name}' found in the HTML.")
    else:
        print("Error extracting item preview URL")


# EXTRACT THE CLOUD URL
def extract_stored_url(url):
    html_content = check_url_status(url)
    if html_content:
        soup = BeautifulSoup(html_content, "html.parser")

        # Find the <strong> tags within the <div class="entry"> element
        strong_tags = soup.find_all("strong")

        # Initialize a list to store the found cloud links
        found_cloud_links = []

        # Loop through the <strong> tags
        for strong_tag in strong_tags:
            # Find the next <p> tag after the <strong> tag
            next_p_tag = strong_tag.find_next("p")

        # Check if the <p> tag exists and its text starts with "https://"
        if next_p_tag and next_p_tag.text.startswith("https://"):
            found_cloud_links.append(next_p_tag.text)

        found_cloud_links = found_cloud_links[0].split("\n")
        return found_cloud_links
    else:
        print(f"Could not fetch HTML content from {url}")


# EXTRACT DATA TO CONTAINER ARRAY
def extract_data(url_array):  # url_array is the list of links on links_app
    container = []
    for url in url_array:
        container.append(
            [extract_item_name(url), extract_item_img_url(url), extract_stored_url(url)]
        )
    return(container)


# DOWNLOAD THE ITEM PREVIEW
def download_item_preview(target_path, preview_url, file_name):
    try:
        # Create a folder to save the downloaded image
        if not os.path.exists(target_path + "/" + file_name):
            os.makedirs(target_path + "/" + file_name)

        # Download the image and save it to the folder
        response = requests.get(preview_url)
        preview_file = target_path + "/" + file_name + "/" + file_name + "_preview.jpg"
        if not os.path.exists(preview_file):
            if response.status_code == 200:
                with open(preview_file, "wb") as f:
                    f.write(response.content)
                    print("Image downloaded successfully!")
            else:
                print("Error downloading image preview")
        else:
            print(
                "   Preview already exist in folder:   {}".format(
                    target_path + "/" + file_name
                )
            )
    except FileNotFoundError as e:
        print(e)


# LOGIN TO DOWNLOAD THE CLOUD URLs
def login_website():
    # Define the login URL and file download URL
    login_url = os.environ.get('auth_url')[1:-1]

    # Create a session to retain your login credentials and handle cookies
    session = requests.session()

    # Prepare the login data
    login_data = {
        "_csrf_token": session.cookies.get("__token"),
        "LoginForm[email]": os.environ.get('USR')[1:-1],
        "LoginForm[password]": os.environ.get('PAS')[1:-1],
        "LoginForm[rememberMe]": 1,
    }

    # Mimic a web browser by setting appropriate headers
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Referer": login_url,
    }

    # Add a delay to avoid being flagged as a bot
    time.sleep(5)

    # Send the login POST request with the login data and headers
    login_response = session.post(login_url, data=login_data, headers=headers)

    # Check if the login was successful
    if "Logout" in login_response.text:
        print("Login successful")
        return session
        # Additional actions after successful login
    else:
        print("Login failed")
        # Additional actions when login fails


# Webscrape data - crawler links -> cloud links
def webscrape_urls(selected_path, urls): # urls are the links_app urls
    container = extract_data(urls)
    print("   Items Collected! Downloading...", "\n")

    for item in container:
        if all(item) and len(item) == 3:
            # os.makedirs(item[0], exist_ok=True)

            # download the item preview from url
            # item[0] is the name of the item
            # item[1] is the url of the item image
            # item[2] is the CLOUD url of the item

            download_item_preview(
                selected_path, item[1], item[0]
            )  # also creates a new folder with item[0]
            print(item)
        else:
            print("!! ISSUE with:", item)

    # download each archive separately
    cloud_urls = [item[2] for item in container]
    session = login_website()

    # Download cloud URL
    for cloud_url in cloud_urls:
        # CASE 01 - single cloud URL
        if len(cloud_url) == 1:
            # Obtain the session cookie and file ID
            _token = session.cookies.get("__token")
            _file_id = session.cookies.get("file_id")

            # Send a GET request to download the file
            params = {"file_id": _file_id, "token": _token}

            response = session.get(cloud_url[0], params=params)

            if response.status_code == 200:
                # content = response.content
                soup = BeautifulSoup(response.content, "html.parser")
                direct_download_url = soup.find("div", {"class": "btm"}).find("a")[
                    "href"
                ]
                print(direct_download_url)

                # Find the corresponding item in the container list
                item = next(
                    (item for item in container if item[2] and cloud_url[0] in item[2]),
                    None,
                )
                if item:
                    file_name = item[0]
                    rar_file_path = (
                        selected_path + "/" + file_name + "/" + file_name + ".rar"
                    )

                    # Save the downloaded content to a file
                    with open(rar_file_path, "wb") as f:
                        f.write(session.get(direct_download_url).content)
                        print("Archive downloaded successfully.")
                else:
                    print("Failed to find item in container.")
            else:
                print("Archive download failed.")

        # CASE 02 - multiple cloud URLs
        elif len(cloud_url) > 1:
            for i in range(len(cloud_url)):
                # Obtain the session cookie and file ID
                _token = session.cookies.get("__token")
                _file_id = session.cookies.get("file_id")

                # Send a GET request to download the file
                params = {"file_id": _file_id, "token": _token}

                response = session.get(cloud_url[i], params=params)

                if response.status_code == 200:
                    # content = response.content
                    soup = BeautifulSoup(response.content, "html.parser")
                    direct_download_url = soup.find("div", {"class": "btm"}).find("a")[
                        "href"
                    ]
                    print(f"{item[0]}: {direct_download_url} [1/{i+1}]")

                    # Find the corresponding item in the container list
                    item = next(
                        (
                            item
                            for item in container
                            if item[2] and cloud_url[i] in item[2]
                        ),
                        None,
                    )
                    if item:
                        file_name = item[0]
                        rar_file_path = (
                            selected_path
                            + "/"
                            + file_name
                            + "/"
                            + file_name
                            + "_"
                            + str(i + 1)
                            + ".rar"
                        )

                        # Save the downloaded content to a file
                        with open(rar_file_path, "wb") as f:
                            f.write(session.get(direct_download_url).content)
                            print("Archive downloaded successfully.")
                    else:
                        print("Failed to find item in container.")
                else:
                    print("Archive download failed.")

    print("DOWNLOADING FINISHED!")


# Webscrape data - direct cloud links
def download_cloud_urls(selected_path, cloud_urls):
    session = login_website()

    # Download Cloud URL
    for url in cloud_urls:
        # Obtain the session cookie and file ID
        _token = session.cookies.get("__token")
        _file_id = session.cookies.get("file_id")

        # Send a GET request to download the file
        params = {"file_id": _file_id, "token": _token}

        response = session.get(url, params=params)

        if response.status_code == 200:
            # content = response.content
            soup = BeautifulSoup(response.content, "html.parser")
            direct_download_url = soup.find("div", {"class": "btm"}).find("a")["href"]

            extracted_file_name = url.split("/")[-1].split(".html")[0]
            archive_path = (
                selected_path + "/" + extracted_file_name
                if extracted_file_name.lower().endswith((".rar", ".zip"))
                else extracted_file_name + ".zip"
            )

            # Save the downloaded content to a file
            with open(archive_path, "wb") as f:
                f.write(session.get(direct_download_url).content)
                print("Archive downloaded successfully.")

        else:
            print("Archive download failed.")

    print("DOWNLOADING FINISHED!")
