# -*- coding: UTF-8 -*-

# App module for TeamViewer 9, trial version:
# http://www.teamviewer.com
# Date: 23/12/2013
# Version: 1.0
# Following community add-on guidelines
# Based on TeamViewerNVDASupport:
# Version: 1.1
# Date: 09/12/2012
# Fixed some spelling mistakes in this file
# Updated for TeamViewer 8, trial version

import appModuleHandler
import addonHandler
import languageHandler
import os
import api
import controlTypes
import ui

addonHandler.initTranslation()

# The root of the addon folder
_addonDir = os.path.join(os.path.dirname(__file__), "..").decode("mbcs")
_curAddon = addonHandler.Addon(_addonDir)
_addonSummary = _curAddon.manifest['summary']
_scriptCategory = unicode(_addonSummary)

class AppModule(appModuleHandler.AppModule):

	scriptCategory = _scriptCategory

	def event_NVDAObject_init(self, obj):
		if obj.windowControlID == 20098:
			# Translators: label for the ID control in TeamViewer's main dialog.
			obj.name = _("ID")
		elif obj.windowControlID == 20099:
			# Translators: label for the password control in TeamViewer's main dialog.
			obj.name = _("Password")

	def getDocFolder(self):
		langs = [languageHandler.getLanguage(), "en"]
		for lang in langs:
			docFolder = os.path.join(os.path.dirname(__file__), "..", "doc", lang)
			if os.path.isdir(docFolder):
				return docFolder
			if "_" in lang:
				tryLang = lang.split("_")[0]
				docFolder = os.path.join(os.path.dirname(__file__), "..", "doc", tryLang)
				if os.path.isdir(docFolder):
					return docFolder
				if tryLang == "en":
					break
			if lang == "en":
				break
		return None

	def getDocPath(self, docFileName):
		docPath = self.getDocFolder()
		if docPath is not None:
			docFile = os.path.join(docPath, docFileName)
			if os.path.isfile(docFile):
				docPath = docFile
		return docPath

	def script_about(self, gesture):
		try:
			os.startfile(self.getDocPath("readme.html"))
		except WindowsError:
			pass
	# Translators: message presented in input mode.
	script_about.__doc__ = _("Opens the documentation for this application module.")

	def script_copyData(self, gesture):
		obj = api.getForegroundObject().simpleLastChild.simpleLastChild.simplePrevious
		if not obj:
			return
		password = obj.value
		if not password:
			return
		obj = obj.simplePrevious.simplePrevious
		id = obj.value
		data = _("ID: {0} - Password: {1}").format(id, password)
		if api.copyToClip(data):
			# Translators: message presented when TeamViewer's ID and password have been copied to the clipboard.
			ui.message(_("ID and password copied to clipboard."))
	# Translators: message presented in input mode.
	script_copyData.__doc__ = _("Copies your ID and password to the clipboard.")

	def script_changeTab(self, gesture):
		obj = api.getForegroundObject().simpleFirstChild
		children = obj.children
		if len(children) != 3:
		# Translators: message presented when trying to switch to a different tab, but the main dialog of TeamViewer is not focused.
			ui.message(_("You are out of main dialog."))
			return
		index = 0
		for child in children:
			if controlTypes.STATE_SELECTED in child.states:
				break
			else:
				index += 1
		if index <= 1:
			index = 2
		else:
			index = 1
		children[index].setFocus()
	# Translators: message presented in input mode.
	script_changeTab.__doc__ = _("Changes the selected tab on the main dialog of TeamViewer.")

	__gestures = {
		"kb:NVDA+shift+c": "copyData",
		"kb:control+tab": "changeTab",
		"kb:control+shift+tab": "changeTab",
		"kb:control+shift+NVDA+h": "about",
	}
