
import pygame
from pygame.locals import *
pygame.init()
import cv2
import mediapipe as mp

mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
screen_width = 600
screen_height = 600
cap.set(3, screen_width)
cap.set(4, screen_height)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Breakout')

font = pygame.font.SysFont('Impact', 40)

bg = (2,29,92)

block_1 = (78, 78, 78)
block_2 = (152, 152, 152)
block_3 = (225, 225, 225)

paddle_col = (255, 255, 255)
paddle_outline = (0,0,0)

text_col = (255,199,11)




cols = 6
rows = 6
clock = pygame.time.Clock()
fps = 60
live_ball = False
game_over = 0


def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))


class wall():
	def __init__(self):
		self.width = screen_width // cols
		self.height = 50

	def create_wall(self):
		self.blocks = []
		block_individual = []
		for row in range(rows):
			block_row = []
			for col in range(cols):
				block_x = col * self.width
				block_y = row * self.height
				rect = pygame.Rect(block_x, block_y, self.width, self.height)
				if row < 2:
					strength = 3
				elif row < 4:
					strength = 2
				elif row < 6:
					strength = 1
				block_individual = [rect, strength]
				block_row.append(block_individual)
			self.blocks.append(block_row)


	def draw_wall(self):
		for row in self.blocks:
			for block in row:
				if block[1] == 3:
					block_col = block_1
				elif block[1] == 2:
					block_col = block_2
				elif block[1] == 1:
					block_col = block_3
				pygame.draw.rect(screen, block_col, block[0])
				pygame.draw.rect(screen, bg, (block[0]), 2)



class paddle():
	def __init__(self):
		self.reset()

	def move(self, lip_x):
		self.rect.x = lip_x - (self.width // 2)
			
		if self.rect.left < 0:
			self.rect.left = 0	

		if self.rect.right > screen_width : 
			self.rect.right = screen_width


	def draw(self):
		pygame.draw.rect(screen, paddle_col, self.rect)
		pygame.draw.rect(screen, paddle_outline, self.rect, 3)


	def reset(self):
		self.height = 20
		self.width = int(screen_width / cols)
		self.x = int((screen_width / 2) - (self.width / 2))
		self.y = screen_height - (self.height * 2)
		self.speed = 10
		self.rect = Rect(self.x, self.y, self.width, self.height)
		self.direction = 0


class game_ball():
	def __init__(self, x, y):
		self.reset(x, y)


	def move(self):

		collision_thresh = 5

		wall_destroyed = 1
		row_count = 0
		for row in wall.blocks:
			item_count = 0
			for item in row:
				if self.rect.colliderect(item[0]):
					if abs(self.rect.bottom - item[0].top) < collision_thresh and self.speed_y > 0:
						self.speed_y *= -1
					if abs(self.rect.top - item[0].bottom) < collision_thresh and self.speed_y < 0:
						self.speed_y *= -1						
					if abs(self.rect.right - item[0].left) < collision_thresh and self.speed_x > 0:
						self.speed_x *= -1
					if abs(self.rect.left - item[0].right) < collision_thresh and self.speed_x < 0:
						self.speed_x *= -1
					if wall.blocks[row_count][item_count][1] > 1:
						wall.blocks[row_count][item_count][1] -= 1
					else:
						wall.blocks[row_count][item_count][0] = (0, 0, 0, 0)

				if wall.blocks[row_count][item_count][0] != (0, 0, 0, 0):
					wall_destroyed = 0
				item_count += 1
			row_count += 1
		if wall_destroyed == 1:
			self.game_over = 1



		if self.rect.left < 0 or self.rect.right > screen_width:
			self.speed_x *= -1

		if self.rect.top < 0:
			self.speed_y *= -1
		if self.rect.bottom > screen_height:
			self.game_over = -1


		if self.rect.colliderect(player_paddle):
			if abs(self.rect.bottom - player_paddle.rect.top) < collision_thresh and self.speed_y > 0:
				self.speed_y *= -1
				self.speed_x += player_paddle.direction
				if self.speed_x > self.speed_max:
					self.speed_x = self.speed_max
				elif self.speed_x < 0 and self.speed_x < -self.speed_max:
					self.speed_x = -self.speed_max
			else:
				self.speed_x *= -1



		self.rect.x += self.speed_x
		self.rect.y += self.speed_y

		return self.game_over


	def draw(self):
		pygame.draw.circle(screen, paddle_col, (self.rect.x + self.ball_rad, self.rect.y + self.ball_rad), self.ball_rad)
		pygame.draw.circle(screen, paddle_outline, (self.rect.x + self.ball_rad, self.rect.y + self.ball_rad), self.ball_rad, 3)



	def reset(self, x, y):
		self.ball_rad = 10
		self.x = x - self.ball_rad
		self.y = y
		self.rect = Rect(self.x, self.y, self.ball_rad * 2, self.ball_rad * 2)
		self.speed_x = 4
		self.speed_y = -4
		self.speed_max = 5
		self.game_over = 0



wall = wall()
wall.create_wall()

player_paddle = paddle()


ball = game_ball(player_paddle.x + (player_paddle.width // 2), player_paddle.y - player_paddle.height)

run = True
with mp_face_detection.FaceDetection(min_detection_confidence=0.5) as face_detection:
    while run:
        clock.tick(fps)
        screen.fill(bg)

        wall.draw_wall()
        player_paddle.draw()
        ball.draw()
        
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break
        
            
        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
        results = face_detection.process(frame_rgb)
        
        lips_x = screen_width // 2
        if results.detections:
            for detection in results.detections:
                bboxC = detection.location_data.relative_bounding_box
                h, w, c = frame.shape
                x_min = int(bboxC.xmin * w)
                y_min = int(bboxC.ymin * h)
                box_width = int(bboxC.width * w)
                box_height = int(bboxC.height * h)
                cv2.rectangle(frame, (x_min, y_min), (x_min + box_width, y_min + box_height), (0, 255, 0), 2)

                keypoints = detection.location_data.relative_keypoints
                
                lips = keypoints[3]  
                lips_x = int(lips.x * frame.shape[1])
                lips_y = int(lips.y * frame.shape[0])
                
                cv2.circle(frame, (lips_x, lips_y), 10, (0, 0, 255), -1)
                
                coord_text = f"({lips_x}, {lips_y})"
                cv2.putText(frame, coord_text, (lips_x + 20, lips_y - 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                break
        
        cv2.imshow("Face and Nose Detection", frame)
        

        if live_ball:
            player_paddle.move(lips_x//2.5)
            game_over = ball.move()
            if game_over != 0:
                live_ball = False


        if not live_ball:
            if game_over == 0:
                draw_text('CLICK ANYWHERE TO START', font, text_col, 100, screen_height // 2 + 100)
            elif game_over == 1:
                draw_text('WOW YOU REALLY WON !!!', font, text_col, 170, screen_height // 2 + 50)
                draw_text('CLICK ANYWHERE TO START', font, (255,158,11), 100, screen_height // 2 + 100)
            elif game_over == -1:
                draw_text('GAME OVER ', font, text_col, 220, screen_height // 2 + 50)
                draw_text('CLICK ANYWHERE TO START', font, (255,158,11), 100, screen_height // 2 + 100)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and live_ball == False:
                live_ball = True
                ball.reset(player_paddle.x + (player_paddle.width // 2), player_paddle.y - player_paddle.height)
                player_paddle.reset()
                wall.create_wall()



        pygame.display.update()

pygame.quit()