#!/usr/bin/python
#  -*- coding: UTF-8 -*-


import Tkinter
import dashboard
root = Tkinter.Tk("HandsViewer")
dashboard.DashBoard(root).show()
root.lift()
root.attributes('-topmost',True)
root.after_idle(root.attributes,'-topmost',False)
root.mainloop()