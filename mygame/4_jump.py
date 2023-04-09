import pygame
import os
import keyboard

pygame.init() # 초기화 (반드시 필요)

# 조건 모음

monster_added = False
not_appear_3 = True
three_added = False
jump_condition = True


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
character_speed = 0.025
character_jump = 1
jump_height = 10
jump_speed = 5
jump_count = jump_height

monster_images = [
    pygame.image.load("C:\\coding\\mygame\\images\\monster1.png"),
    pygame.image.load("C:\\coding\\mygame\\images\\monster2.png"),
    pygame.image.load("C:\\coding\\mygame\\images\\monster3.png")]

first_monster_rect = monster_images[0].get_rect().size
frist_monster_height = first_monster_rect[1]


monster_speed_x = [3, 5]

monster_appear = [40,60,80]

init_spd_y = -13

monsters = []

monsters.append({
    "pos_x" : monster_appear[0],
    "pos_y" : screen_height - frist_monster_height,
    "to_x" : monster_speed_x[0],
    "img_idx" : 0,
    "to_y":0})


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
                character_to_x -= character_speed * dt
            if event.key == pygame.K_RIGHT:
                character_to_x += character_speed * dt
            # 스페이스바가 눌리면 캐릭터가 위로 올라가도록 설정
            if keyboard.is_pressed("space"):
                character_to_y -= character_jump
                jump_condition = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                character_to_x = 0
            if event.key == pygame.K_SPACE:
                character_to_y = 0.15  # 중력의 원리
        
    if jump_condition:
        if jump_count >= -jump_height:
            character_pos_y -= (jump_count * abs(jump_count)) * 0.2
            jump_count -= jump_speed
        else:
            jump_count = jump_height
            jump_condition = False



    character_pos_x += character_to_x * dt
    character_pos_y += character_to_y * dt
    # 땅에 닿으면 다시 점프 가능

    if character_pos_x < 0:
        character_pos_x = 0
    if character_pos_x > screen_width - character_width:
        character_pos_x = screen_width - character_width
    if character_pos_y < 0:
        character_pos_y = 0
    if character_pos_y > screen_height - character_height:
        character_pos_y = screen_height - character_height

    # 타이머 설정
    elapsed_time = int((pygame.time.get_ticks() - start_tick) / 1000)
    timer = game_font.render("{}".format(int(total_time - elapsed_time)), True, (255, 255, 255))

    # 몬스터드들 정의
    for monster_idx, monster_val in enumerate(monsters):

        monster_pos_x = monster_val["pos_x"]
        monster_pos_y = monster_val["pos_y"]
        monster_img_idx = monster_val["img_idx"]
        
        monster_size = monster_images[monster_img_idx].get_rect().size
        monster_width = monster_size[0]
        monster_height = monster_size[1]


        # 몬스터위 위치 교정하기
        

        if monster_pos_x < 0 or monster_pos_x > screen_width - monster_width:
            monster_val["to_x"] = monster_val["to_x"] * -1
           
        monster_val["pos_x"] += monster_val["to_x"]
        


    if elapsed_time == 5 and monster_added  == False: # 5초라는 시간동안 한번만 입력해주는 변수
        
        second_monster_rect = monster_images[monster_img_idx + 1].get_rect().size
        second_monster_width = second_monster_rect[0]
        second_monster_height = second_monster_rect[1]

        monsters.append({
            "img_idx": monster_img_idx + 1,
            "pos_x" : monster_appear[monster_img_idx + 1],
            "pos_y": screen_height - second_monster_height,
            "to_x" : monster_speed_x[monster_img_idx + 1],
            "to_y": 0})
        monster_added = True




    if elapsed_time == 10 and monster_added == True: # 해당 조건에 monster_added를 쓰면 오류가 뜸
        three_monster_rect = monster_images[monster_img_idx + 1].get_rect().size                   
        three_monster_width = three_monster_rect[0]
        three_monster_height = three_monster_rect[1]

        monsters.append({
            "img_idx": monster_img_idx + 1,
            "pos_x" : monster_appear[monster_img_idx + 1],
            "pos_y": screen_height - three_monster_height,
            "to_x" : monster_speed_x[monster_img_idx],
            "to_y": -6})
        monster_added = False
        not_appear_3 = False

    if not_appear_3 == False:
        for idx, val in enumerate(monsters):
            if val["img_idx"] == 2: # 3번째 몬스터만 해당
                if monster_pos_y >= screen_height - three_monster_height:
                    val["to_y"] = init_spd_y
                else:
                    val["to_y"] += 0.35

                val["pos_y"] += val["to_y"]

    # 3. 게임 캐릭터 위치 정의 
    
    # 4. 충돌 처리
    character_rect = character.get_rect()
    character_rect.left = character_pos_x
    character_rect.top = character_pos_y

    for monster_idx, monster_val in enumerate(monsters):
        monster_pos_x = monster_val["pos_x"]
        monster_pos_y = monster_val["pos_y"]
        monster_img_idx = monster_val["img_idx"]

        monster_rect = monster_images[monster_img_idx].get_rect()
        monster_rect.left = monster_pos_x
        monster_rect.top = monster_pos_y
        # 캐릭터와 몬스터 충돌 감지
        if character_rect.colliderect(monster_rect):
            running = False
            break

    # 5. 화면에 그리기
    screen.blit(background, (0, 0))
    screen.blit(character, (character_pos_x, character_pos_y))

    for idx, val in enumerate(monsters):
        monster_pos_x = val["pos_x"]
        monster_pos_y = val["pos_y"]
        monster_img_idx = val["img_idx"]
        screen.blit(monster_images[monster_img_idx],(monster_pos_x, monster_pos_y)) # 나중에 추가해야할 것 

    screen.blit(timer, (10,10))
    



    pygame.display.update() # 게임화면을 다시 그리기

# 잠시 대기 코드
pygame.time.delay(2000) # 2초 정도 대기

# pygame 종료
pygame.quit()   