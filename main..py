import requests
from io import BytesIO
from tkinter import *
from PIL import Image, ImageTk

# Replace with your own Pexels API key
API_KEY = "YOUR_PEXELS_API_KEY"
url = "https://api.pexels.com/v1/search"

headers = {
    "Authorization": API_KEY
}

while True:
    query = input("Enter image to search (or 'quit' to exit): ")

    if query.lower() == "quit":
        break

    params = {
        "query": query,
        "per_page": 5
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()

        if len(data["photos"]) == 0:
            print("No images found!")
            continue

        root = Tk()
        root.title(f"Smart Image Finder - {query}")

        photos = []

        for i, photo_data in enumerate(data["photos"][:5]):
            image_url = photo_data["src"]["medium"]

            img_data = requests.get(image_url).content

            image = Image.open(BytesIO(img_data))
            image = image.resize((250, 180))

            photo = ImageTk.PhotoImage(image)
            photos.append(photo)

            label = Label(root, image=photo)
            label.image = photo
            label.grid(row=i // 3, column=i % 3, padx=5, pady=5)

        root.mainloop()

    else:
        print("Error:", response.status_code)
