from kivy.app import App
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
import main


if __name__ == "__main__":
    class ChatBot(App):
        def build(self):
            self.title = 'Chat'
            chat = BoxLayout(orientation='horizontal')
            self.affich = Label(text='', font_size=30)
            chat.add_widget(self.affich)
            entree = BoxLayout(orientation='horizontal')
            self.txt = TextInput(font_size=30, size_hint=(0.7, 0.3))
            entree.add_widget(self.txt)
            self.btn1 = Button(text='Entrer', font_size=30, size_hint=(0.7, 0.3))
            self.btn1.bind(on_press=self.recup)
            entree.add_widget(self.btn1)
            box = BoxLayout(orientation='vertical')
            box.add_widget(chat)
            box.add_widget(entree)
            return box

        def recup(self, btn=None):
            str = self.txt.text
            # self.affich.text += "Commande : " + self.txt.text + "\n"
            return str


    Config.set('graphics', 'width', '350')
    Config.set('graphics', 'height', '50')
    ChatBot().run()
