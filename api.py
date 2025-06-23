import requests
import json
from bs4 import BeautifulSoup
import game_requirement
def parse_requirements_html(html_string: str) -> dict:
    """
    Phân tích chuỗi HTML cấu hình game thành một dictionary Python.
    """
    if not html_string:
        return {}
        
    soup = BeautifulSoup(html_string, 'html.parser')
    requirements = {}
    
    list_items = soup.find_all('li')
    
    for item in list_items:
        text = item.get_text(strip=True)
        
        if ':' in text:
            key, value = text.split(':', 1)
            key = key.strip()
            value = value.strip()
            requirements[key] = value
    print(requirements)
    return requirements

def get_structured_game_requirements(app_id: str):
    """
    Lấy thông tin cấu hình của game và trả về dưới dạng dictionary đã được xử lý.
    """
    url = f"https://store.steampowered.com/api/appdetails?appids={app_id}&l=en"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status() 
        data = response.json()
        
        if data and data.get(app_id, {}).get('success'):
            game_data = data[app_id]['data']
            pc_requirements_html = game_data.get('pc_requirements', {})
            
            min_req_html = pc_requirements_html.get('minimum')
            rec_req_html = pc_requirements_html.get('recommended')
            print(min_req_html)
            min_req_dict = parse_requirements_html(min_req_html)
            rec_req_dict = parse_requirements_html(rec_req_html)
            
            print(f"--- Lấy và xử lý dữ liệu thành công cho game: {game_data.get('name')} ---")
            return {
                "minimum": min_req_dict,
                "recommended": rec_req_dict
            }
        else:
            print(f"Không tìm thấy dữ liệu hoặc yêu cầu không thành công cho AppID: {app_id}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Lỗi kết nối hoặc HTTP: {e}")
        return None
    except (KeyError, json.JSONDecodeError) as e:
        print(f"Lỗi xử lý dữ liệu hoặc AppID không hợp lệ: {e}")
        return None
def from_str_to_object(str_requirements : dict):
    if not str_requirements:
        return
    try:
        OS_s = str_requirements.get('OS') or str_requirements.get('OS *') or str_requirements.get('ОС *')
    except KeyError:
        OS_s = "Unknown"

    CPU_s = str_requirements['Processor']
    RAM_s = str_requirements['Memory']
    GPU_s = str_requirements['Graphics']
    DirectX = str_requirements['DirectX']
    Storage = str_requirements['Storage']
    AdditionalNotes = str_requirements.get('Additional Notes', '')


    return game_requirement.Requirement( CPU_s, RAM_s, GPU_s, DirectX, Storage, OS_s, AdditionalNotes)

if __name__ == "__main__":
    # AppID của Cyberpunk 2077 là 1091500
    game_id = "570"
    
    str_requirements = get_structured_game_requirements(game_id)
    min_r = str_requirements['minimum']
    min_requirements = from_str_to_object(min_r)
    rec_r = str_requirements['recommended']
    print('red', rec_r)
    rec_requirements = from_str_to_object(rec_r)
    game = game_requirement.Game(Name='', Minimum=min_requirements, Recommended=rec_requirements)
    print(game)
    