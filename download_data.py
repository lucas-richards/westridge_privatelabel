import os
import requests
import json

# Load data from the JSON file
with open('Assets_with_code.json', 'r') as file:
    data = json.load(file)

# Directory to save the downloads
download_dir_img = "downloads/images"
download_dir_att = "downloads/attachments"

os.makedirs(download_dir_img, exist_ok=True)
os.makedirs(download_dir_att, exist_ok=True)

def download_file(url, folder, filename):
    local_filename = os.path.join(folder, filename)
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename

for item in data:
    item_code = item["code"]
    
    # Download image
    if "image" in item and item["image"]:
        item_folder = os.path.join(download_dir_img, item_code)
        os.makedirs(item_folder, exist_ok=True)
        print(f"Downloading image for {item['name']}")
        download_file(item["image"], item_folder, f"{item_code}.jpg")
    
    # Download attachments
    if "attachments" in item and item["attachments"]:
        attachments = item["attachments"].split(",")
        for attachment in attachments:
            item_folder = os.path.join(download_dir_att, item_code)
            os.makedirs(item_folder, exist_ok=True)
            print(f"Downloading attachment for {item['name']}")
            attachment_name = attachment.split("/")[-1]
            download_file(attachment, item_folder, attachment_name)

print("Download completed.")
