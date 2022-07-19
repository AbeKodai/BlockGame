import pygame
from random import randint


FPS = 60     # Frame per Second 毎秒のフレーム数

# 定数群
BOX_TOP_X = 100        # ゲーム領域の左上X座標
BOX_TOP_Y = 100        # ゲーム領域の左上Y座標
BOX_WIDTH = 300        # ゲーム領域の幅
BOX_HEIGHT = 300       # ゲーム領域の高さ

DURATION = 0.05        # 描画間隔

RED = (255, 0, 0)
BLUE = (0, 0, 255)

D = 25


# ballは、Spriteを継承している。
class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y, vx, vy):
        super().__init__()
        self.x = x
        self.y = y
        self.vx, self.vy = (vx, vy)
        self.image = pygame.Surface((D, D))
        self.image.fill(RED)
        self.rect = pygame.Rect(self.x, self.y, D, D)
    
    def move(self):
        self.rect.move_ip(self.vx, self.vy)

# Roadは、Spriteを継承している。
class Road(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.x = x
        self.y = y
        self.h = h
        self.w = w
        self.image = pygame.Surface((w, h))
        self.image.fill(BLUE)
        self.rect = pygame.Rect(x, y, w, h)

roadmap =  [[Road(50, 555, 450, 15), Road(50, 490, 350, 15), Road(385, 150, 15, 340), Road(400, 150, 500, 15), Road(485, 215, 415, 15), Road(485, 230, 15, 340), Road(50, 505, 15, 50)],
            [Road(100, 60, 15, 450), Road(115, 60, 685, 15), Road(800, 60, 15, 300), Road(800, 360, 300, 15), Road(165, 125, 15, 385), Road(180, 260, 570, 15), Road(735, 275, 15, 165), Road(750, 425, 350, 15), Road(380, 75, 15, 115), Road(630, 145, 15, 115), Road(115, 495, 50, 15)],
            [Road(60, 470, 420, 15), Road(60, 535, 540, 15), Road(435, 150, 15, 320), Road(450, 150, 350, 15), Road(600, 225, 15, 325), Road(615, 225, 120, 15), Road(720, 240, 15, 325), Road(800, 150, 15, 350), Road(800, 500, 285, 15), Road(1070, 140, 15, 360), Road(720, 565, 430, 15), Road(1135, 140, 15, 425), Road(520, 400, 80, 15), Road(450, 300, 95, 15), Road(60, 485, 15, 50)]            
            ]   #コース3パターン

ball_spawnpoint = [Ball(80, 515, 4, 4), Ball(125, 460, 4, 4), Ball(85, 495, 4, 4)]
#コースごとの自機の出現位置

# ----------------------------------
# Box(ゲーム領域)の定義
class Box:

    def __init__(self, w, h):
        self.width = w
        self.height = h
        

    def set(self):   # 初期設定を一括して行う
        screen = pygame.display.set_mode((1200, 600))
        self.screen = screen
        self.clock = pygame.time.Clock()   # 時計オブジェクト
        self.number = randint(0, 2) #コース決定
        self.ball = ball_spawnpoint[self.number]
        self.font = pygame.font.SysFont(None, 150)
        self.Game_Clear = False
        self.Game_Over = False
        self.in_game = True
        self.exit = False
        self.exit_count = 0
        
        
        
    def animate(self):
        LOOP = True
        while LOOP:  # メインループ
            for event in pygame.event.get():
                # 「閉じる」ボタンを処理する
                if event.type == pygame.QUIT: LOOP = False
            self.clock.tick(FPS)      # 毎秒の呼び出し回数に合わせて遅延
            
            if self.in_game:
                pressed_keys = pygame.key.get_pressed() # キー情報を取得
                if pressed_keys[pygame.K_UP]:    # 上が押されたら
                    self.ball.rect.move_ip(0, -self.ball.vy)   # y 座標を小さく
                if pressed_keys[pygame.K_DOWN]:  # 下が押されたら
                    self.ball.rect.move_ip(0, self.ball.vy)       # y 座標を大きく
                if pressed_keys[pygame.K_RIGHT]:  # 右が押されたら
                    self.ball.rect.move_ip(self.ball.vx, 0)       # x 座標を大きく
                if pressed_keys[pygame.K_LEFT]:  # 左が押されたら
                    self.ball.rect.move_ip(-self.ball.vx, 0)       # x 座標を小さく
                


                self.ball.update()

                self.screen.blit(self.ball.image, self.ball.rect)
                for i in roadmap[self.number]:
                    self.screen.blit(i.image, i.rect)
                
                if self.number == 0:
                    if self.ball.rect.x >= 900:  #ゴール設定
                        self.Game_Clear = True
                        self.in_game = False
                elif self.number == 1:
                    if self.ball.rect.x >= 1100:  #ゴール設定
                        self.Game_Clear = True
                        self.in_game = False
                else:
                    if self.ball.rect.x >= 1070 and self.ball.rect.y <= 140:  #ゴール設定
                        self.Game_Clear = True
                        self.in_game = False
                
                if self.ball.rect.collidelistall(roadmap[self.number]):
                    self.Game_Over = True
                    self.in_game = False

                


            pygame.display.flip()
            self.screen.fill((0, 0, 0))  # 塗潰し：次の flip まで反映されない

            if pressed_keys[pygame.K_a]:
                self.Game_Clear = True
                self.in_game = False

            if self.Game_Clear:
                clear_text = self.font.render("Game Clear!", False, (255, 153, 255))
                self.screen.blit(clear_text, (300, 200))
                self.exit = True
                

            if self.Game_Over:
                false_text = self.font.render("Game Over...", False, (153, 76, 0))
                self.screen.blit(false_text, (300, 200))
                self.exit = True

            if self.exit:
                self.exit_count += 1
                if self.exit_count >= 180:  #テキストを表示して3秒経過したらゲーム終了
                    pygame.quit()


box = Box(BOX_WIDTH, BOX_HEIGHT)
pygame.init()
box.set()       # ゲームの初期設定
box.animate()   # アニメーション
pygame.quit()   # 画面を閉じる