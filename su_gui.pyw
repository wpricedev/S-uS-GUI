import wx
from wx.lib.pubsub import pub   # Inter-frame messaging
import urllib.request
import su_ustream_front     # Settings in another file, specifically for uStream
import ustream
import configparser
import os
###########################################################################################################
#   WARNING! This application is currently configured for PURELY uStream!
###########################################################################################################
config = configparser.ConfigParser()
config.read('settings.ini')
###########################################################################################################
#   Limited to 20 results per page due to limitation of virtual browser 'scrolling'
###########################################################################################################
broadcaster_title = ['0'] * 20
broadcaster_viewers = ['0'] * 20
broadcaster_url = ['0'] * 20
broadcaster_thumbnail = ['0'] * 20


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
            temp_txt4 = wx.StaticText(self, -1, "")
            ###########################################################################################################
            quality_choices = ['Best', '720p', '480p', 'Worst']
            ###########################################################################################################
            self.dark_mode_txt = wx.StaticText(self, -1, "Dark Mode", style=wx.ALIGN_CENTER_VERTICAL)
            self.dark_mode_checkb = wx.CheckBox(self, label='Enable')
            self.dark_mode_checkb.Bind(wx.EVT_CHECKBOX, self.dark_mode)
            self.dark_mode_checkb.SetValue(config.getboolean('dark_mode', 'Status'))
            ###########################################################################################################
            self.quality_text = wx.StaticText(self, -1, "Video Quality", style=wx.ALIGN_CENTER_VERTICAL)
            self.quality_choice = wx.Choice(self, choices=quality_choices)
            self.quality_choice.Bind(wx.EVT_CHOICE, self.update_quality)
            self.quality_choice.SetSelection(-1)
            ###########################################################################################################
            box_sizer_vertical_1 = wx.BoxSizer(wx.VERTICAL)
            box_sizer_horizontal_1 = wx.BoxSizer(wx.HORIZONTAL)
            box_sizer_horizontal_2 = wx.BoxSizer(wx.HORIZONTAL)
            box_sizer_vertical_1.Add(box_sizer_horizontal_1, 1, wx.EXPAND)
            box_sizer_vertical_1.Add(box_sizer_horizontal_2, 1, wx.EXPAND)
            ###########################################################################################################
            box_sizer_horizontal_1.Add(temp_txt1, 20)
            box_sizer_horizontal_1.Add(self.dark_mode_txt, 40)
            box_sizer_horizontal_1.Add(self.dark_mode_checkb, 20)
            box_sizer_horizontal_1.Add(temp_txt2, 20)
            ###########################################################################################################
            box_sizer_horizontal_2.Add(temp_txt3, 10)
            box_sizer_horizontal_2.Add(self.quality_text, 20)
            box_sizer_horizontal_2.Add(self.quality_choice, 40)
            box_sizer_horizontal_2.Add(temp_txt4, 5)
            # ToDo: Fix/Redo layout
            ###########################################################################################################
            self.SetSizer(box_sizer_vertical_1)
            box_sizer_vertical_1.Fit(self)
            self.Layout()
            ###########################################################################################################

        def update_quality(self, event):
            ###########################################################################################################
            #   Update selected quality off of user-input value. 'Back-up' qualities are declared for specific qualities
            ###########################################################################################################
            if self.quality_choice.GetStringSelection() == "Best":
                config.set('pref_quality', 'quality', 'best')
            elif self.quality_choice.GetStringSelection() == "Worst":
                config.set('pref_quality', 'quality', 'worst')
            elif self.quality_choice.GetStringSelection() == "720p":
                config.set('pref_quality', 'quality', '720p,480p,best')
            elif self.quality_choice.GetStringSelection() == "480p,worst":
                config.set('pref_quality', 'quality', '720p')
            with open('settings.ini', 'w') as configfile:
                config.write(configfile)

        def dark_mode(self, event):
            ###########################################################################################################
            #   Update dark mode setting & send message to other frames to toggle dark mode
            ###########################################################################################################
            if self.dark_mode_checkb.GetValue():
                config.set('dark_mode', 'Status', 'On')
                self.dark_mode_checkb.SetValue(True)
                pub.sendMessage('dark_mode', message='On')
            else:
                config.set('dark_mode', 'Status', 'Off')
                self.dark_mode_checkb.SetValue(False)
                pub.sendMessage('dark_mode', message='Off')
            with open('settings.ini', 'w') as configfile:
                config.write(configfile)
            self.colour_control()

        def colour_control(self):
            ###########################################################################################################
            #   Get pre-determined colour settings dependent on 'dark mode' setting.
            ###########################################################################################################
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
        wx.Frame.__init__(self, None, -1, title='Public Stream Viewer (Service Select)', size=(400, 150),
                          style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)
        self.pnl = wx.Panel(self, -1)   # For this frame, there is no need for a complicated panel
        ###########################################################################################################
        service = ['uStream', 'More...']    # 'More...' being a place holder and *future* redirect
        self.service_choice = wx.Choice(self.pnl, choices=service, pos=(15, 40), size=(352, 25))
        self.service_choice.SetSelection(0)
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
        ###########################################################################################################
        #   Select the web-service to focus on.
        ###########################################################################################################
        if self.service_choice.GetStringSelection() == "uStream":
            self.Close()
            frame = InterfaceWindow()
            frame.Show()
        elif self.service_choice.GetStringSelection() == "More...":
            wx.MessageBox('Coming Soon!', 'More...', wx.OK | wx.ICON_INFORMATION)


###########################################################################################################
#   Frame for the 'main' interface
###########################################################################################################
class InterfaceWindow(wx.Frame):

    class InterfaceTop(wx.Panel):
        def __init__(self, parent):
            wx.Panel.__init__(self, parent, size=(1280, 100))
            self.SetBackgroundColour('#241773')
            ###########################################################################################################
            #   Above colour code could be used in settings file. However, since this colour is never changing, hard
            #   coding is somewhat acceptable for this implementation.
            ###########################################################################################################
            self.search_site = wx.SearchCtrl(self, -1, style=wx.TE_PROCESS_ENTER, name='Search for broadcaster')
            self.search_site.SetDescriptiveText(text='Search uStream')
            self.search_site.Bind(wx.EVT_TEXT_ENTER, self.search_ustream)
            self.search_site.ShowCancelButton(True)
            self.search_str_lnk = wx.SearchCtrl(self, -1, style=wx.TE_PROCESS_ENTER, name='Open Broadcaster by URL')
            self.search_str_lnk.SetDescriptiveText(text='Enter URL to Open Stream')
            self.search_str_lnk.Bind(wx.EVT_TEXT_ENTER, self.open_manual_url)
            self.search_str_lnk.ShowCancelButton(True)
            self.temp_text_1 = wx.StaticText(self, -1, "")
            self.temp_text_2 = wx.StaticText(self, -1, "")
            self.temp_text_3 = wx.StaticText(self, -1, "")
            ###########################################################################################################
            box_sizer_horizontal_1 = wx.BoxSizer(wx.HORIZONTAL)
            box_sizer_horizontal_1.Add(self.temp_text_1, 19, wx.EXPAND + wx.CENTER)
            box_sizer_horizontal_1.Add(self.search_site, 25, wx.ALIGN_CENTER)
            box_sizer_horizontal_1.Add(self.temp_text_3, 5, wx.EXPAND + wx.CENTER)
            box_sizer_horizontal_1.Add(self.search_str_lnk, 25, wx.ALIGN_CENTER)
            box_sizer_horizontal_1.Add(self.temp_text_2, 5, wx.EXPAND + wx.CENTER)
            ###########################################################################################################
            self.SetSizer(box_sizer_horizontal_1)
            self.Layout()

        def open_manual_url(self, event):
            os.system("streamlink " + self.search_str_lnk.GetValue() + " " + config.get('pref_quality', 'quality'))

        @staticmethod
        def search_ustream(event):
            wx.MessageBox('uStream Search bar is unavailable.', 'Search Unavailable',
                          wx.OK | wx.ICON_INFORMATION)
            # Search bar on uStream has...gone missing. There appears to remnants of it within the HTML however.

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
            #   Apply pre-determined sidebar contents to tree. Enables changing of sidebar text via the parsed file.
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
            self.menu_tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.open_selected)
            ###########################################################################################################
            self.change_p_button = wx.Button(self, label='Change Platform')
            self.change_p_button.Bind(wx.EVT_BUTTON, self.return_service_select)
            ###########################################################################################################
            box_sizer_vertical_1 = wx.BoxSizer(wx.VERTICAL)
            box_sizer_vertical_1.Add(self.menu_tree, 15, wx.EXPAND)
            box_sizer_vertical_1.Add(self.change_p_button, 1, wx.ALIGN_CENTER)
            self.SetSizer(box_sizer_vertical_1)
            self.Layout()

        def return_service_select(self, event):
            ###########################################################################################################
            #   Closes 'InterfaceWindow'. Tests have shown this is a stable implementation, however, there are lingering
            #   concerns regarding how many times the 'switching' can take place before a problem is encountered.
            ###########################################################################################################
            frame = Window()
            frame.Show()
            InterfaceWindow.close_window(self.Parent)

        def open_selected(self, event):
            ###########################################################################################################
            #   Selection window for sidebar contents. Additional 'selections' can be added easily.
            #   'Try' encapsulation is due to the often occurring run-time error.
            ###########################################################################################################
            try:
                if self.menu_tree.GetItemText(event.GetItem()) == su_ustream_front.SideBar.Browse[0]:
                    pub.sendMessage("setup_browse_upcoming",
                                    message="http://www.ustream.tv/upcoming")
                elif self.menu_tree.GetItemText(event.GetItem()) == su_ustream_front.SideBar.Browse[1]:
                    pub.sendMessage("setup_browse_all",
                                    message="http://www.ustream.tv/explore/all")
                elif self.menu_tree.GetItemText(event.GetItem()) == su_ustream_front.SideBar.Browse[2]:
                    pub.sendMessage("setup_browse_all",
                                    message="http://www.ustream.tv/explore/news/all?type=live")
                elif self.menu_tree.GetItemText(event.GetItem()) == su_ustream_front.SideBar.Browse[3]:
                    pub.sendMessage("setup_browse_all",
                                    message="http://www.ustream.tv/explore/gaming/all?type=live")
                elif self.menu_tree.GetItemText(event.GetItem()) == su_ustream_front.SideBar.Browse[4]:
                    pub.sendMessage("setup_browse_all",
                                    message="http://www.ustream.tv/explore/entertainment/all?type=live")
                elif self.menu_tree.GetItemText(event.GetItem()) == su_ustream_front.SideBar.Browse[5]:
                    pub.sendMessage("setup_browse_all",
                                    message="http://www.ustream.tv/explore/sports/all?type=live")
                elif self.menu_tree.GetItemText(event.GetItem()) == su_ustream_front.SideBar.Browse[6]:
                    pub.sendMessage("setup_browse_all",
                                    message="http://www.ustream.tv/explore/animals/all?type=live")
                elif self.menu_tree.GetItemText(event.GetItem()) == su_ustream_front.SideBar.Browse[7]:
                    pub.sendMessage("setup_browse_all",
                                    message="http://www.ustream.tv/explore/music/all?type=live")
                elif self.menu_tree.GetItemText(event.GetItem()) == su_ustream_front.SideBar.Browse[8]:
                    pub.sendMessage("setup_browse_all",
                                    message="http://www.ustream.tv/explore/technology/all?type=live")
                elif self.menu_tree.GetItemText(event.GetItem()) == su_ustream_front.SideBar.Browse[9]:
                    pub.sendMessage("setup_browse_all",
                                    message="http://www.ustream.tv/explore/education/all?type=live")
                elif self.menu_tree.GetItemText(event.GetItem()) == su_ustream_front.SideBar.Log_in[0]:
                    pub.sendMessage("log_in")
                elif self.menu_tree.GetItemText(event.GetItem()) == su_ustream_front.SideBar.Log_in[1]:
                    pub.sendMessage("log_in")
                elif self.menu_tree.GetItemText(event.GetItem()) == su_ustream_front.SideBar.Log_in[2]:
                    pub.sendMessage("log_in")
                elif self.menu_tree.GetItemText(event.GetItem()) == su_ustream_front.SideBar.Options[0]:
                    #   Check to see if the user clicks 'advanced' and if they do, open a new frame
                    frame = Advanced()
                    frame.Show()
            except RuntimeError:
                temp = 1
                # This occurs when the program closes and reverts back to the start-up window

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
        ###########################################################################################################
        #   WARNING! This class contains numerous functions that may or may not be 'optimal'. Future efforts to
        #   update, refactor or alter code in this section should take care of what is changed as it may alter a
        #   significant number of features.
        ###########################################################################################################
        #   NOTE! 'Instance attribute defined outside of' warnings are a minor warning due to the __init__ function
        #   being subverted so 'refreshing' of pages can occur easily.
        ###########################################################################################################
        def __init__(self, parent):
            wx.Panel.__init__(self, parent, size=(1080, 668))
            self.init_ui()

        def setup_profile(self, url):
            url = "http://" + url
            self.broadcaster_profile_title, self.broadcaster_profile_description = ustream.ViewProfile.get_info(url)

        def show_profile(self, message):
            # ToDo: Fix/Redo layout
            self.setup_profile(message)
            ###########################################################################################################
            self.box_sizer_vertical_1.Add((0, 5))
            ###########################################################################################################
            self.prof_titl_txt = wx.StaticText(self, label=self.broadcaster_profile_title, style=wx.ALIGN_CENTRE)
            self.prof_titl_txt.Wrap(700)
            self.box_sizer_vertical_1.Add(self.prof_titl_txt, 1, wx.EXPAND)
            ###########################################################################################################
            self.prof_desc_txt = wx.StaticText(self, label=self.broadcaster_profile_description, style=wx.ALIGN_CENTRE)
            self.prof_desc_txt.Wrap(700)
            self.box_sizer_vertical_1.Add(self.prof_desc_txt, 1, wx.EXPAND)
            ###########################################################################################################
            self.box_sizer_vertical_1.Add((0, 5))
            ###########################################################################################################
            self.open_current_stream = wx.Button(self, label='Play Live Stream', size=(175, 33))
            self.box_sizer_horizontal_1.Add(self.open_current_stream, 1, wx.ALIGN_BOTTOM)
            self.open_current_stream.Bind(wx.EVT_BUTTON, lambda evt, temp=message: self.profile_play(evt, temp))
            ###########################################################################################################
            self.spacer = wx.StaticText(self, -1, "")
            self.box_sizer_horizontal_1.Add(self.spacer, 10, wx.EXPAND)
            ###########################################################################################################
            self.open_vod_list = wx.Button(self, label='View VoDs', size=(175, 33))
            self.box_sizer_horizontal_1.Add(self.open_vod_list, 1, wx.ALIGN_BOTTOM)
            self.open_vod_list.Bind(wx.EVT_BUTTON, self.profile_view_vod)
            ###########################################################################################################
            self.spacer2 = wx.StaticText(self, -1, "")
            self.box_sizer_horizontal_1.Add(self.spacer2, 10, wx.EXPAND)
            ###########################################################################################################
            self.open_related = wx.Button(self, label='Show Related Channels', size=(175, 33))
            self.box_sizer_horizontal_1.Add(self.open_related, 1, wx.ALIGN_BOTTOM)
            self.open_related.Bind(wx.EVT_BUTTON, self.profile_view_related)
            self.box_sizer_vertical_1.Add(self.box_sizer_horizontal_1)
            ###########################################################################################################
            self.SetSizer(self.box_sizer_vertical_1)
            self.Layout()

        @staticmethod
        def profile_play(event, url):
            script = "streamlink " + url + " " + config.get('pref_quality', 'quality')
            os.system(script)

        @staticmethod
        def profile_view_vod(event):
            wx.MessageBox('Not Available for this service.', 'Not Available',
                          wx.OK | wx.ICON_INFORMATION)

        @staticmethod
        def profile_view_related(event):
            wx.MessageBox('Not Available for this service.', 'Not Available',
                          wx.OK | wx.ICON_INFORMATION)

        def init_ui(self):
            self.colour_control()
            ###########################################################################################################
            self.broadcaster_data_length = len(broadcaster_title)
            self.broadcaster_index = 0
            self.page_in_use = 0
            self.broadcaster_profile_title = ""
            self.broadcaster_profile_description = ""
            self.broadcaster_profile_url = ""
            ###########################################################################################################
            pub.subscribe(self.dark_mode, 'dark_mode')
            pub.subscribe(self.setup_browse_all, 'setup_browse_all')
            pub.subscribe(self.setup_browse_upcoming, 'setup_browse_upcoming')
            pub.subscribe(self.reset_browse_area, 'reset_browse_area')
            pub.subscribe(self.show_profile, 'show_profile')
            pub.subscribe(self.log_in, 'log_in')
            ###########################################################################################################
            self.box_sizer_vertical_1 = wx.BoxSizer(wx.VERTICAL)
            self.box_sizer_horizontal_1 = wx.BoxSizer(wx.HORIZONTAL)
            self.grid_sizer_1 = wx.GridSizer(2, 3, 5, 5)
            self.SetSizer(self.box_sizer_vertical_1)
            self.grid_sizer_1.Layout()

        @staticmethod
        def log_in():
            wx.MessageBox('Not Available for this service.', 'Not Available',
                          wx.OK | wx.ICON_INFORMATION)

        def setup_browse_upcoming(self, message):
            global broadcaster_title, broadcaster_viewers, broadcaster_url, broadcaster_thumbnail
            try:
                broadcaster_title, broadcaster_viewers, broadcaster_url, broadcaster_thumbnail = \
                    ustream.BrowseUpcoming.get_info(message)
                self.reset_browse_area()
                self.init_browse_upcoming()
                self.set_browse_all()
            except IndexError:
                wx.MessageBox('Unable to Obtain uStream Data. Please try again or restart the application.', 'Error: 1',
                              wx.OK | wx.ICON_INFORMATION)
                self.reset_browse_area()

        def setup_browse_all(self, message):
            global broadcaster_title, broadcaster_viewers, broadcaster_url, broadcaster_thumbnail
            try:
                broadcaster_title, broadcaster_viewers, broadcaster_url, broadcaster_thumbnail = \
                    ustream.BrowseAll.get_info(message)
                self.reset_browse_area()
                self.init_browse_all()
                self.set_browse_all()
            except IndexError:
                wx.MessageBox('Unable to Obtain uStream Data. Please try again or restart the application.', 'Error: 1',
                              wx.OK | wx.ICON_INFORMATION)
                self.reset_browse_area()

        def reset_browse_area(self):
            if self.page_in_use == 1:
                self.DestroyChildren()
                self.init_ui()

        def init_browse_upcoming(self):
            self.box_sizer_vertical_1.Add(self.grid_sizer_1, wx.EXPAND)
            self.page_in_use = 1
            self.SetSizer(self.box_sizer_vertical_1)

        def init_browse_all(self):
            self.box_sizer_vertical_1.Add(self.grid_sizer_1, wx.EXPAND)
            self.page_in_use = 1
            ###########################################################################################################
            self.first_button = wx.Button(self, label='First Page', size=(123, 33))
            self.box_sizer_horizontal_1.Add(self.first_button, 1, wx.ALIGN_BOTTOM + wx.ALIGN_LEFT)
            self.first_button.Bind(wx.EVT_BUTTON, self.previous_page)
            ###########################################################################################################
            self.spacer = wx.StaticText(self, -1, "")
            self.box_sizer_horizontal_1.Add(self.spacer, 10, wx.EXPAND + wx.CENTER)
            ###########################################################################################################
            self.next_button = wx.Button(self, label='Next Page', size=(123, 33))
            self.box_sizer_horizontal_1.Add(self.next_button, 1, wx.ALIGN_BOTTOM + wx.ALIGN_RIGHT)
            self.next_button.Bind(wx.EVT_BUTTON, self.next_page)
            ###########################################################################################################
            self.box_sizer_vertical_1.Add(self.box_sizer_horizontal_1, wx.EXPAND)
            self.SetSizer(self.box_sizer_vertical_1)

        def set_browse_all(self):
            global broadcaster_title, broadcaster_viewers, broadcaster_url, broadcaster_thumbnail
            min_a = 0
            max_a = 6
            for i in range(min_a, max_a):
                if self.broadcaster_index >= self.broadcaster_data_length:
                    break
                    # This 'code' runs when there is nothing else to display. Iterator (i) should always run until 5.
                else:
                    self.grid_sizer_1.Add(self.BroadcastContainer(self))
                    self.broadcaster_index = self.broadcaster_index + 1
            self.Layout()

        def get_index(self):
            return self.broadcaster_index

        def next_page(self, event):
            if self.broadcaster_index != self.broadcaster_data_length:
                pub.sendMessage("clear_container", message='clear_container')
                self.SetSizer(self.box_sizer_vertical_1)
                self.Layout()
                self.set_browse_all()

        def previous_page(self, event):
            if self.broadcaster_index > 6:
                pub.sendMessage("clear_container", message='clear_container')
                self.broadcaster_index = self.broadcaster_index - self.broadcaster_index
                self.SetSizer(self.box_sizer_vertical_1)
                self.Layout()
                self.set_browse_all()

        class BroadcastContainer(wx.Panel):
            def __init__(self, parent):
                wx.Panel.__init__(self, parent, size=(353, 297))
                ########################################################################################################
                #   'Container' for all broadcasting meta-data. At most, six of these will be displayed per page and if
                #   the page scrolls backwards or forwards, the containers will be wiped ready for new data.
                ########################################################################################################
                global broadcaster_title, broadcaster_viewers, broadcaster_url, broadcaster_thumbnail
                pub.subscribe(self.clear_container, 'clear_container')
                self.box_sizer = wx.BoxSizer(wx.VERTICAL)
                ########################################################################################################
                self.title = wx.StaticText(self, -1, broadcaster_title[InterfaceWindow.InterfaceMain.get_index(parent)],
                                           style=wx.ALIGN_CENTRE)
                self.title.name = broadcaster_url[InterfaceWindow.InterfaceMain.get_index(parent)]
                self.box_sizer.Add(self.title), wx.EXPAND
                self.title.Bind(wx.EVT_LEFT_DOWN, self.on_click_title)
                ########################################################################################################
                #   Download image file from the URL scraped, using urllib.request, to a local folder
                ########################################################################################################
                urllib.request.urlretrieve(broadcaster_thumbnail[InterfaceWindow.InterfaceMain.get_index(parent)],
                                           "temp_img/" + str(InterfaceWindow.InterfaceMain.get_index(parent)) + ".bmp")
                self.thumbnail = wx.Image("temp_img/" + str(InterfaceWindow.InterfaceMain.get_index(parent)) + ".bmp")
                ########################################################################################################
                #   Convert base image to a usable bitmap for the wxPython objects
                ########################################################################################################
                self.thumbnail_use_me = self.thumbnail.ConvertToBitmap()
                self.thumbnail_sb = wx.StaticBitmap(self, -1, self.thumbnail_use_me, name="empty")
                self.thumbnail_sb.name = broadcaster_url[InterfaceWindow.InterfaceMain.get_index(parent)]
                #   ^ Assign 'name' to the URL. This allows the URL to become assigned to the object and thusly called
                #   ^ upon with ease
                self.thumbnail_sb.Bind(wx.EVT_LEFT_DOWN, self.on_click_thumbnail)
                self.box_sizer.Add(self.thumbnail_sb)
                ########################################################################################################
                #   The returned 'viewers' from uStream is often inconsistent. This is likely due to uStream often not
                #   providing ANY value, thus messing up the scraping and often assignment of viewers to streams.
                ########################################################################################################
                try:
                    self.box_sizer.Add(wx.StaticText(self, -1, broadcaster_viewers[InterfaceWindow.InterfaceMain.
                                                     get_index(parent)], style=wx.ALIGN_CENTRE))
                except IndexError:
                    self.box_sizer.Add(wx.StaticText(self, -1, "N/A", style=wx.ALIGN_CENTRE))
                self.SetSizer(self.box_sizer)
                self.Layout()

            @staticmethod
            def on_click_thumbnail(event):
                name = event.GetEventObject().name
                script = "streamlink " + name + " " + config.get('pref_quality', 'quality')
                os.system(script)

            @staticmethod
            def on_click_title(event):
                message = event.GetEventObject().name
                pub.sendMessage("reset_browse_area")
                pub.sendMessage("show_profile", message=message)

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
        wx.Frame.__init__(self, None, title='Public Stream Viewer (uStream)', size=(1280, 768),
                          style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)
        ###########################################################################################################
        self.panel1 = InterfaceWindow.InterfaceTop(self)
        self.panel2 = InterfaceWindow.InterfaceSide(self)
        self.panel3 = InterfaceWindow.InterfaceMain(self)
        ###########################################################################################################
        # pub.subscribe(self.service_listener, 'ok')
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


def main_serv_select():
    app = wx.App(False)
    Window()
    app.MainLoop()


if __name__ == '__main__':
    main_serv_select()
