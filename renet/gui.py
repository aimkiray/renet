#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/24
# @Author  : aimkiray

import wx
import wx.adv
from raw import img
from threading import Thread
from renet import renet
from conf import config
import time
import sys

my_config = config.Config()


########################################################################
class ReNetIcon(wx.adv.TaskBarIcon):
    TBMENU_RESTORE = wx.NewId()
    TBMENU_CLOSE = wx.NewId()
    TBMENU_CHANGE = wx.NewId()
    TBMENU_REMOVE = wx.NewId()

    # ----------------------------------------------------------------------
    def __init__(self, parent):
        wx.adv.TaskBarIcon.__init__(self)
        self.parent = parent

        # Set the image
        self.tbIcon = img.getIcon()

        self.SetIcon(self.tbIcon, "reNet")

        # bind some events
        self.Bind(wx.EVT_MENU, self.OnTaskBarClose, id=self.TBMENU_CLOSE)
        self.Bind(wx.EVT_MENU, self.ShowMainFrame, id=self.TBMENU_RESTORE)
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.OnTaskBarLeftClick)

    # ----------------------------------------------------------------------
    def CreatePopupMenu(self, evt=None):
        """
        This method is called by the base class when it needs to popup
        the menu for the default EVT_RIGHT_DOWN event.  Just create
        the menu how you want it and return it from this function,
        the base class takes care of the rest.
        """
        menu = wx.Menu()
        menu.Append(self.TBMENU_RESTORE, "Setting")
        # menu.Append(self.TBMENU_CHANGE, "Show all the Items")
        menu.AppendSeparator()
        menu.Append(self.TBMENU_CLOSE, "Exit")
        return menu

    def ShowMainFrame(self, evt):
        self.parent.Show()

    # ----------------------------------------------------------------------
    def OnTaskBarActivate(self, evt):
        """"""
        pass

    # ----------------------------------------------------------------------
    def OnTaskBarClose(self, evt):
        """
        Destroy the taskbar icon and frame from the taskbar icon itself
        """
        self.parent.Close()

    # ----------------------------------------------------------------------
    def OnTaskBarLeftClick(self, evt):
        """
        Create the right-click menu
        """
        menu = self.CreatePopupMenu()
        self.PopupMenu(menu)
        menu.Destroy()


########################################################################
class MainPanel(wx.Panel):
    """"""

    # ----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""

        my_conf = my_config.get_config()
        self.parent = parent

        wx.Panel.__init__(self, parent=parent)

        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.panelSizer = wx.BoxSizer(wx.VERTICAL)
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)

        # add prev/next buttons
        self.okBtn = wx.Button(self, label="OK")
        self.okBtn.Bind(wx.EVT_BUTTON, self.onOK)
        # self.okBtn.Disable()
        btnSizer.Add(self.okBtn, 0, wx.ALL | wx.ALIGN_RIGHT, 5)

        self.applyBtn = wx.Button(self, label="Apply")
        self.applyBtn.Bind(wx.EVT_BUTTON, self.onApply)
        btnSizer.Add(self.applyBtn, 0, wx.ALL | wx.ALIGN_RIGHT, 5)

        # finish layout
        self.mainSizer.Add(self.panelSizer, 1, wx.EXPAND)
        self.mainSizer.Add(btnSizer, 0, wx.ALIGN_RIGHT)
        self.SetSizer(self.mainSizer)

        # Create widget controls
        # ----------------------------------------------------------------------------------------
        # PAC file
        box = wx.StaticBoxSizer(wx.StaticBox(self, label="Automatic Proxy"), wx.VERTICAL)

        self.cb_auto = wx.CheckBox(self,
                                   label=' Use the PAC file to automatically switch proxy based on the websites.',
                                   style=wx.TE_LEFT)
        box.Add(self.cb_auto, 0, wx.EXPAND | wx.ALIGN_CENTRE | wx.ALL, 5)

        sizer_inline = wx.BoxSizer(wx.HORIZONTAL)

        self.pac_file_label = wx.StaticText(self, wx.ID_ANY, "PAC File: ", style=wx.TE_LEFT)
        sizer_inline.Add(self.pac_file_label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)

        self.pac_file_input = wx.FilePickerCtrl(self, wx.ID_ANY, my_conf['pac_file_path'], wildcard="*.pac")
        self.pac_file_input.SetHelpText("Click the right button to select a PAC file.")
        sizer_inline.Add(self.pac_file_input, 1, wx.ALIGN_CENTRE | wx.ALL, 5)

        box.Add(sizer_inline, 0, wx.EXPAND | wx.ALIGN_CENTRE | wx.ALL, 5)

        self.panelSizer.Add(box, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        # Optional Sheet Name
        box = wx.StaticBoxSizer(wx.StaticBox(self, label="Manual Proxy"), wx.VERTICAL)

        self.cb_manually = wx.CheckBox(self,
                                       label=' Manually specify a global proxy.',
                                       style=wx.TE_LEFT)
        box.Add(self.cb_manually, 0, wx.EXPAND | wx.ALIGN_CENTRE | wx.ALL, 5)

        sizer_inline = wx.BoxSizer(wx.HORIZONTAL)

        self.address_label = wx.StaticText(self, wx.ID_ANY, "Address: ", style=wx.TE_LEFT)
        sizer_inline.Add(self.address_label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)

        self.address_input = wx.TextCtrl(self, wx.ID_ANY, my_conf['address'])
        sizer_inline.Add(self.address_input, 1, wx.ALIGN_CENTRE | wx.ALL, 5)

        box.Add(sizer_inline, 0, wx.EXPAND | wx.ALIGN_CENTRE | wx.ALL, 5)

        self.panelSizer.Add(box, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        # Blank
        box = wx.BoxSizer(wx.HORIZONTAL)
        sep_or = wx.StaticText(self, wx.ID_ANY, "", style=wx.TE_CENTER)
        box.Add(sep_or, 1, wx.ALIGN_CENTRE_HORIZONTAL | wx.ALL, 5)
        self.panelSizer.Add(box, 1, wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)

        # Other
        box = wx.BoxSizer(wx.HORIZONTAL)

        self.server_port_label = wx.StaticText(self, wx.ID_ANY, "PAC Server Port: ", style=wx.TE_LEFT)
        box.Add(self.server_port_label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)

        self.server_port_input = wx.TextCtrl(self, wx.ID_ANY, my_conf['pac_server_port'])
        box.Add(self.server_port_input, 1, wx.ALIGN_CENTRE | wx.ALL, 5)

        sep_or = wx.StaticText(self, wx.ID_ANY, "", style=wx.TE_CENTER)
        box.Add(sep_or, 1, wx.ALIGN_CENTRE_HORIZONTAL | wx.ALL, 5)

        self.cb_lock = wx.CheckBox(self, label=' Lock setting', style=wx.TE_LEFT)
        box.Add(self.cb_lock, 0, wx.EXPAND | wx.ALIGN_CENTRE | wx.ALL, 5)
        self.cb_lock.SetValue(True)

        self.panelSizer.Add(box, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        self.Bind(wx.EVT_CHECKBOX, self.onChecked)
        self.Bind(wx.EVT_KEY_UP, self.onEnable)

        # default
        self.cb_auto.SetValue(True)
        self.address_input.Disable()

        # And indicate we don't have a worker thread yet
        self.worker = None

    def onEnable(self, e):
        self.doEnable()

    def doEnable(self):
        self.okBtn.Enable()
        self.applyBtn.Enable()

    def onChecked(self, e):
        self.doEnable()
        cb = e.GetEventObject()
        if cb.GetLabel() == ' Use the PAC file to automatically switch proxy based on the websites.':
            self.cb_manually.SetValue(False)
            self.address_input.Disable()
            self.pac_file_input.Enable()
        elif cb.GetLabel() == ' Manually specify a global proxy.':
            self.cb_auto.SetValue(False)
            self.address_input.Enable()
            self.pac_file_input.Disable()

    def onOK(self, event):
        self.onStop()
        self.onStart()
        self.parent.Hide()

    def onApply(self, event):
        self.applyBtn.Disable()
        self.onStop()
        self.onStart()

    def onStart(self):
        """Start Computation."""
        # Trigger the worker thread unless it's already busy
        self.worker = WorkerThread(self)

    def onStop(self):
        """Stop Computation."""
        # Flag the worker thread to stop if running
        if self.worker:
            self.worker.abort()


# Thread class that executes processing
########################################################################
class WorkerThread(Thread):
    """Worker Thread Class."""

    # ----------------------------------------------------------------------
    def __init__(self, parent):
        """Init Worker Thread Class."""
        Thread.__init__(self)

        # Read input
        self.pac = parent.pac_file_input.GetPath()
        self.address = parent.address_input.GetValue()
        self.pac_port = parent.server_port_input.GetValue()

        self.auto = parent.cb_auto.GetValue()
        self.manually = parent.cb_manually.GetValue()
        self.lock = parent.cb_lock.GetValue()

        # Stop signal
        self._want_abort = 0
        # This starts the thread running on creation
        self.start()

    def run(self):
        """Run Worker Thread"""
        # save setting
        my_config.set_config(self)
        # start file server
        renet.run_server(self.pac_port, self.pac)
        pac_file_name = self.pac.split("\\")[-1]
        if self.auto:
            proxy_type = 5
            key_name = 'http://127.0.0.1:' + str(self.pac_port) + '/' + pac_file_name
            binary_proxy = renet.prepare_my_proxy(key_name)
        elif self.manually:
            proxy_type = 3
            key_name = self.address
            binary_proxy = renet.prepare_my_proxy(key_name)
        while True:
            result = renet.monitor_key(key_name, proxy_type)
            if not result:
                renet.exec_change(binary_proxy)
            # Stop event
            if self._want_abort:
                break
            if not self.lock:
                break
            else:
                # Interval 2s, monitoring proxy setting
                time.sleep(2)

    def abort(self):
        """abort worker thread."""
        # Method for use by main thread to signal an abort
        self._want_abort = 1


########################################################################
class MainForm(wx.Frame):

    # ----------------------------------------------------------------------
    def __init__(self):
        wx.Frame.__init__(self, None, title="reNet", size=(500, 500))

        self.panel = MainPanel(self)
        self.tbIcon = ReNetIcon(self)

        self.Bind(wx.EVT_CLOSE, self.onClose)
        self.Bind(wx.EVT_ICONIZE, self.onMinimize)

    def onMinimize(self, event):
        """
        When minimizing, hide the frame so it "minimizes to tray"
        """
        if self.IsIconized():
            self.Hide()

    # ----------------------------------------------------------------------
    def onClose(self, event):
        """
        Destroy the taskbar icon and the frame
        """
        self.panel.onStop()
        self.panel.Destroy()
        self.tbIcon.RemoveIcon()
        self.tbIcon.Destroy()
        self.Destroy()
        sys.exit()


# ----------------------------------------------------------------------
# Run the program
if __name__ == "__main__":
    app = wx.App(False)
    frame = MainForm().Show()
    app.MainLoop()
