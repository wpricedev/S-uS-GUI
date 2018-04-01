import wx
import ustream


class Window(wx.Frame):

    def __init__(self, *args, **kw):
        super(Window, self).__init__(*args, **kw)
        self.init_ui()

    def init_ui(self):
        pnl = wx.Panel(self)
        select_instr = "Select the streaming service to access"
        wx.StaticText(pnl, label=select_instr, pos=(15, 18))

        exit_cbtn = wx.Button(pnl, label='Exit', pos=(15, 75)) # x=horizontal, y=vertical
        exit_cbtn.Bind(wx.EVT_BUTTON, self.exit)

        ok_ctbn = wx.Button(pnl, label='OK', pos=(280, 75))
        #ok_ctbn.Bind(wx.EVT_BUTTON, self.open_select)

        service = ['uStream', 'More...', '                                                                                                            ']
        service_cb = wx.ComboBox(pnl, pos=(15, 40), choices=service, style=wx.CB_READONLY)

        self.SetSize((400, 150))
        self.SetTitle('Select Service')
        self.Centre()
        self.Show(True)

    def exit(self, a):
        self.Close(True)

    #def open_select(self, b):
        #frame.Show()


def main_serv_select():
    app = wx.App(False)
    Window(None)
    app.MainLoop()


if __name__ == '__main__':
    main_serv_select()