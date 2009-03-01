# python graphical progress bar
# Min-Hua Chen <orca.chen@gmail.com> 

import Tkinter

class pb:
	# constructor
	def __init__(self, root, title):
		self.root = root
		self.width = 350
		self.height = 30
		self.title = title
		self.w = Tkinter.Toplevel()
		# put the progress bar on the center of the screen
		w = self.w.winfo_screenwidth() / 2
		h = self.w.winfo_screenheight() / 2
		self.w.geometry("+" + `w - self.width / 2` + 
				"+" + `h - self.height / 2`)
		self.w.title("0%" + self.title)
		self.canvas = Tkinter.Canvas(self.w, bg = "black", 
				height = self.height, width = self.width)
		self.canvas.grid()
	# update - update the progress bar
	# @ratio - progress ratio
	def update(self, ratio):
		self.canvas.delete(self.w)
		self.canvas.create_rectangle(0, 0, 
				ratio * self.width, 
				30 + 2, fill = "green", stipple = "gray75")
		self.w.title(`int(ratio * 100)` + "% " + self.title)
		self.w.update()
	def close(self):
	 	self.w.withdraw()
