import tkinter as tk
import time
import threading
from async_handler import AsyncHandler


class MainWindow:

	def __init__(self, master):
		self.master = master
		self.frame = tk.Frame(self.master)
		self.scale = tk.Scale(
				self.frame, orient=tk.HORIZONTAL, command = AsyncHandler(self.handle_scale))
		self.label = tk.Label(self.frame)
		self.label.pack()
		self.scale.pack()
		self.frame.pack()

	def handle_scale(self, scale):
		time.sleep(0.5)
		print(scale)
		self.label.config(text = str(scale))
