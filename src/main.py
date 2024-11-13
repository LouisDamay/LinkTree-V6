import wx
import webbrowser
from infos import infoWindow
from modifier import EditWindow
import pickle

with open('../assets/all_labels.bin', 'rb') as file:
    all_labels = pickle.load(file)

class MyFrame(wx.Frame):
    def __init__(self):
        self.optionsView = False
        self.current_index = 0

        style = wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX)
        super().__init__(parent=None, title=('LinkTree v6 (1/'+str(len(all_labels))+')'), size=(484, 205), style=style)

        self.panel = wx.Panel(self)
        self.panel.SetFocus()
        self.panel.Bind(wx.EVT_CHAR_HOOK, self.on_key_down)  

        self.panel.Bind(wx.EVT_LEFT_DCLICK, self.on_double_click)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)

        self.create_button_grid(all_labels[self.current_index])

        self.bottom_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.info_btn = wx.Button(self.panel, label='Infos', size=(80, 30))
        self.modify_btn = wx.Button(self.panel, label='Modifier', size=(80, 30))
        self.Bind(wx.EVT_BUTTON, self.on_info, self.info_btn)
        self.Bind(wx.EVT_BUTTON, self.on_modify, self.modify_btn)

        self.bottom_sizer.Add(self.info_btn, 0, wx.RIGHT, 3)
        self.bottom_sizer.Add(self.modify_btn, 0, wx.LEFT, 3)

        self.main_sizer.Add(self.grid_sizer, 0, wx.ALIGN_CENTER | wx.TOP, 8)
        self.main_sizer.Add(self.bottom_sizer, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        self.panel.SetSizer(self.main_sizer)

        self.bottom_sizer.ShowItems(False)

        self.Centre()
        icon = wx.Icon("../assets/linktree_v6.ico", wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)

        self.SetSizeHints(464, 192, -1, -1)

        self.Bind(wx.EVT_KEY_DOWN, self.on_key_down)

        self.Show()

    def create_button_grid(self, labels):
        self.grid_sizer = wx.GridSizer(2, 6, 5, 5)

        for label_data in labels:
            for label, urls in label_data.items():
                btn = wx.Button(self.panel, label=label, size=(70, 70))
                self.grid_sizer.Add(btn, 0, wx.EXPAND)
                self.Bind(wx.EVT_BUTTON, lambda evt, urls=urls: self.open_all_urls(urls), btn)

    def update_button_grid(self):
        self.main_sizer.Hide(self.grid_sizer, recursive=True)
        self.main_sizer.Remove(self.grid_sizer) 

        self.create_button_grid(all_labels[self.current_index])

        self.main_sizer.Insert(0, self.grid_sizer, 0, wx.ALIGN_CENTER | wx.TOP, 8)
        
        self.panel.Layout()

    def on_double_click(self, event):
        self.optionsView = not self.optionsView
        if self.optionsView:
            self.SetSize((484, 240))
            self.bottom_sizer.ShowItems(True)
        else:
            self.SetSize((484, 205))
            self.bottom_sizer.ShowItems(False)

        self.panel.Layout()
        event.Skip()

    def open_all_urls(self, urls):
        for url in urls:
            webbrowser.open(url)
        self.Close()

    def on_info(self, event):
        second_window = infoWindow(None, title="Informations")
        second_window.Show()
        self.Close()

    def on_modify(self, event):
        second_window = EditWindow(None, title="Modifier un bouton")
        second_window.Show()
        self.Close()
    
    def on_key_down(self, event):
        keycode = event.GetKeyCode()
        if keycode == ord('A'):  # Touche 'A'
            self.current_index = (self.current_index - 1) % len(all_labels)
            self.SetTitle(
                ('LinkTree v6 (' +
                str(self.current_index + 1) +
                '/' +str(len(all_labels))
                +')')
            )
            self.update_button_grid()
        elif keycode == ord('Z'):  # Touche 'Z'
            self.current_index = (self.current_index + 1) % len(all_labels)
            self.SetTitle(
                ('LinkTree v6 (' +
                str(self.current_index + 1) +
                '/' +str(len(all_labels))
                +')')
            )
            self.update_button_grid()
        else:
            event.Skip()


if __name__ == '__main__':
    error = False

    # On commence par vérifier que le tableau contenant les dictionnaires est
    for labels in all_labels:
        if len(labels) != 12:
            error = True
            break

    if not error:
        app = wx.App(False)
        frame = MyFrame()
        app.MainLoop()
    else:
        print("Erreur dans la configuration du fichier.")
