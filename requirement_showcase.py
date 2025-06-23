import requests
from PIL import Image
from bs4 import BeautifulSoup
from io import BytesIO
gamelist = ['1091500','1245620', '730', '413150', '271590','1086940', '1145360', '292030', '1172470', '739630']
def k(app_id):
    return f'https://cdn.cloudflare.steamstatic.com/steam/apps/{app_id}/header.jpg'

for game_id in gamelist:
    html = k(game_id)
    response = requests.get(html)
    image_byte = response.content
    file_image = BytesIO(image_byte)
    img = Image.open(file_image)
    img.show()
    