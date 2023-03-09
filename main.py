import pygame, sys

pygame.init()  #初始化运行pygame，此函数必须执行
screen = pygame.display.set_mode((800,400))  #创建游戏窗口
pygame.display.set_caption('Pygame Tutorial')  #窗口名
clock = pygame.time.Clock()  #时间

#.Font(自定义字体路径, 字体大小)
score_font = pygame.font.Font('font/Pixeltype.ttf', 50)  #设置字体

#test_surface = pygame.Surface((100,200))  #创建层面
#test_surface.fill('Red')  #层面填充色

#.convert()转换图片格式到更好匹配Pygame的层面
sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()
#.render(text, 是否让字体平滑, color)
#文本层面
score_surface = score_font.render('My Game', False, 'black').convert()
score_rect = score_surface.get_rect(center=(400,50))
#.convert_alpha()转换图片格式并消除周边白背景
snail_surface = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_rect = snail_surface.get_rect(bottomleft=(800,300))  #给snail确定边框

player_surface = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_rect = player_surface.get_rect(midbottom=(80,300))  #给人物确定边框

while True:  #保持游戏始终运行
    for event in pygame.event.get():  #获取玩家操作
        if event.type == pygame.QUIT:  #如果用户执行退出操作
            pygame.quit()  #则执行退出pygame
            sys.exit()  #退出整个程序
        # if event.type == pygame.MOUSEMOTION:  #在event loop中对鼠标的属性获取
        #     if player_rect.collidepoint(event.type):
        #         print('collision')

    #层面是可按加载顺序向上叠加的
    screen.blit(sky_surface,(0,0))  #让层面展现到窗口中,左上角为origin
    screen.blit(ground_surface,(0,300))
    screen.blit(score_surface,score_rect)
    snail_rect.left -= 3  #让snail向左以每秒3个pixel的距离移动
    if snail_rect.right < -100:
        snail_rect.left = 800
    screen.blit(snail_surface,snail_rect)
    player_rect.left += 1
    screen.blit(player_surface,player_rect)

    # if player_rect.colliderect(snail_rect):  #边框碰撞检测，返回值0或1
    #     print('collision')

    # mouse_position = pygame.mouse.get_pos()  #获取鼠标指针位置
    # if player_rect.collidepoint(mouse_position):  #指针碰撞检测
    #     print('collision')
    # mouse_click = pygame.mouse.get_pressed()  #获取鼠标键是否被按

    pygame.display.update()  #更新display窗口
    clock.tick(60)  #让While循环一次不超过60帧每秒，同于fps上限
