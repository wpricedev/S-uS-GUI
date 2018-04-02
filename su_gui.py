import wx


class Window(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, -1, title='Service Select', size=(400, 150),
                          style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)
        pnl = wx.Panel(self, -1)

        service = ['uStream', 'More...']
        self.service_choice = wx.Choice(pnl, choices=service, pos=(15, 40), size=(352, 25))

        self.service_choice.SetSelection(-1)

        select_instr = "Select the streaming service to access"
        wx.StaticText(pnl, label=select_instr, pos=(15, 18))

        exit_button = wx.Button(pnl, label='Exit', pos=(15, 75))  # x=horizontal, y=vertical
        exit_button.Bind(wx.EVT_BUTTON, self.exit)

        ok_button = wx.Button(pnl, label='OK', pos=(280, 75))
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

    def __init__(self):
        wx.Frame.__init__(self, None, title="Streamlink/uStream GUI")


def main_serv_select():
    app = wx.App(False)
    Window()
    app.MainLoop()


if __name__ == '__main__':
    main_serv_select()