import DigitDrawerModel as ddm

class DigitDrawerViewModel(object):

	def __init__(self):
		self.model = ddm.DigitDrawerModel(10, 40)

	def mouseEvent(self, x, y, eventType):
		if eventType == pygame.MOUSEBUTTONDOWN:
			self.isDrawing = True
		elif eventType == pygame.MOUSEBUTTONUP:
			self.isDrawing = False
			self.model.clearGridChanges()
		elif eventType == pygame.MOUSEMOTION:
			if self.isDrawing == True:


		pass