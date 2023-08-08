import os
import requests
import csv

def download(
        images_csv_path: str,
    ) -> list:
    """
    Downloads images from kramerius.mzk.cz
    """

    images = []

    with open(images_csv_path, "r") as csv_file:
        skipped_first_line = csv_file.readline()
        for line in csv_file:
            info = line.split(",")
            uuid = info[0]
            x = info[1]
            y = info[2]
            width = info[3]
            height = info[4]
            dpi = info[5]

            url = f"https://kramerius.mzk.cz/search/iiif/uuid:{uuid}/{x},{y},{width},{height}/max/0/default.jpg"
            image_path = f"./data/backgrounds/images/{uuid}_{x}_{y}_{width}_{height}.jpg"

            if not os.path.exists(image_path):
                print(f"Downloading {uuid}_{x}_{y}_{width}_{height}...")
                r = requests.get(url, allow_redirects=True)
                open(image_path, "wb").write(r.content)
            else:
                print(f"Skipping {uuid}_{x}_{y}_{width}_{height}...")
            
            images.append(image_path)
    
    return images
