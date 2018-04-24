import pygame


class util(object):
	def centerText(font, text, x, y):
		width, height = font.size(text)
		x0 = x - width // 2
		y0 = y - height // 2
		return (x0, y0)

	def row2Y(row, frame):
		return frame.y + row * frame.scale
	def col2X(col, frame):
		return frame.x + col * frame.scale
	def x2Col(x, frame):
		return (x - frame.x) // frame.scale
	def y2Row(y, frame):
		return (y - frame.y) // frame.scale



	def drawTextRect(frame, rect, font, text, rColor, tColor):
		(x, y, width, height) = rect
		pygame.draw.rect(frame.screen, rColor, rect, 0);
		cx = (x + x + width) // 2  #error with median
		cy = (y + y + height) // 2
		(tx, ty) = util.centerText(font, text, cx, cy)
		#print("X: %d, y: %d, tx: %d, ty: %d, cx: %d, cy: %d"%(x,y,tx,ty,cx,cy))
		frame.screen.blit(font.render(text, True, tColor), (tx, ty))