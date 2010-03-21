#! /usr/bin/env python
# Copyright (c) 2010 Javier Uruen (juruen@warp.es)
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from inspyktor  import systemcall
from inspyktor.ui import centralwidget
from PyQt4 import QtGui, QtCore


class CentralWidget(QtGui.QWidget, centralwidget.Ui_CentralWidget):
    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.sysCallModel = systemcall.SystemCallModel()
        self.proxyModel = QtGui.QSortFilterProxyModel(self)
        self.proxyModel.setSourceModel(self.sysCallModel)
        self.sysCallView.setModel(self.proxyModel)
        self.sysCallView.setCornerButtonEnabled(False)
        self.sysCallView.setShowGrid(False)
        self.sysCallView.verticalHeader().hide()
        self.sysCallView.hideColumn(0)
        self.sysCallView.horizontalHeader().setResizeMode(3,
           QtGui.QHeaderView.Stretch)


        self.connect(self.startButton, QtCore.SIGNAL('clicked()'),
             self._slot_start_button)
        self.connect(self.filterLine,
            QtCore.SIGNAL('textChanged(const QString&)'),
            self._slot_filter_text_changed)

    def _slot_start_button(self):
        split_cmd = str(self.commandLine.text()).split()
        self.sysCallModel.clearData()
        self.sysCallModel.strace_runner.set_trace_command(split_cmd[0],
            split_cmd[1:])
        self.sysCallModel.strace_runner.start_trace()

    def _slot_filter_text_changed(self, filter):
        self.proxyModel.setFilterRegExp(QtCore.QRegExp(filter))
