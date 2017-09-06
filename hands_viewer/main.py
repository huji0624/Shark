#!/usr/bin/python
#  -*- coding: UTF-8 -*-


import Tkinter
import dashboard
top = Tkinter.Tk("HandsViewer")
dashboard.DashBoard(top).show()
top.attributes("-topmost", True)
top.mainloop()