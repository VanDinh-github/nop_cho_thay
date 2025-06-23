import os
import requests
def get_image(app_id : str) -> str:
    #where cache is stored
    cache_path = f'cache/{app_id}.jpg' 

    if os.path.exists(cache_path):
        #If already have, use it
        return cache_path
    else:
        url = f"https://cdn.cloudflare.steamstatic.com/steam/apps/{app_id}/header.jpg"
        response = requests.get(url)

        if response.status_code == 200:
            os.makedirs("cache", exist_ok=True)  
            with open(cache_path, "wb") as f:
                f.write(response.content)
            return cache_path
        else:
            raise Exception(f"Lỗi tải {app_id}: {response.status_code}")

if __name__ == '__main__':
    from PIL import Image
    path = get_image('346110')
    img = Image.open(path)
    img.show()