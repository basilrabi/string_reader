# -*- coding: utf-8 -*-
"""
/***************************************************************************
 StringReader
                                 A QGIS plugin
 Reads string files
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2020-07-11
        git sha              : $Format:%H$
        copyright            : (C) 2020 by Basil Eric C. Rabi
        email                : ericbasil.rabi@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

# pylint: disable=import-error
# pylint: disable=relative-beyond-top-level

import os
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QFileDialog
from . import resources
from .string_importer import import_str
from .string_reader_dialog import StringReaderDialog


class StringReader:

    def __init__(self, iface):
        self.actions = []
        self.dlg = StringReaderDialog()
        self.first_start = None
        self.iface = iface
        self.menu = 'String Reader'
        self.plugin_dir = os.path.dirname(__file__)

        self.dlg.lineEdit.clear()
        self.dlg.pushButton.clicked.connect(self.select_string_file)

    def add_action(self,
                   icon_path,
                   text,
                   callback,
                   enabled_flag=True,
                   add_to_menu=True,
                   add_to_toolbar=True,
                   status_tip=None,
                   whats_this=None,
                   parent=None):
        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)
        if status_tip is not None:
            action.setStatusTip(status_tip)
        if whats_this is not None:
            action.setWhatsThis(whats_this)
        if add_to_toolbar:
            self.iface.addToolBarIcon(action)
        if add_to_menu:
            self.iface.addPluginToVectorMenu(self.menu, action)
        self.actions.append(action)
        return action

    def initGui(self):
        icon_path = ':/plugins/string_reader/icon.png'
        self.add_action(icon_path,
                        text='Read String File',
                        callback=self.run,
                        parent=self.iface.mainWindow())
        self.first_start = True

    def unload(self):
        for action in self.actions:
            self.iface.removePluginVectorMenu('String Reader', action)
            self.iface.removeToolBarIcon(action)

    def select_string_file(self):
        filename = QFileDialog.getOpenFileName(
            self.dlg, 'Select string file', '', '*.str'
        )
        self.dlg.lineEdit.setText(filename[0])

    def run(self):
        if self.first_start == True:
            self.first_start = False

        self.dlg.show()
        result = self.dlg.exec_()
        if result:
            filename = self.dlg.lineEdit.text()
            import_str(filename)
