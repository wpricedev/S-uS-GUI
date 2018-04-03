import wx
import su_ustream_front


class Window(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, -1, title='Service Select', size=(400, 150),
                          style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)
        self.pnl = wx.Panel(self, -1)

        service = ['uStream', 'More...']
        self.service_choice = wx.Choice(self.pnl, choices=service, pos=(15, 40), size=(352, 25))
        self.service_choice.SetSelection(-1)

        select_instr = "Select the streaming service to access"
        wx.StaticText(self.pnl, label=select_instr, pos=(15, 18))

        exit_button = wx.Button(self.pnl, label='Exit', pos=(15, 75))  # x=horizontal, y=vertical
        exit_button.Bind(wx.EVT_BUTTON, self.exit)

        ok_button = wx.Button(self.pnl, label='OK', pos=(280, 75))
        ok_button.Bind(wx.EVT_BUTTON, self.open_select)

        self.Centre()
        self.Show(True)

    def exit(self, b):
        self.Close(True)

    def open_select(self, event):
        if self.service_choice.GetStringSelection() == "uStream":
            self.Destroy()
            frame = InterfaceWindow()
            frame.Show()
        elif self.service_choice.GetStringSelection() == "More...":
            wx.MessageBox('Coming Soon!', 'More...', wx.OK | wx.ICON_INFORMATION)


class InterfaceWindow(wx.Frame):

    class InterfaceTop(wx.Panel):
        def __init__(self, parent):
            wx.Panel.__init__(self, parent, size=(1280, 100))
            self.SetBackgroundColour('#241773')

            self.search_site = wx.SearchCtrl(self, -1, style=wx.TE_PROCESS_ENTER, name='Search for broadcaster')
            self.search_site.ShowCancelButton(True)
            self.image_maybe = wx.StaticText(self, -1, "")
            self.image_maybe2 = wx.StaticText(self, -1, "")

            self.png = wx.StaticBitmap(self, -1, wx.Bitmap("uStream_logo.png", wx.BITMAP_TYPE_ANY))

            xlobox = wx.BoxSizer(wx.HORIZONTAL)
            xlobox.Add(self.png, 19, wx.ALIGN_CENTER)
            xlobox.Add(self.search_site, 50, wx.ALIGN_CENTER)
            xlobox.Add(self.image_maybe2, 10, wx.EXPAND + wx.CENTER)
            self.SetSizer(xlobox)
            self.Layout()

    class InterfaceSide(wx.Panel):

        def __init__(self, parent):
            wx.Panel.__init__(self, parent, size=(200, 668))
            self.SetBackgroundColour('#999999')
            large_font = wx.Font(16, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Verdana')
            small_font = wx.Font(10, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Verdana')
            ###########################################################################################################
            self.menu_tree = wx.TreeCtrl(self, wx.ID_ANY, style=wx.TR_NO_LINES | wx.TR_HAS_BUTTONS)
            self.menu_tree.SetBackgroundColour('#999999')
            self.menu_tree.SetWindowStyleFlag(wx.NO_BORDER + wx.TR_HIDE_ROOT)
            self.menu_root = self.menu_tree.AddRoot('I should be hidden')
            ###########################################################################################################
            self.browse_sub_root = self.menu_tree.AppendItem(self.menu_root, 'Browse')
            #self.menu_tree.SetItemFont(self.browse_sub_root, small_font)
            for i, text in enumerate(su_ustream_front.SideBar.Browse):
                self.menu_tree.AppendItem(self.browse_sub_root, text)
            ###########################################################################################################
            self.log_in_sub_root = self.menu_tree.AppendItem(self.menu_root, 'Log-in')
            #self.menu_tree.SetItemFont(self.log_in_sub_root, small_font)
            for i, text in enumerate(su_ustream_front.SideBar.Log_in):
                self.menu_tree.AppendItem(self.log_in_sub_root, text)

            ###########################################################################################################
            self.options_sub_root = self.menu_tree.AppendItem(self.menu_root, 'Options')
            #self.menu_tree.SetItemFont(self.options_sub_root, small_font)
            for i, text in enumerate(su_ustream_front.SideBar.Options):
                self.menu_tree.AppendItem(self.options_sub_root, text)
            ###########################################################################################################
            self.change_p_button = wx.Button(self, label='Change Platform')
            self.change_p_button.Bind(wx.EVT_BUTTON, self.return_service_select)
            ###########################################################################################################

            ###########################################################################################################
            xdbox = wx.BoxSizer(wx.VERTICAL)
            xdbox.Add(self.menu_tree, 15, wx.EXPAND)
            xdbox.Add(self.change_p_button, 1, wx.ALIGN_CENTER)
            self.SetSizer(xdbox)
            self.Layout()

        def return_service_select(self, event):
            frame = Window()
            frame.Show()

        #def write_text(self):

    class InterfaceMain(wx.Panel):
        def __init__(self, parent):
            wx.Panel.__init__(self, parent, size=(1080, 668))
            self.SetBackgroundColour('#FFFFFF')

    def __init__(self):
        wx.Frame.__init__(self, None, title='Streamlink/uStream GUI', size=(1280, 768),
                          style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)

        panel1 = InterfaceWindow.InterfaceTop(self)
        panel2 = InterfaceWindow.InterfaceSide(self)
        panel3 = InterfaceWindow.InterfaceMain(self)

        box = wx.BoxSizer(wx.VERTICAL)
        box2 = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(panel1, 1, wx.EXPAND)
        box.Add(box2, 1, wx.EXPAND)
        box2.Add(panel2, 1, wx.EXPAND)
        box2.Add(panel3, 1, wx.EXPAND)

        self.SetAutoLayout(True)
        self.SetSizer(box)
        self.Layout()
        self.Show()
        self.Centre(wx.BOTH)


def main_serv_select():
    app = wx.App(False)
    Window()
    app.MainLoop()


if __name__ == '__main__':
    main_serv_select()
