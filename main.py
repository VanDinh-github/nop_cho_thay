from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from kivy.animation import Animation
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.navigationdrawer import MDNavigationDrawer, MDNavigationDrawerItem
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.list import OneLineListItem
from kivymd.uix.dialog import MDDialog
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.core.text import LabelBase
from kivy.uix.image import Image
from kivymd.uix.behaviors import HoverBehavior
from kivymd.uix.menu import MDDropdownMenu
from kivy.clock import Clock
import os
from kivy.metrics import dp
import json
from models.hardwares import CPU, GPU, Mainboard, RAM, PSU, OS
from models.pc import PC
import requests
from game_requirement import *
from bs4 import BeautifulSoup
from get_image import get_image
import re
import sys
# dismiss() là để đóng 1 widget dạng pop-up, dialog, hoặc menu tạm thời

def resource_path(relative_path):
    """Trả về đường dẫn tuyệt đối, phù hợp khi chạy trong PyInstaller --onefile"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.abspath(relative_path)

class BuildCheckApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dialog = None
        self.pc_config = None

        # Load dữ liệu từ JSON
        self.cpu_data = self.load_component(resource_path('datas/cpu.json'))
        self.gpu_data = self.load_component(resource_path('datas/gpu.json'))
        self.ram_data = self.load_component(resource_path('datas/ram.json'))
        self.mainboard_data = self.load_component(resource_path('datas/mainboard.json'))
        self.psu_data = self.load_component(resource_path('datas/psu.json'))
        self.os_data = self.load_component(resource_path('datas/os.json'))

        # Dữ liệu phần cứng tổng hợp
        self.data = {
            'cpu': {'data': self.cpu_data, 'class': CPU, 'menu': None},
            'gpu': {'data': self.gpu_data, 'class': GPU, 'menu': None},
            'ram': {'data': self.ram_data, 'class': RAM, 'menu': None},
            'mainboard': {'data': self.mainboard_data, 'class': Mainboard, 'menu': None},
            'psu': {'data': self.psu_data, 'class': PSU, 'menu': None},
            'os': {'data': self.os_data, 'class': OS, 'menu': None}
        }

        self.game_data = self.load_component(resource_path('datas/steam_games_cache.json'))
        self.game_menu = None
        self.search_trigger = None
        self.selected_game = None

        self.logo_img_path = resource_path('assets/images/logo.png')
        self.nen_img_path = resource_path('assets/images/nen.png')
        self.cpu_img_path =  resource_path("assets/images/cpu.jpeg")
        self.ram_img_path = resource_path("assets/images/ramc.JPG")
        self.gpu_img_path =resource_path("assets/images/gpu.jpg")
        self.mainb_img_path =resource_path("assets/images/maib.jpg")
        self.psu_img_path = resource_path("assets/images/psu.jpeg")
        self.icon_img_path = resource_path("assets/images/icon.png")
        self.i1 =resource_path("assets/view/blackwithwukong.PNG")
        self.i2 =resource_path("assets/view/dota_2.PNG")
        self.i3 = resource_path( "assets/view/ark.PNG")
        self.i4 =resource_path( "assets/view/pubg.PNG")
        self.i5 = resource_path("assets/view/gta5.PNG")

    def build(self):
        # Load các file KV qua resource_path
        Builder.load_file(resource_path('gui/home_screen.kv'))
        Builder.load_file(resource_path('gui/pc_input_screen.kv'))
        Builder.load_file(resource_path('gui/select_game_screen.kv'))
        Builder.load_file(resource_path('gui/compatibility_screen.kv'))
        Builder.load_file(resource_path('gui/details_screen.kv'))
        return Builder.load_file(resource_path('gui/main.kv'))

    def load_component(self, file_path):
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                return data
        else:
            return 'file not found'
    

    def set_screen(self, name):
        self.root.ids.screen_manager.current = name
    
    def on_profile(self):
        print("Hồ sơ người dùng")

    def on_settings(self):
        print("Mở cài đặt")
    
    def clear_pc_input(self):
        # Xóa tất cả các trường nhập
        for screen in self.root.ids.screen_manager.screens:
            if screen.name == 'pc_input':
                for widget in screen.walk():
                    if isinstance(widget, MDTextField):
                        widget.text = ''
                break
    def show_exit_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Xác nhận thoát",
                text="Bạn muốn thoát ứng dụng?",
                buttons=[
                    MDFlatButton(
                        text="HỦY", text_color=self.theme_cls.primary_color,
                        on_release=lambda x: self.dialog.dismiss()
                    ),
                    MDFlatButton(
                        text="THOÁT", text_color=self.theme_cls.primary_color,
                        on_release=lambda x: self.stop()
                    ),
                ],
            )
        self.dialog.open()
    
    def on_component_model_text(self, component_type,  text_field):
        
        if self.search_trigger:
            self.search_trigger.cancel()

        # Lên lịch gọi hàm tìm kiếm sau 0.4 giây
        self.search_trigger = Clock.schedule_once(
            lambda dt: self.show_component_suggestions(component_type, text_field), 0.4
        )

    def show_component_suggestions(self, component_type, text_field):
        search_text = text_field.text.lower()
        # for item in self.data[component_type]['data']:
        #     if search_text in item['name']:
        #         try:
        #              filtered_components = [self.data[component_type]['class'](**item)]
        #         except:
        #             print(item)
        search_text = text_field.text.strip().lower()
        search_keywords = search_text.split()
        filtered_components = [
            self.data[component_type]['class'](**item)
            for item in self.data[component_type]['data']
            if all(keyword in item['name'].lower() for keyword in search_keywords)
        ]

        menu_items = [
            {
                "text": component.name,
                "viewclass": "OneLineListItem",
                "height": dp(48),
                "on_release": lambda x=component: self.select_component(text_field, component=x, component_type=component_type,  )
            } for component in filtered_components 
        ]

        if self.data[component_type]['menu']:
            self.data[component_type]['menu'].dismiss()
        
        self.data[component_type]['menu'] = MDDropdownMenu(
            caller=text_field,
            items=menu_items,
            width_mult=4,
            max_height=dp(300),
            position="bottom",
            
        )
        if menu_items:
            self.data[component_type]['menu'].open()


    def select_component(self, text_field, component, component_type):

        screen = self.root.ids.screen_manager.get_screen('pc_input')
        if component_type == 'cpu':
            screen.ids.cpu_model.text = component.name
            screen.ids.cpu_cores.text = str(component.core_count)
            screen.ids.cpu_socket.text = component.socket
            screen.ids.cpu_tdp.text = component.tdp
            screen.ids.cpu_coreclock.text = str(component.core_clock)
            screen.ids.cpu_boost.text = str(component.boost_clock)
            
        elif component_type == 'gpu': 
            
            screen.ids.gpu_model.text=component.name
            screen.ids.gpu_vram.text=str(component.vram)
            screen.ids.gpu_boostclock.text=str(component.boost_clock)
            screen.ids.gpu_tdp.text=str(component.tdp)
            screen.ids.gpu_chipset.text=str(component.chipset)
            screen.ids.gpu_coreclock.text=str(component.core_clock)
            screen.ids.gpu_length.text=str(component.length)
            screen.ids.gpu_color.text=str(component.color)
            
        elif component_type == 'ram':
            screen.ids.ram_model.text=component.name
            screen.ids.ram_capa.text=str(component.capacity)
            screen.ids.speed_ram.text=str(component.speed)
            screen.ids.ram_type.text=str(component.ram_type)
            screen.ids.ram_color.text=str(component.color)
            
            
        elif component_type == 'mainboard':
            screen.ids.mainboard_model.text=component.name
            screen.ids.mainboard_socket.text=component.socket
            screen.ids.mainboard_form.text=component.form_factor
            screen.ids.mainboard_chipset.text=component.chipset
            screen.ids.mainboard_ramtype.text=component.ram_type 
            screen.ids.pcie.text=component.pcie_version
            screen.ids.mainboard_max.text=component.max_memory
            screen.ids.slots.text=component.memory_slots
            screen.ids.mainboard_color.text=component.color
            

        elif component_type == 'psu':
            screen.ids.psu_model.text=component.name
            screen.ids.psu_wattage.text=str(component.wattage)
        
        elif component_type == 'os':
            screen.ids.os.text=component.name

        if self.data[component_type]['menu']:
            self.data[component_type]['menu'].dismiss()
      
    def validate_required_fields(self):
        screen = self.root.ids.screen_manager.get_screen('pc_input')

        # Danh sách các trường bắt buộc
        required_fields = {
            'cpu_model': screen.ids.cpu_model,
            'gpu_model': screen.ids.gpu_model,
            'ram_model': screen.ids.ram_model,
            'mainboard_model': screen.ids.mainboard_model,
            'psu_model': screen.ids.psu_model,

        }

        is_valid = True

        for field_id, field in required_fields.items():
            if not field.text.strip():
                # Nếu trống, hiển thị lỗi
                field.error = True
                field.helper_text = "Trường bắt buộc!"
                field.helper_text_mode = "on_error"
                is_valid = False
            else:
                # Nếu hợp lệ, xóa thông báo lỗi
                field.error = False
                field.helper_text = ""
                field.helper_text_mode = "on_focus"
        

        return is_valid
    def check_pc_compatibility(self):
        if not self.validate_required_fields():
            return

        screen = self.root.ids.screen_manager.get_screen('pc_input')
        # Tạo đối tượng PC từ dữ liệu nhập
        
        cpu = CPU(
            name=screen.ids.cpu_model.text,
            core_count=int(float(screen.ids.cpu_cores.text)),
            socket=screen.ids.cpu_socket.text,
            tdp=int(float(screen.ids.cpu_tdp.text)),
            core_clock=float(screen.ids.cpu_coreclock.text),
            boost_clock=screen.ids.cpu_boost.text
        )

        gpu = GPU(
            name=screen.ids.gpu_model.text,
            memory=screen.ids.gpu_vram.text,
            boost_clock=screen.ids.gpu_boostclock.text,
            tdp=int(float(screen.ids.gpu_tdp.text)),
            chipset=screen.ids.gpu_chipset.text,
            core_clock=int(float(screen.ids.gpu_coreclock.text)),
            length=int(float(screen.ids.gpu_length.text)),
            color=screen.ids.gpu_color.text
        )
        ram = RAM(
            name=screen.ids.ram_model.text,
            capacity=int(float(screen.ids.ram_capa.text)),
            speed=screen.ids.speed_ram.text,
            ram_type=screen.ids.ram_type.text,
            color=screen.ids.ram_color.text
        )
        mainboard = Mainboard(
            name=screen.ids.mainboard_model.text,
            socket=screen.ids.mainboard_socket.text,
            form_factor=screen.ids.mainboard_form.text,
            chipset=screen.ids.mainboard_chipset.text,
            ram_type=screen.ids.mainboard_ramtype.text ,
            pcie_version=screen.ids.pcie.text,
            max_memory=screen.ids.mainboard_max.text,
            memory_slots=screen.ids.slots.text,
            color=screen.ids.mainboard_color.text
        )
        psu = PSU(
            name=screen.ids.psu_model.text,
            wattage=int(float(screen.ids.psu_wattage.text))
        )
        os=screen.ids.os.text
        

        pc = PC(cpu, gpu, ram, mainboard, psu, os)
        result = pc.check_compatible()

        
        screen.ids.compatibility_text.text = result
        screen.ids.compatibility_result.md_bg_color = [0.2, 0.8, 0.2, 1] if result == "Cấu hình tương thích!" else [1, 0.2, 0.2, 1]

    # Kiem tra dau vao hop le, neu ko hien canh bao
    def on_submit_pc_input(self):
        if self.validate_required_fields():
            screen = self.root.ids.screen_manager.get_screen('pc_input')
            ids = screen.ids
            self.pc_config = {
                'OS': ids.os.text.strip(),
                'CPU': ids.cpu_model.text.strip(),
                'CPU_CoreClock': ids.cpu_coreclock.text.strip(),
                'CPU_BoostClock': ids.cpu_boost.text.strip(),
                'CPU_Cores': ids.cpu_cores.text.strip(),
                'RAM': ids.ram_capa.text.strip(),
                'GPU': ids.gpu_model.text.strip(),
                "GPU_chipset": ids.gpu_chipset.text.strip(),
                'GPU_VRAM': ids.gpu_vram.text.strip(),
                'Mainboard': ids.mainboard_model.text.strip(),
                'PSU': ids.psu_wattage.text.strip(),
            }    
            print(f"Cấu hình PC đã lưu: {self.pc_config}") 
            screen_table = self.root.ids.screen_manager.get_screen('compatibility')
            screen_table.ids.cpu_name.text=self.pc_config['CPU']
            screen_table.ids.pc_ram.text=self.pc_config['RAM'] + ' GB'
            screen_table.ids.pc_gpu.text=self.pc_config['GPU_chipset']
            screen_table.ids.os.text=self.pc_config['OS']

        else:         
            self.show_error_dialog("Điền đầy đủ các dòng bắt buộc !!!!")
    def show_error_dialog(self, message):
        if self.dialog:
            self.dialog.dismiss()
        self.dialog = MDDialog(
            title="Thiếu thông tin",
            text=message,
            buttons=[
                MDFlatButton(
                    text="OK", text_color=self.theme_cls.primary_color,
                    on_release=lambda x: self.dialog.dismiss()
                )
            ],
        )
        self.dialog.open()
    def search_games(self, search_text):
        """Tìm kiếm game dựa trên văn bản nhập và cập nhật RecycleView."""
        search_text = search_text.strip().lower()
        search_keywords = search_text.split()
        filtered_games = [
            {"text": name, "app_id": app_id}
            for name, app_id in self.game_data.items()
            if all(keyword in name.lower() for keyword in search_keywords)
        ]

        try:
            screen = self.root.ids.screen_manager.get_screen('select_game')
            screen.ids.game_list.data = [
                {
                    "text": game["text"],
                    "on_press": lambda x=game["app_id"], y=game["text"]: self.select_game(y, x)
                }
                for game in filtered_games
            ]
        except Exception as e:
            print(f"Không cập nhật được danh sách game: {e}")
    
    def update_suggestions(self, search_text):
        if hasattr(self, 'search_trigger') and self.search_trigger:
            self.search_trigger.cancel()
        self.show_game_suggestions(search_text)






    def select_game(self, game_name, app_id):
        """Cập nhật thông tin game được chọn."""
        try:
            screen = self.root.ids.screen_manager.get_screen('select_game')
            ids = screen.ids
        except Exception as e:
            print(f"Không truy cập được screen hoặc ids: {e}")
            return

        # Lấy dữ liệu game từ cache hoặc API
        game_data = self.get_structured_game_requirements(str(app_id))
        if not game_data:
            ids.game_name.text = "Lỗi: Không lấy được dữ liệu game. Hãy kết nối Internet"
            ids.game_image.source = "gpu.jpg"
            ids.game_requirements.text = "Không có thông tin cấu hình"
            return

        min_req = None
        min_req_text = "Không có thông tin cấu hình tối thiểu."
        if game_data.get('minimum'):
            try:
                min_req = self.from_str_to_object(game_data['minimum'])
                min_req_text = (
                    f"Cấu hình tối thiểu:\n"
                    f"OS: {min_req.OS}\n"
                    f"CPU: {min_req.CPU}\n"
                    f"RAM: {min_req.RAM}\n"
                    f"GPU: {min_req.GPU}\n"
                    f"DirectX: {min_req.DirectX}\n"
                    f"Storage: {min_req.Storage}"
                )
            except Exception as e:
                print(f"Lỗi khi xử lý yêu cầu tối thiểu: {e}")

        

        self.selected_game = Game(
            Name=game_data.get('name', 'Unknow'),
            Minimum=min_req,
            Image=get_image(str(app_id))
        )

        ids.game_name.text = self.selected_game.Name
        ids.game_image.source = self.selected_game.Image
        ids.game_requirements.text = min_req_text

    def show_game_suggestions(self, search_text):
        search_text = search_text.strip().lower()
        search_keywords = search_text.split()
        filtered_games = [
            {"name": name, "app_id": app_id}
            for name, app_id in self.game_data.items()
            if all(keyword in name.lower() for keyword in search_keywords)
        ]

        screen = self.root.ids.screen_manager.get_screen('select_game')
        text_field = screen.ids.get('game_input', None)
        if not text_field:
            print("Không tìm thấy trường nhập game.")
            return

        if self.game_menu:
            self.game_menu.dismiss()

        self.menu_game_buffer = {}  # 💡 Dùng để lưu trữ tham chiếu an toàn

        menu_items = []
        for idx, game in enumerate(filtered_games):
            self.menu_game_buffer[idx] = game  # lưu mạnh reference

            menu_items.append({
                "text": game["name"],
                "viewclass": "OneLineListItem",
                "height": dp(48),
                "on_release": lambda idx=idx: self.on_game_selected(idx)
            })

        self.game_menu = MDDropdownMenu(
            caller=text_field,
            items=menu_items,
            width_mult=4,
            max_height=dp(300),
            position="bottom",
        )

        if menu_items:
            self.game_menu.open()

    def on_game_selected(self, idx):
        if self.game_menu:
            self.game_menu.dismiss()

        game = self.menu_game_buffer.get(idx)
        if not game:
            print("Không tìm thấy game trong buffer.")
            return

        game_name = game["name"]
        app_id = game["app_id"]

        if not hasattr(self, 'root') or not self.root:
            print("Root widget không tồn tại.")
            return

        try:
            screen_manager = self.root.ids.get('screen_manager')
            if not screen_manager:
                print("ScreenManager không tồn tại trong ids.")
                return

            screen = screen_manager.get_screen('select_game')
            if not screen:
                print("Màn hình select_game không tồn tại.")
                return

            ids = screen.ids
            self.select_game(game_name, app_id, ids)
        except Exception as e:
            print(f"Không truy cập được screen hoặc ids: {e}")

    def get_structured_game_requirements(self, app_id: str):
        url = "https://store.steampowered.com/api/appdetails?appids=" + app_id +'&l=en'
    
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status() 
            data = response.json()
            
            if data and data.get(app_id, {}).get('success'):
                game_data = data[app_id]['data']
                pc_requirements_html = game_data.get('pc_requirements', {})
                print(pc_requirements_html)
                min_req_html = pc_requirements_html.get('minimum')
                
                min_req_dict = self.parse_requirements_html(min_req_html)
                
                
                print(f"--- Lấy và xử lý dữ liệu thành công cho game: {game_data.get('name')} ---")
                return {'name': game_data.get('name'),
                    "minimum": min_req_dict
                    
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
    
    def parse_requirements_html(self, html_string: str) -> dict:
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
                
        return requirements
    def from_str_to_object(self, str_requirements : dict):
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


        return Requirement( CPU_s, RAM_s, GPU_s, DirectX, Storage, OS_s, AdditionalNotes)
        
    def check_compatibility(self):
        """Chuyển sang CompatibilityScreen."""
        if not self.selected_game:
            try:
                current_screen = self.root.ids.screen_manager.current
                if current_screen == 'pc_input':
                    screen = self.root.ids.screen_manager.get_screen('pc_input')
                    screen.ids.compatibility_text.text = "Vui lòng chọn một game trước!"
                elif current_screen == 'select_game':
                    screen = self.root.ids.screen_manager.get_screen('select_game')
                    screen.ids.game_name.text = "Vui lòng chọn một game trước!"
                self.root.ids.screen_manager.current = 'select_game'
                return
            except Exception as e:
                print(f"Lỗi khi hiển thị thông báo: {e}")
                return

        self.on_submit_pc_input()  # Lưu cấu hình PC

        try:
            screen = self.root.ids.screen_manager.get_screen('compatibility')
            screen.ids.game_title.text = f"So Sánh Cấu Hình: {self.selected_game.Name}"
            print(f"self.pc_config trước khi chuyển: {self.pc_config}")  # Debug
            game_min=self.selected_game.Minimum
            screen.ids.game_os.text=game_min.OS
            screen.ids.game_cpu.text=game_min.CPU
            screen.ids.game_gpu.text=game_min.GPU
            screen.ids.free.text=game_min.Storage
            screen.ids.game_directx.text=game_min.DirectX
            screen.ids.game_ram.text=game_min.RAM
        except Exception as e:
            print(f"Lỗi khi cập nhật CompatibilityScreen: {e}")
        self.root.ids.screen_manager.current = 'compatibility'
    
if __name__ == '__main__':
    BuildCheckApp().run()
