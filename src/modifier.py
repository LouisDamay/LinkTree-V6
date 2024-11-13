import wx
import pickle
import subprocess

# Charger les données depuis le fichier binaire
with open('../assets/all_labels.bin', 'rb') as file:
    all_labels = pickle.load(file)
class EditWindow(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(EditWindow, self).__init__(None, style=wx.CAPTION | wx.CLOSE_BOX)
        self.SetTitle("LinkTree (v6) - Modifier")
        self.SetSize((500, 500))
        self.Center()

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Champ pour le numéro de collection
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        lbl_collection = wx.StaticText(panel, label="Numéro de la collection:")
        hbox1.Add(lbl_collection, flag=wx.RIGHT, border=8)
        self.txt_collection = wx.TextCtrl(panel)
        hbox1.Add(self.txt_collection, proportion=1)

        # Bouton "Charger" pour charger les données
        btn_load = wx.Button(panel, label="Charger")
        btn_load.Bind(wx.EVT_BUTTON, self.OnLoadCollection)
        hbox1.Add(btn_load, flag=wx.LEFT, border=10)

        # Bouton "Créer une nouvelle collection"
        btn_new_collection = wx.Button(panel, label="Créer une nouvelle collection")
        btn_new_collection.Bind(wx.EVT_BUTTON, self.OnCreateNewCollection)
        hbox1.Add(btn_new_collection, flag=wx.LEFT, border=10)

        vbox.Add(hbox1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        # Liste déroulante pour choisir une clé
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        lbl_key = wx.StaticText(panel, label="Clé à modifier:")
        hbox2.Add(lbl_key, flag=wx.RIGHT, border=8)
        self.choice_key = wx.Choice(panel, choices=[])
        self.choice_key.Bind(wx.EVT_CHOICE, self.OnKeyChange)
        hbox2.Add(self.choice_key, proportion=1)
        vbox.Add(hbox2, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        # Champ pour renommer la clé
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        lbl_new_key = wx.StaticText(panel, label="Nouveau nom de la clé:")
        hbox3.Add(lbl_new_key, flag=wx.RIGHT, border=8)
        self.txt_new_key = wx.TextCtrl(panel)
        hbox3.Add(self.txt_new_key, proportion=1)
        vbox.Add(hbox3, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        # Liste des liens (modifiable)
        hbox4 = wx.BoxSizer(wx.VERTICAL)
        lbl_links = wx.StaticText(panel, label="Liens:")
        hbox4.Add(lbl_links, flag=wx.BOTTOM, border=5)
        self.txt_links = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
        hbox4.Add(self.txt_links, proportion=1, flag=wx.EXPAND)
        vbox.Add(hbox4, proportion=1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        # Boutons Sauvegarder et Retour
        hbox5 = wx.BoxSizer(wx.HORIZONTAL)
        btn_save = wx.Button(panel, label="Sauvegarder")
        btn_save.Bind(wx.EVT_BUTTON, self.OnSave)
        hbox5.Add(btn_save, flag=wx.RIGHT, border=10)

        btn_back = wx.Button(panel, label="Retour")
        btn_back.Bind(wx.EVT_BUTTON, self.OnBack)
        hbox5.Add(btn_back)
        vbox.Add(hbox5, flag=wx.ALIGN_RIGHT | wx.RIGHT | wx.BOTTOM, border=10)

        panel.SetSizer(vbox)

    def OnCreateNewCollection(self, event):
        """Crée une nouvelle collection remplie de placeholders numérotés de 1 à 12."""
        try:
            # Créer une nouvelle collection avec des clés "Placeholder X" et des valeurs vides (listes)
            new_collection = [{f"Placeholder {i}": []} for i in range(1, 13)]
            
            # Ajouter cette nouvelle collection à all_labels
            all_labels.append(new_collection)

            # Sauvegarder la mise à jour dans le fichier binaire
            with open('../assets/all_labels.bin', 'wb') as file:
                pickle.dump(all_labels, file)

            # Afficher un message de confirmation et mettre à jour le champ collection
            wx.MessageBox("Nouvelle collection créée avec des placeholders 1 à 12.", "Succès", wx.ICON_INFORMATION)
            self.txt_collection.SetValue(str(len(all_labels)))  # Affiche le numéro de la nouvelle collection

        except Exception as e:
            wx.MessageBox(f"Erreur lors de la création de la nouvelle collection : {str(e)}", "Erreur", wx.ICON_ERROR)


    def OnLoadCollection(self, event):
        """Charge les clés et les données pour le numéro de collection saisi."""
        try:
            collection_num = int(self.txt_collection.GetValue()) - 1
            if collection_num < 0 or collection_num >= len(all_labels):
                wx.MessageBox("Numéro de collection invalide.", "Erreur", wx.ICON_ERROR)
                return

            # Récupérer toutes les clés présentes dans les dictionnaires de la collection
            collection = all_labels[collection_num]
            all_keys_in_collection = set()
            for item in collection:
                all_keys_in_collection.update(item.keys())

            combined_keys = sorted(all_keys_in_collection)
            self.choice_key.SetItems(combined_keys)
            if combined_keys:
                self.choice_key.SetSelection(0)  # Sélectionner la première clé par défaut
                self.LoadLinks(self.choice_key.GetStringSelection())
            else:
                wx.MessageBox("Aucune clé disponible.", "Info", wx.ICON_INFORMATION)

        except ValueError:
            wx.MessageBox("Veuillez entrer un numéro de collection valide.", "Erreur", wx.ICON_ERROR)

    def OnKeyChange(self, event):
        """Recharge les liens pour la clé sélectionnée."""
        selected_key = self.choice_key.GetStringSelection()
        self.txt_new_key.SetValue(selected_key)  # Remplir le champ pour renommer
        self.LoadLinks(selected_key)

    def LoadLinks(self, selected_key):
        """Charge les liens pour la clé sélectionnée."""
        try:
            collection_num = int(self.txt_collection.GetValue()) - 1
            collection = all_labels[collection_num]

            for item in collection:
                if selected_key in item:
                    links = item[selected_key]
                    self.txt_links.SetValue("\n".join(links))
                    return  # Clé trouvée, on charge les liens et quitte la fonction

            # Si la clé n'existe pas encore dans cette collection
            self.txt_links.SetValue("")

        except (ValueError, IndexError):
            wx.MessageBox("Erreur lors du chargement des liens.", "Erreur", wx.ICON_ERROR)

    def OnSave(self, event):
        """Sauvegarde les modifications dans le fichier binaire."""
        try:
            collection_num = int(self.txt_collection.GetValue()) - 1
            if collection_num < 0 or collection_num >= len(all_labels):
                wx.MessageBox("Numéro de collection invalide.", "Erreur", wx.ICON_ERROR)
                return

            selected_key = self.choice_key.GetStringSelection()
            new_key_name = self.txt_new_key.GetValue().strip()

            if not new_key_name:
                wx.MessageBox("Le nouveau nom de la clé ne peut pas être vide.", "Erreur", wx.ICON_ERROR)
                return

            new_links = self.txt_links.GetValue().strip().split("\n")

            # Sauvegarde des changements
            collection = all_labels[collection_num]

            # Modifier le nom de la clé ou en ajouter une nouvelle
            for item in collection:
                if selected_key in item:
                    del item[selected_key]
                    item[new_key_name] = new_links
                    break
            else:
                # Si la clé n'existait pas encore
                collection.append({new_key_name: new_links})

            # Sauvegarder dans le fichier binaire
            with open('../assets/all_labels.bin', 'wb') as file:
                pickle.dump(all_labels, file)

            wx.MessageBox("Modifications sauvegardées.", "Succès", wx.ICON_INFORMATION)

        except Exception as e:
            wx.MessageBox(f"Erreur : {str(e)}", "Erreur", wx.ICON_ERROR)

    def OnBack(self, event):
        """Retourne à l'écran principal."""
        subprocess.Popen(["python", "main.py"])
        self.Close()

if __name__ == "__main__":
    app = wx.App(False)
    frame = EditWindow(None)
    frame.Show()
    app.MainLoop()
