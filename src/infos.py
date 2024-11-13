import wx
import subprocess
from PIL import Image
import webbrowser

class infoWindow(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(infoWindow, self).__init__(None, style=wx.CAPTION | wx.CLOSE_BOX)

        self.SetTitle("LinkTree (v6) - Informations")
        icon = wx.Icon("../assets/linktree_v6.ico", wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)
        self.SetSize((400, 300))
        self.Center()

        # Main panel
        panel = wx.Panel(self)

        # Load and resize image
        image_path = "../assets/infos_banner.png"
        img = Image.open(image_path)
        img = img.resize((50, self.GetSize()[1] - 40), Image.Resampling.LANCZOS)
        img = wx.Bitmap.FromBufferRGBA(img.size[0], img.size[1], img.convert("RGBA").tobytes())

        bitmap = wx.StaticBitmap(panel, bitmap=img)

        # Text content
        text = wx.StaticText(panel, label=(
            "LinkTree, dans sa sixième version, vous permet "
            "toujours de gagner du temps à l'ouverture de votre "
            "navigateur Internet.\n\n"
            "Appuyez sur A et Z pour aller à la page suivante ou "
            "précédente.\n\n"
            "Dans le menu \"Modifier\", vous pouvez changer \nles boutons "
            "et/ou leur configuration."
            "\nSouvenez-vous de ne placer qu'un seul lien par ligne !!!\n\n"
            "(c) Louis Damay, 2024"
        ))
        text.Wrap(300)

        GitHubBtn = wx.Button(panel, label="GitHub", size=(80, 30))
        GitHubBtn.Bind(wx.EVT_BUTTON, self.OnGitHubClick)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(bitmap, 0, wx.ALL | wx.EXPAND, 5)

        text_sizer = wx.BoxSizer(wx.VERTICAL)
        text_sizer.Add(text, 1, wx.ALL | wx.EXPAND, 10)
        text_sizer.Add(GitHubBtn, 0, wx.ALL | wx.CENTER, 10)

        sizer.Add(text_sizer, 1, wx.EXPAND)
        panel.SetSizer(sizer)

        self.Bind(wx.EVT_CLOSE, self.OnClose)

    def OnGitHubClick(self, event):
        webbrowser.open("https://github.com/LouisDamay/LinkTree-v6")  # Replace with your GitHub URL

    def OnClose(self, event):
        subprocess.Popen(["python", "main.py"])
        self.Destroy()

if __name__ == "__main__":
    app = wx.App(False)
    frame = infoWindow(None)
    frame.Show()
    app.MainLoop()
