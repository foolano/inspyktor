#! /usr/bin/env python
# Copyright (c) 2010 Javier Uruen (juruen@warp.es)
# Licensed under the terms of the MIT license

import inspyktor
import sys

from PyQt4 import QtGui, QtCore
from PyKDE4 import kdeui, kdecore
from inspyktor import stracerunner, mainwindow


def main():
    _ = kdecore.ki18n

    emptyloc = kdecore.KLocalizedString()

    about_data = kdecore.KAboutData(
            inspyktor.__appname__,
            "",
            _(inspyktor.__progname__),
            inspyktor.__version__,
            _(inspyktor.__description__),
            kdecore.KAboutData.License_Custom,
            _(inspyktor.__copyright__),
            emptyloc,
            inspyktor.__homepage__,
            inspyktor.__bts__)

    options = kdecore.KCmdLineOptions()
    options.add("command <command>", _("Command to trace"))
    options.add("pid <pid>", _("PID of existing process to trace"))

    kdecore.KCmdLineArgs.init(sys.argv, about_data)
    kdecore.KCmdLineArgs.addCmdLineOptions(options)

    args = kdecore.KCmdLineArgs.parsedArgs()

    if args.isSet("command"):
        print args.getOption("command")

    a = kdeui.KApplication()

    strace_runner = stracerunner.StraceRunner()
    strace_runner.set_trace_command("ls", ["-l"])
    QtCore.QTimer.singleShot(0, strace_runner.slot_trace_command)

    main_window = mainwindow.MainWindow()
    main_window.show()
    main_window.central_widget.sysCallModel.set_strace_runner(strace_runner)

    sys.exit(a.exec_())
