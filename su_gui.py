import wx
from wx.lib.pubsub import pub   # Inter-frame messaging
import su_ustream_front     # Settings in another file, specifically for uStream
import ustream
import configparser
from streamlink import Streamlink
config = configparser.ConfigParser()
config.read('settings.ini')

broadcaster_title = ['0'] * 15
broadcaster_viewers = ['0'] * 15
broadcaster_url = ['0'] * 15
broadcaster_thumbnail = ['0'] * 15

# broadcaster_title = ['x1', 'awd2', 'x3', 'awd4', 'x5', 'mag6', 'nus7', 'oui8', 'ekg9', 'nus10', 'oui11', 'ekg12']
# broadcaster_viewers = ['9', '82', '9', '82', '9', '123', 'ix', 'oi', 'pho', 'you', 'better', 'work']
# broadcaster_url = ['9', '82', '9', '82', '9', '123', 'ix', 'oi', 'pho', 'you', 'better', 'work']


###########################################################################################################
#   Frame for the Advanced Settings Window
###########################################################################################################
class Advanced(wx.Frame):

    class AdvancedPanel(wx.Panel):
        def __init__(self, parent):
            wx.Panel.__init__(self, parent, size=(300, 500))
            self.colour_control()
            ###########################################################################################################
            temp_txt1 = wx.StaticText(self, -1, "")
            temp_txt2 = wx.StaticText(self, -1, "")
            temp_txt3 = wx.StaticText(self, -1, "")
            self.dark_mode_txt = wx.StaticText(self, -1, "Dark Mode", style=wx.ALIGN_CENTER_VERTICAL)
            self.dark_mode_checkb = wx.CheckBox(self, label='Enable')
            self.dark_mode_checkb.Bind(wx.EVT_CHECKBOX, self.dark_mode)
            self.dark_mode_checkb.SetValue(config.getboolean('dark_mode', 'Status'))
            ###########################################################################################################
            box = wx.BoxSizer(wx.VERTICAL)
            box2 = wx.BoxSizer(wx.HORIZONTAL)
            box.Add(box2, 1, wx.EXPAND)
            box2.Add(temp_txt1, 20)
            box2.Add(self.dark_mode_txt, 40)
            box2.Add(self.dark_mode_checkb, 20)
            box2.Add(temp_txt2, 20)
            ###########################################################################################################
            self.SetSizer(box)
            self.Layout()
            ###########################################################################################################

        def dark_mode(self, event):
            if self.dark_mode_checkb.GetValue():
                config.set('dark_mode', 'Status', 'On')
                self.dark_mode_checkb.SetValue(True)
                pub.sendMessage('dark_mode', message='On', listener='dark_mode')
            else:
                config.set('dark_mode', 'Status', 'Off')
                self.dark_mode_checkb.SetValue(False)
                pub.sendMessage('dark_mode', message='Off', istener='dark_mode')
            with open('settings.ini', 'w') as configfile:
                config.write(configfile)
            self.colour_control()

        def colour_control(self):
            if config.get('dark_mode', 'Status') == 'On':
                self.SetBackgroundColour(config.get('dark_mode_colours', 'menu'))
            else:
                self.SetBackgroundColour(config.get('light_mode_colours', 'menu'))
            self.Refresh()

    def __init__(self):
        wx.Frame.__init__(self, None, -1, title='Advanced Settings', size=(300, 200),
                          style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)
        ###########################################################################################################
        self.pnl = Advanced.AdvancedPanel(self)
        ###########################################################################################################
        self.SetAutoLayout(True)
        self.Layout()
        self.Show()
        self.Centre(wx.BOTH)
        ###########################################################################################################


###########################################################################################################
#   Frame for the opening dialogue window asking for a service to select
###########################################################################################################
class Window(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, -1, title='Service Select', size=(400, 150),
                          style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)
        self.pnl = wx.Panel(self, -1)   # For this frame, there is no need for a complicated panel
        ###########################################################################################################
        service = ['uStream', 'More...']    # 'More...' being a place holder and *future* redirect
        self.service_choice = wx.Choice(self.pnl, choices=service, pos=(15, 40), size=(352, 25))
        self.service_choice.SetSelection(-1)
        ###########################################################################################################
        select_instr = "Select the streaming service to access"
        wx.StaticText(self.pnl, label=select_instr, pos=(15, 18))
        ###########################################################################################################
        exit_button = wx.Button(self.pnl, label='Exit', pos=(15, 75))  # x=horizontal, y=vertical
        exit_button.Bind(wx.EVT_BUTTON, self.exit)
        ###########################################################################################################
        ok_button = wx.Button(self.pnl, label='OK', pos=(280, 75))
        ok_button.Bind(wx.EVT_BUTTON, self.open_select)
        ###########################################################################################################
        self.Centre()
        self.Show(True)
        ###########################################################################################################

    def exit(self, b):
        self.Close(True)
        ###########################################################################################################

    def open_select(self, event):
        selected_service = self.service_choice.GetStringSelection()
        #pub.sendMessage('ok', message=selected_service, listener='ok')
        if self.service_choice.GetStringSelection() == "uStream":
            self.Close()
            frame = InterfaceWindow()
            frame.Show()
        elif self.service_choice.GetStringSelection() == "More...":
            wx.MessageBox('Coming Soon!', 'More...', wx.OK | wx.ICON_INFORMATION)
            ###########################################################################################################


###########################################################################################################
#   Frame for the 'main' interface
###########################################################################################################
class InterfaceWindow(wx.Frame):

    class InterfaceTop(wx.Panel):
        def __init__(self, parent):
            wx.Panel.__init__(self, parent, size=(1280, 100))
            self.SetBackgroundColour('#241773')
            ###########################################################################################################
            self.search_site = wx.SearchCtrl(self, -1, style=wx.TE_PROCESS_ENTER, name='Search for broadcaster')
            self.search_site.ShowCancelButton(True)
            self.image_maybe2 = wx.StaticText(self, -1, "")
            ###########################################################################################################
            if 1 == 1:  # ToDo Get the listener running! Replace this with a correct modular approach
                self.init_ustream()
            ###########################################################################################################
            xlobox = wx.BoxSizer(wx.HORIZONTAL)
            xlobox.Add(self.png, 19, wx.ALIGN_CENTER)
            xlobox.Add(self.search_site, 50, wx.ALIGN_CENTER)
            xlobox.Add(self.image_maybe2, 10, wx.EXPAND + wx.CENTER)
            ###########################################################################################################
            self.SetSizer(xlobox)
            self.Layout()
            ###########################################################################################################

        def init_ustream(self):
            if 1 == 1:
                self.png = wx.StaticBitmap(self, -1,
                                           wx.Bitmap(su_ustream_front.TopBar.uStream_logo, wx.BITMAP_TYPE_ANY))
            ###########################################################################################################

    class InterfaceSide(wx.Panel):

        def __init__(self, parent):
            wx.Panel.__init__(self, parent, size=(200, 668))
            ###########################################################################################################
            pub.subscribe(self.dark_mode, 'dark_mode')
            ###########################################################################################################
            self.menu_tree = wx.TreeCtrl(self, wx.ID_ANY, style=wx.TR_NO_LINES | wx.TR_HAS_BUTTONS)
            self.menu_tree.SetBackgroundColour('#999999')
            self.menu_tree.SetWindowStyleFlag(wx.NO_BORDER + wx.TR_HIDE_ROOT)
            self.menu_root = self.menu_tree.AddRoot('I should be hidden')
            ###########################################################################################################
            self.colour_control()
            ###########################################################################################################
            self.browse_sub_root = self.menu_tree.AppendItem(self.menu_root, 'Browse')
            for i, text in enumerate(su_ustream_front.SideBar.Browse):
                self.menu_tree.AppendItem(self.browse_sub_root, text)
            ###########################################################################################################
            self.log_in_sub_root = self.menu_tree.AppendItem(self.menu_root, 'Log-in')
            for i, text in enumerate(su_ustream_front.SideBar.Log_in):
                self.menu_tree.AppendItem(self.log_in_sub_root, text)
            ###########################################################################################################
            self.options_sub_root = self.menu_tree.AppendItem(self.menu_root, 'Options')
            for i, text in enumerate(su_ustream_front.SideBar.Options):
                self.menu_tree.AppendItem(self.options_sub_root, text)
            ###########################################################################################################
            self.menu_tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.open_advanced)
            self.menu_tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.open_browse)
            ###########################################################################################################
            self.change_p_button = wx.Button(self, label='Change Platform')
            self.change_p_button.Bind(wx.EVT_BUTTON, self.return_service_select)
            ###########################################################################################################
            xdbox = wx.BoxSizer(wx.VERTICAL)
            xdbox.Add(self.menu_tree, 15, wx.EXPAND)
            xdbox.Add(self.change_p_button, 1, wx.ALIGN_CENTER)
            self.SetSizer(xdbox)
            self.Layout()
            ###########################################################################################################

        def return_service_select(self, event):
            frame = Window()
            frame.Show()
            InterfaceWindow.close_window(self.Parent)

        def open_browse(self, event):
            if self.menu_tree.GetItemText(event.GetItem()) == su_ustream_front.SideBar.Browse[1]:
                pub.sendMessage("set_browse_all", message='set_browse_all')

        def open_advanced(self, event):
            if self.menu_tree.GetItemText(event.GetItem()) == su_ustream_front.SideBar.Options[2]:
                #   Check to see if the user clicks 'advanced' and if they do, open a new frame
                frame = Advanced()
                frame.Show()

        def dark_mode(self, message):
            self.colour_control()

        def colour_control(self):
            if config.get('dark_mode', 'Status') == 'On':
                self.SetBackgroundColour(config.get('dark_mode_colours', 'side'))
                self.menu_tree.SetBackgroundColour(config.get('dark_mode_colours', 'side'))
                self.Refresh()
            else:
                self.SetBackgroundColour(config.get('light_mode_colours', 'side'))
                self.menu_tree.SetBackgroundColour(config.get('light_mode_colours', 'side'))
                self.Refresh()

    class InterfaceMain(wx.Panel):
        def __init__(self, parent):
            wx.Panel.__init__(self, parent, size=(1080, 668))
            self.colour_control()
            ###########################################################################################################
            self.broadcaster_data_length = len(broadcaster_title)
            self.broadcaster_index = 0
            ###########################################################################################################
            pub.subscribe(self.dark_mode, 'dark_mode')
            pub.subscribe(self.setup_browse_all, 'set_browse_all')
            ###########################################################################################################
            ###########################################################################################################
            self.bs = wx.BoxSizer(wx.VERTICAL)
            self.bs2 = wx.BoxSizer(wx.HORIZONTAL)
            self.gs = wx.GridSizer(2, 3, 5, 5)
            self.SetSizer(self.bs)
            self.gs.Layout()
            ###########################################################################################################
            # self.set_browse_all()

        def setup_browse_all(self, message):
            self.init_browse_all()
            self.set_browse_all()

        def init_browse_all(self):
            global broadcaster_title, broadcaster_viewers, broadcaster_url, broadcaster_thumbnail
            broadcaster_title, broadcaster_viewers, broadcaster_url, broadcaster_thumbnail = \
                ustream.BrowseAll.get_info()
            self.bs.Add(self.gs, wx.EXPAND)

            self.first_button = wx.Button(self, label='First Page', size=(123, 33))
            self.bs2.Add(self.first_button, 1, wx.ALIGN_BOTTOM + wx.ALIGN_LEFT)
            self.first_button.Bind(wx.EVT_BUTTON, self.previous_page)

            self.spacer = wx.StaticText(self, -1, "")
            self.bs2.Add(self.spacer, 10, wx.EXPAND + wx.CENTER)

            self.next_button = wx.Button(self, label='Next Page', size=(123, 33))
            self.bs2.Add(self.next_button, 1, wx.ALIGN_BOTTOM + wx.ALIGN_RIGHT)
            self.next_button.Bind(wx.EVT_BUTTON, self.next_page)

            self.bs.Add(self.bs2, wx.EXPAND)
            self.SetSizer(self.bs)

        def set_browse_all(self):
            global broadcaster_title, broadcaster_viewers, broadcaster_url, broadcaster_thumbnail
            # print(broadcaster_title[0])
            # print(broadcaster_viewers[0])
            # print(broadcaster_url[0])
            # print(self.broadcaster_data_length)
            min_a = 0
            max_a = 6
            for i in range(min_a, max_a):
                if self.broadcaster_index >= self.broadcaster_data_length:
                    1==1
                    # This 'code' runs when there is nothing else to display. Iterator (i) should always run until 5.
                else:
                    self.gs.Add(self.BroadcastContainer(self))
                    self.broadcaster_index = self.broadcaster_index + 1
            #print(self.iterator)
            self.Layout()

        def get_index(self):
            print(self.broadcaster_index)
            return self.broadcaster_index

        def next_page(self, event):
            if self.broadcaster_index != self.broadcaster_data_length:
                pub.sendMessage("clear_container", message='clear_container')
                self.SetSizer(self.bs)
                self.Layout()
                self.set_browse_all()

        def previous_page(self, event):
            if self.broadcaster_index > 6:
                pub.sendMessage("clear_container", message='clear_container')
                self.broadcaster_index = self.broadcaster_index - self.broadcaster_index
                self.SetSizer(self.bs)
                self.Layout()
                self.set_browse_all()

        class BroadcastContainer(wx.Panel):
            def __init__(self, parent):
                wx.Panel.__init__(self, parent, size=(353, 297))
                global broadcaster_title, broadcaster_viewers, broadcaster_url, broadcaster_thumbnail
                pub.subscribe(self.clear_container, 'clear_container')
                self.bs = wx.BoxSizer(wx.VERTICAL)
                #self.bs.Add(wx.StaticText(self, -1, "title"))
                self.bs.Add(wx.StaticText
                            (self, -1, broadcaster_title[InterfaceWindow.InterfaceMain.get_index(parent)])), wx.EXPAND
                self.thumbnail = wx.Image("thumbnail.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
                self.thumbnail_sb = wx.StaticBitmap(self, -1, self.thumbnail)
                self.thumbnail_sb.Bind(wx.EVT_LEFT_DOWN, self.on_click)
                self.bs.Add(self.thumbnail_sb)
                # ^Temporary thumbnail implementation
                # Note: ctrl+/ to comment blocks of code out
                # ToDo: Find another way of displaying thumbnails, as the PIL + convert method is impossible
                #self.bs.Add(wx.StaticText(self, -1, "viewers"))
                self.bs.Add(wx.StaticText
                            (self, -1, broadcaster_viewers[InterfaceWindow.InterfaceMain.get_index(parent)])), wx.EXPAND
                self.SetSizer(self.bs)
                self.Layout()

            def on_click(self, event):
                print(broadcaster_url[0])

            def clear_container(self, message):
                self.Destroy()

        def dark_mode(self, message):
            self.colour_control()

        def colour_control(self):
            if config.get('dark_mode', 'Status') == 'On':
                self.SetBackgroundColour(config.get('dark_mode_colours', 'main'))
                self.Refresh()
            else:
                self.SetBackgroundColour(config.get('light_mode_colours', 'main'))
                self.Refresh()

    def __init__(self):
        wx.Frame.__init__(self, None, title='Streamlink/uStream GUI', size=(1280, 768),
                          style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)
        ###########################################################################################################
        self.panel1 = InterfaceWindow.InterfaceTop(self)
        self.panel2 = InterfaceWindow.InterfaceSide(self)
        self.panel3 = InterfaceWindow.InterfaceMain(self)
        ###########################################################################################################
        #pub.subscribe(self.service_listener, 'ok')
        ###########################################################################################################
        box = wx.BoxSizer(wx.VERTICAL)
        box2 = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(self.panel1, 1, wx.EXPAND)
        box.Add(box2, 1, wx.EXPAND)
        box2.Add(self.panel2, 1, wx.EXPAND)
        box2.Add(self.panel3, 1, wx.EXPAND)
        ###########################################################################################################
        self.SetAutoLayout(True)
        self.SetSizer(box)
        self.Layout()
        self.Show()
        self.Centre(wx.BOTH)
        ###########################################################################################################

    def close_window(self):
        self.Destroy()

    #def service_listener(self, message):
        # Below is unreachable...?
        # Testing revealed the listener works, however
        #self.SetLabel(message)


def main_serv_select():
    app = wx.App(False)
    Window()
    app.MainLoop()


if __name__ == '__main__':
    main_serv_select()
