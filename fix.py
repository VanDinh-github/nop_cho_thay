from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import StringProperty


class MyWidget(BoxLayout):
    my_text = StringProperty("Chà có ncạnvnàvâf o bạn!")

    def __init__(self, **kwargs):
        super(MyWidget, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 10

        # Label ban đầu, để text rỗng vì sẽ được cập nhật qua bind
        self.label = Label(font_size=24)
        self.add_widget(self.label)

        # Button
        self.button = Button(text="Nhấn để thay đổi", font_size=20)
        self.button.bind(on_press=self.change_text)
        self.add_widget(self.button)

        # Ràng buộc để cập nhật label mỗi khi my_text thay đổi
        self.bind(my_text=self.update_label)

        # Gán giá trị ban đầu cho label
        self.update_label(self, self.my_text)

    def change_text(self, instance):
        self.my_text = "Bạn vừa nhấn nút!"

    def update_label(self, instance, value):
        self.label.text = value


class MyApp(App):
    def build(self):
        return MyWidget()


if __name__ == '__main__':
    MyApp().run()
