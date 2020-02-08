import pygame,math
from pygame.locals import *
from sys import exit

class draw:
	
	def __init__(self,wide,high):
		pygame.init()
		screen = pygame.display.set_mode((wide,high),0,0)
		pygame.display.set_caption("gomoku")
		self.screen = screen
		#按钮字典:值是列表[序号,始坐标,大小,文字,是否显示]
		self.button_dict = {"start":[1,(0,0),(0,0),"新局",1],"undo":[2,(0,0),(0,0),"悔棋",1],"exit":[3,(0,0),(0,0),"退出",1]}

	def draw_board(self,size,seat): #绘制棋盘函数
		x,y = seat
		self.screen.fill((201,202,187))
		#绘制边界线
		pygame.draw.rect(self.screen,(0,0,0),(x-10,y-10,size+20,size+20),3)
		#绘制网格线
		for i in range(15):
			pygame.draw.line(self.screen,(0,0,0),(x,size*i//14+y),(x+size,size*i//14+y),1)
			pygame.draw.line(self.screen,(0,0,0),(size*i//14+x,y+size),(size*i//14+x,y),1)
		#绘制定位点
		for point in [(7,7),(3,3),(11,3),(11,11),(3,11)]:
			pygame.draw.circle(self.screen,(0,0,0),(x+size*point[0]//14,y+size*point[1]//14),round(0.15*size//14),0)
		#绘制棋子
		radius = round(0.382*size//14) #黄金比
		for black in gomoku.black_list:
			position = (x+size*black[0]//14,y+size*black[1]//14)
			pygame.draw.circle(self.screen,(0,0,0),position,radius,0)
		for white in gomoku.white_list:
			position = (x+size*white[0]//14,y+size*white[1]//14)
			pygame.draw.circle(self.screen,(255,255,255),position,radius,0)
			pygame.draw.circle(self.screen,(0,0,0),position,radius,1)
	
	def draw_button(self,seat,size): 
		#draw_button(屏幕对象,显示位置,区域大小)所有按钮被绘制在这一区域内
		x,y = seat
		w,h = size
		button_list = []
		for i in self.button_dict:
			if self.button_dict[i][-1]:
				button_list.append(i)
		#将需要显示的按钮加载到列表中
		button_num = len(button_list)
		s_font = pygame.font.Font("maobi.ttf",h//(button_num*3))
		index = 0
		for j in button_list:
			self.button_dict[j][1:3] = (x+w//4,y+h*index//button_num),(w//2,(h//button_num)//2)
			(a,b),(c,d) = self.button_dict[j][1:3]
			pygame.draw.rect(self.screen,(0,0,0),(a,b,c,d),3)
			self.screen.blit(s_font.render(self.button_dict[j][-2],True,(0,0,0)),(x+w//3,y+h*index//button_num+h//(button_num*10)))
			index += 1

class gomoku:
	
	black_list,white_list = [],[]
	
	def __init__(self,color):
		if color:
			self.color = color
		else:
			self.color = color

	def play(self,pos):
		if self.color:
			gomoku.black_list.append(pos)
		else:
			gomoku.white_list.append(pos)
	
	def win(self,pos):
		#判断位于pos处的棋子是否连成五子
		x,y = pos
		lst1,lst2,lst3,lst4 = [],[],[],[]
		if self.color:
			chessList = gomoku.black_list
		else:
			chessList = gomoku.white_list
		for i in range(9):
			lst1.append((x-4+i,y))
			lst2.append((x-4+i,y-4+i))
			lst3.append((x,y-4+i))
			lst4.append((x+4-i,y-4+i))
		for lst in [lst1,lst2,lst3,lst4]:
			score = 0
			for j in lst:
				if j in chessList:
					score += 1
				else:
					score = 0
				if score == 5:
					return True
		return False
		
	def main(wide=1280,high=720):
		#主函数(窗口尺寸)
		screen = draw(wide,high)
		s_font = pygame.font.Font("maobi.ttf",40)
		color,running = True,True #color为真表示这是黑方，runing为真表示可以落子
		text2 = 0 #高优先级文本
		while True: #主循环
			size,seat = high-40,(20,20)
			player_1,player_2 = gomoku(0),gomoku(1)
			screen.draw_board(size,seat)
			screen.draw_button((high,high//3),(wide-high,high-high//3))
			if text2:
				#优先绘制高优先级文本
				screen.screen.blit(text2,(high+(wide-high)//3,high//6))
			else:
				if color:
					text = s_font.render("黑方落子",True,(0,0,0))
				else:
					text = s_font.render("白方落子",True,(0,0,0))
				screen.screen.blit(text,(high+(wide-high)//3,high//6))
			for event in pygame.event.get():
				if event.type == QUIT:
					exit()
				elif event.type == MOUSEBUTTONDOWN:
					if event.button == 1:
						pos_x,pos_y = event.pos
						x,y = (pos_x-seat[0]+size//28)//(size//14),(pos_y-seat[1]+size//28)//(size//14)
						if (x,y) not in gomoku.black_list and (x,y) not in gomoku.white_list and 0<=x<=14 and 0<=y<=14 and running:
							if color:
								player = player_2
							else:
								player = player_1
							player.play((x,y))
							if player.win((x,y)):
								running = False
								if color:
									text2 = s_font.render("黑方胜利",True,(0,0,0))
								else:
									text2 = s_font.render("白方胜利",True,(0,0,0))
							elif len(gomoku.black_list) + len(gomoku.white_list) == 225:
								#棋盘被下满却没人赢
								text2 = s_font.render("和     棋",True,(0,0,0))
								running = False
							color = not color
						else:
							for i in screen.button_dict:
								button = screen.button_dict[i]
								if button[1][0] <= pos_x <= button[1][0]+button[2][0] and button[1][1] <= pos_y <= button[1][1]+button[2][1] and button[-1]:
									if i == "start":
										gomoku.black_list.clear()
										gomoku.white_list.clear()
										running = True
										color = True
										text2 = 0
									if i == "undo" and running:
										if not color:
											if gomoku.black_list:
												gomoku.black_list.pop()
												color = not color
										else:
											if gomoku.white_list:
												gomoku.white_list.pop()
												color = not color
									if i == "exit":
										exit()
			pygame.display.update()

if __name__ == "__main__":
	gomoku.main(1080,640)