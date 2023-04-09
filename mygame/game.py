import pygame
import os

pygame.init() # 초기화 (반드시 필요)

#화면 크기 설정
screen_width = 700
screen_height = 480
screen = pygame.display.set_mode((screen_width,screen_height))
 
#화면 타이틀 설정
pygame.display.set_caption("내가 처음 기획한 게임") # 게임 이름

#FPS
clock = pygame.time.Clock()

################################################################################

# 1. 사용자 게임 초기화 (배경 화면, 게임 이미지, 좌표, 폰트, 속도 등)
background = pygame.image.load("C:\\coding\\mygame\\images\\background.png")

character = pygame.image.load("C:\\coding\\mygame\\images\\character.png")
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_pos_x = (screen_width /2) - (character_width /2)
character_pos_y = screen_height - character_height
character_to_x = 0
character_to_y = 0
character_speed = 0.2
character_jump = 1

monster_images = [
    pygame.image.load("C:\\coding\\mygame\\images\\monster1.png"),
    pygame.image.load("C:\\coding\\mygame\\images\\monster2.png"),
    pygame.image.load("C:\\coding\\mygame\\images\\monster3.png")]

monster_speed_x = [3, 5, 7]

monsters = []

monsters.append({
    "pos_x" : 40,
    "pos_y" : screen_height, #임시
    "to_x" : monster_speed_x[0],
    "img_idx" : 0})


game_font = pygame.font.Font(None, 40)
total_time = 60
start_tick = pygame.time.get_ticks()


running = True
while running:
    dt = clock.tick(60) # 게임화면의 초당 프레임 수를 설정

    # 2. 이벤트 처리 (키보드, 마우스 등)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            running = False 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                character_to_x -= character_speed
            if event.key == pygame.K_RIGHT:
                character_to_x += character_speed
            if event.key == pygame.K_SPACE:
                # 스페이스바가 눌리면 캐릭터가 위로 올라가도록 설정
                character_to_y -= character_jump
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                character_to_x = 0
            if event.key == pygame.K_SPACE:
                character_to_y = 0.3  # 중력의 원리



    character_pos_x += character_to_x * dt
    character_pos_y += character_to_y * dt

    if character_pos_x < 0:
        character_pos_x = 0
    if character_pos_x > screen_width - character_width:
        character_pos_x = screen_width - character_width
    if character_pos_y < 0:
        character_pos_y = 0
    if character_pos_y > screen_height - character_height:
        character_pos_y = screen_height - character_height

    # 몬스터드들 정의
    for monster_idx, monster_val in enumerate(monsters):
        monster_pos_x = monster_val["pos_x"]
        monster_pos_y = monster_val["pos_y"]
        monster_img_idx = monster_val["img_idx"]

        monster_size = monster_images[monster_img_idx].get_rect().size
        monster_width = monster_size[0]
        monster_height = monster_size[1]

        monster_rect = monster_images[monster_img_idx].get_rect()
        monster_rect.left = monster_pos_x
        monster_rect.top = monster_pos_y

        if monster_pos_x < 0 or monster_pos_x > screen_width - monster_width:
            monster_val["to_x"] = monster_val["to_x"] * -1
           
        monster_val["pos_x"] += monster_val["to_x"]


    # 타이머 설정
    elapsed_time = int((pygame.time.get_ticks() - start_tick) / 1000)
    timer = game_font.render("{}".format(int(total_time - elapsed_time)), True, (255, 255, 255))


    # 시간이 지남에 따라 몬스터 추가하기
    # if elapsed_time == 5 and monster_img_idx < len(monster_images) - 1:

    #     monster_width = monster_rect.size[0]
    #     monster_height = monster_rect.size[1]


    #     next_monster_rect = monster_images[monster_img_idx + 1].get_rect().size
    #     next_monster_width = next_monster_rect[0]
    #     next_monster_height = next_monster_rect [1]

    #     monsters.append({
    #         "pos_x" : 40,
    #         "pos_y" : screen_height - next_monster_height, #임시
    #         "to_x" : monster_speed_x[0] + 1 ,
    #         "img_idx" : monster_img_idx + 1
    #     })


    # 3. 게임 캐릭터 위치 정의 
    
    # 4. 충돌 처리

    # 5. 화면에 그리기
    screen.blit(background, (0, 0))
    screen.blit(character, (character_pos_x, character_pos_y))

    for idx, val in enumerate(monsters):
        monster_pos_x = val["pos_x"]
        monster_pos_y = val["pos_y"]
        screen.blit(monster_images[monster_img_idx],(monster_pos_x, monster_pos_y - monster_height))

    screen.blit(timer, (10,10))




    pygame.display.update() # 게임화면을 다시 그리기

# 잠시 대기 코드
pygame.time.delay(2000) # 2초 정도 대기

# pygame 종료
pygame.quit()   