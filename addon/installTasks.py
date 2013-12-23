# -*- coding: UTF-8 -*-

import addonHandler
import globalVars
import os
import shutil
import glob
import gui
import wx

basePath = os.path.dirname(__file__).decode("mbcs")

addonHandler.initTranslation()

def onInstall():
	for addon in addonHandler.getAvailableAddons():
		if addon.manifest['name'] == "TeamViewerNVDASupport":
			if gui.messageBox(
				# Translators: the label of a message box dialog.
				_("You have installed the TeamViewerNVDASupport add-on, probably an old and incompatible version with this one. Do you want to uninstall the old version?"),
				# Translators: the title of a message box dialog.
				_("Uninstall incompatible add-on"),
				wx.YES|wx.NO|wx.ICON_WARNING)==wx.YES:
					addon.requestRemove()
			break
