# -*- coding: UTF-8 -*-

# App module for TeamViewer 9, trial version:
# http://www.teamviewer.com
# Date: 08/05/2015
# Version: 3.0
# Used windowsUtil instead of objects position to find windows
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
import os
import api
import controlTypes
import ui
import winUser
import windowUtils
import NVDAObjects.IAccessible

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

	def script_copyData(self, gesture):
		try:
			obj = NVDAObjects.IAccessible.getNVDAObjectFromEvent(
			windowUtils.findDescendantWindow(api.getForegroundObject().windowHandle, controlID=20099),
			winUser.OBJID_CLIENT, 0)
		except LookupError:
			return
		password = obj.value
		if not password:
			return
		try:
			obj = NVDAObjects.IAccessible.getNVDAObjectFromEvent(
			windowUtils.findDescendantWindow(api.getForegroundObject().windowHandle, controlID=20098),
			winUser.OBJID_CLIENT, 0)
		except LookupError:
			return
		id = obj.value
		# Translators: a formatted message with the id and password which will be copied to clipboard ready to be pasted in a chat or similar to enable the individuals to share a team viewer session.
		data = _("ID: {idValue} - Password: {passwordValue}").format(idValue=id, passwordValue=password)
		if api.copyToClip(data):
			# Translators: message presented when TeamViewer's ID and password have been copied to the clipboard.
			ui.message(_("ID and password copied to clipboard."))
	# Translators: message presented in input mode.
	script_copyData.__doc__ = _("Copies your ID and password to the clipboard ready for sharing.")

	def script_changeTab(self, gesture):
		obj = api.getForegroundObject().firstChild.firstChild
		if not obj:
			return
		children = obj.children
		if len(children) != 3:
			# Translators: message presented when trying to switch to a different tab, but the main dialog of TeamViewer is not focused.
			ui.message(_("Unable to switch tab, please ensure the main dialog has focus."))
			return
		index = 0
		for child in children:
			if controlTypes.STATE_SELECTED in child.states:
				break
			index += 1
		if index <= 1:
			index = 2
		else:
			index = 1
		children[index].setFocus()
	# Translators: message presented in input mode.
	script_changeTab.__doc__ = _("In the main dialog of TeamViewer, changes the selected tab.")

	def script_moveToExternalID(self, gesture):
		try:
			obj = NVDAObjects.IAccessible.getNVDAObjectFromEvent(
			windowUtils.findDescendantWindow(api.getForegroundObject().windowHandle, visible=True, controlID=1001),
			winUser.OBJID_CLIENT, 0)
		except LookupError:
			return
		obj.setFocus()
	# Translators: message presented in input mode.
	script_moveToExternalID.__doc__ = _("In the main dialog of TeamViewer, moves the focus to the external ID field of the selected tab.")

	__gestures = {
		"kb:NVDA+shift+c": "copyData",
		"kb:control+tab": "changeTab",
		"kb:control+shift+tab": "changeTab",
		"kb:control+shift+a": "moveToExternalID",
	}
