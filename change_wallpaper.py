import re
import requests
import random
import os
import ctypes
import tempfile  # Import the tempfile module

def download_random_image(url):
    # Make the HTTP request
    response = requests.get(url)
    
    # Ensure the response is successful
    if response.status_code == 200:
        # Extract the text content from the response
        text_content = response.text
        
        # Regular expression to extract URLs ending with .jpg
        url_pattern = r'(https?://[^\s]+\.jpg|www\.[^\s]+\.jpg)'
        jpg_urls = re.findall(url_pattern, text_content)

        # If there are .jpg URLs found
        if jpg_urls:
            # Select one randomly
            selected_url = random.choice(jpg_urls)
            upscale_resolution = f"https://w.wallhaven.cc/full/{selected_url[30:32]}/wallhaven-{selected_url[33:43]}"
            print(f"Selected image URL: {upscale_resolution}")
            
            # Download the image
            image_response = requests.get(upscale_resolution, stream=True)
            if image_response.status_code == 200:
                # Save the image to a temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
                    for chunk in image_response.iter_content(1024):
                        temp_file.write(chunk)
                    temp_image_path = temp_file.name
                print(f"Image downloaded to temporary file: {temp_image_path}")
                
                # Set the downloaded image as the desktop wallpaper
                ctypes.windll.user32.SystemParametersInfoW(20, 0, temp_image_path, 3)
            else:
                print(f"Failed to download image: {upscale_resolution}")
        else:
            print("No .jpg images found in the text.")
    else:
        print(f"Failed to retrieve content. Status code: {response.status_code}")


def set_wallpaper(search_image):
    # Example URL to scrape images from
    source_url = f"https://wallhaven.cc/search?q={search_image}&categories=111&purity=110&resolutions=2560x1080%2C1920x1080&sorting=relevance&order=desc&ai_art_filter=1"
    download_random_image(source_url)


if __name__ == '__main__':
    set_wallpaper("super car")
