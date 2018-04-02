import wx


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
            frame = UStream()
            frame.Show()
        elif self.service_choice.GetStringSelection() == "More...":
            wx.MessageBox('Coming Soon!', 'More...', wx.OK | wx.ICON_INFORMATION)


class UStream(wx.Frame):

    class UStreamTop(wx.Panel):
        def __init__(self, parent):
            wx.Panel.__init__(self, parent, size=(1280, 100))
            self.SetBackgroundColour('#241773')

    class UStreamSide(wx.Panel):
        def __init__(self, parent):
            wx.Panel.__init__(self, parent, size=(300, 668))
            self.SetBackgroundColour('#999999')
            change_p_button = wx.Button(self, label='Change Platform', pos=(85, 580))
            change_p_button.Bind(wx.EVT_BUTTON, self.return_service_select)

        def return_service_select(self, event):
            frame = Window()
            frame.Show()

    class UStreamMain(wx.Panel):
        def __init__(self, parent):
            wx.Panel.__init__(self, parent, size=(980, 668))
            self.SetBackgroundColour('#FFFFFF')

    def __init__(self):
        wx.Frame.__init__(self, None, title='Streamlink/uStream GUI', size=(1280, 768),
                          style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)

        panel1 = UStream.UStreamTop(self)
        panel2 = UStream.UStreamSide(self)
        panel3 = UStream.UStreamMain(self)

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
