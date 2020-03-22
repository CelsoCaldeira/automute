#!/usr/bin/python3
# -*- coding: utf-8 -*-
#esta é a versão mais atualizada, com melhor código
#versão para python 3
#depende dos pacotes wxpython
import wx.adv
import sys, os
import subprocess
from wx.lib.embeddedimage import PyEmbeddedImage 

TRAY_TOOLTIP = 'System Tray Demo'
TRAY_ICON =	'icon.png'
RED = 'red.png'
ON = "Som na Caixa!"
OFF = "Headphone"

def saida():
	status, estado = subprocess.getstatusoutput("/usr/bin/amixer -c 1 sget \"Auto-Mute Mode\" | grep Item0 | cut -d\"'\" -f2")
	return estado

def amute():
	estado=saida()
	if estado == "Enabled":
		os.system("/usr/bin/amixer -c 1 sset \"Auto-Mute Mode\" Disabled 1>/dev/null")
		os.system("/usr/bin/amixer -c 1 sset \"Channel Mode\" 6ch 1>/dev/null")
		return estado
	else:
		os.system("/usr/bin/amixer -c 1 sset \"Auto-Mute Mode\" Enabled 1>/dev/null")
		os.system("/usr/bin/amixer -c 1 sset \"Channel Mode\" 2ch 1>/dev/null")
		return estado

def create_menu_item(menu, label, func):
    item = wx.MenuItem(menu, -1, label)
    menu.Bind(wx.EVT_MENU, func, id=item.GetId())
    menu.Append(item)
    return item

class TaskBarIcon(wx.adv.TaskBarIcon):
	def __init__(self, frame):
		self.frame = frame
		super(TaskBarIcon, self).__init__()
		estado=saida()
		if estado == "Enabled":
			self.set_icon(RED, OFF)
		else:
			self.set_icon(TRAY_ICON, ON)
		self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.on_left_down)
	
	def CreatePopupMenu(self):
		menu = wx.Menu()
		create_menu_item(menu, 'Automute', self.on_hello)
		menu.AppendSeparator()
		create_menu_item(menu, 'Exit', self.on_exit)
		return menu
	
	def set_icon(self, path, state):
		icon = wx.Icon(wx.Bitmap(path))
		self.SetIcon(icon, state)
	
	def on_left_down(self, event):
		estado=amute()
		if estado == "Enabled":
			self.set_icon(TRAY_ICON, ON)
		else:
			self.set_icon(RED, OFF)
			
	def on_hello(self, event):
		estado=amute()
		if estado == "Enabled":
			self.set_icon(TRAY_ICON, ON)
		else:
			self.set_icon(RED, OFF)

	def on_exit(self, event):
		wx.CallAfter(self.Destroy)
		self.frame.Close()

class App(wx.App):
	def OnInit(self):
		frame=wx.Frame(None)
		self.SetTopWindow(frame)
		TaskBarIcon(frame)
		return True

def main():
    app = App(False)
    app.MainLoop()

if __name__ == '__main__':
    main()
