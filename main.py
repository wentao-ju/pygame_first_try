import pygame, sys

def display_score():
    #.get_ticks()返回毫秒值
    current_time = int(pygame.time.get_ticks()/1000) - start_time
    score_surface = score_font.render(f'Score: {current_time}',False,(64,64,64))
    score_rect = score_surface.get_rect(center=(400,50))
    screen.blit(score_surface,score_rect)

    return current_time

pygame.init()  #初始化运行pygame，此函数必须执行
screen = pygame.display.set_mode((800,400))  #创建游戏窗口
pygame.display.set_caption('Pygame Tutorial')  #窗口名
clock = pygame.time.Clock()  #时间

#.Font(自定义字体路径, 字体大小)
score_font = pygame.font.Font('font/Pixeltype.ttf', 50)  #设置字体

game_active = False  #游戏状态
start_time = 0
score = 0

#.convert()转换图片格式到更好匹配Pygame的层面
sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()
#.render(text, 是否让字体平滑, color)
#文本层面
# score_surface = score_font.render('My Game', False, (64,64,64)).convert()
# score_rect = score_surface.get_rect(center=(400,50))
#.convert_alpha()转换图片格式并消除周边白背景
snail_surface = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_rect = snail_surface.get_rect(bottomleft=(800,300))  #给snail确定边框

player_surface = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_rect = player_surface.get_rect(midbottom=(80,300))  #给人物确定边框
player_gravity = 0

#intro screen
player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand= pygame.transform.rotozoom(player_stand,0,2)  #rescaled the surface
player_stand_rect = player_stand.get_rect(center=(400,200))

#game title
game_name = score_font.render('Pixel Runner',False,(111,196,169))
game_name_rect = game_name.get_rect(center=(400,80))
game_message = score_font.render('Press space to run',False,(111,196,169))
game_message_rect = game_message.get_rect(center=(400,330))

while True:  #保持游戏始终运行
    for event in pygame.event.get():  #获取玩家操作
        if event.type == pygame.QUIT:  #如果用户执行退出操作
            pygame.quit()  #则执行退出pygame
            sys.exit()  #退出整个程序
        
        if game_active:
            #检查是否有键盘键被按下或抬起
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if player_rect.bottom == 300:
                        player_gravity = -18  #实现人物跳跃
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True  #如果game over，按空格键重新开始
                snail_rect.left = 800  #初始化snail的位置
                start_time = int(pygame.time.get_ticks()/1000)  #分数归零

    if game_active:
        #层面是可按加载顺序向上叠加的
        screen.blit(sky_surface,(0,0))  #让层面展现到窗口中,左上角为origin
        screen.blit(ground_surface,(0,300))
        #对指定区域画图案
        # pygame.draw.rect(screen,'#c0e8ec',score_rect)
        # pygame.draw.rect(screen,'#c0e8ec',score_rect,10)
        score = display_score()

        #怪物
        snail_rect.left -= 4  #让snail向左以每秒3个pixel的距离移动
        if snail_rect.right < -100:
            snail_rect.left = 800
        screen.blit(snail_surface,snail_rect)

        #玩家
        player_gravity += 0.8
        player_rect.y += player_gravity  #实现人物下落
        if player_rect.bottom >= 300:  #让人物停落在地面上
            player_rect.bottom = 300
        screen.blit(player_surface,player_rect)

        #game over state
        if snail_rect.colliderect(player_rect):
            game_active = False
    else:  #if game over
        screen.fill((94,129,162))
        screen.blit(player_stand,player_stand_rect)
        score_message = score_font.render(f'Your score: {score}',False,(111,196,169))
        score_message_rect = score_message.get_rect(center=(400,330))
        screen.blit(game_name,game_name_rect)
        if score == 0:
            screen.blit(game_message,game_message_rect)
        else:
            screen.blit (score_message,score_message_rect)

    pygame.display.update()  #更新display窗口
    clock.tick(60)  #让While循环一次不超过60帧每秒，同于fps上限
