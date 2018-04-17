from abc import ABCMeta, abstractmethod



class Button(object):

	__metaclass__ = ABCMeta

	def __init__(self, x, y, w, h):
		self.x = x
		self.y = y; 
		self.width = w
		self.height = h


	def inBounds(self, x, y):
		return (self.x <= x and x <= self.x + self.width and
		   	   self.y <= y and y <= self.y + self.height)

	@abstractmethod
	def pressed(self, data):
		pass




