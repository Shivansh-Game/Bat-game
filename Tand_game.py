import pygame
import random
from player import Player
from enemy import Enemy
from sky import Sky
from particle import Particles
from perks import Perks 

#initialisation
particle = Particles()
sky = Sky(1)
pygame.init()
perks = Perks()

#display info
infoObject = pygame.display.Info()
screen_width, screen_height = infoObject.current_w, infoObject.current_h
WIDTH, HEIGHT = screen_width, screen_height



#loading go BRRRRR
BG_menu = pygame.image.load("Shivansh Python\Files/background.jpg").convert_alpha()
BG_menu = pygame.transform.scale(BG_menu,(WIDTH, HEIGHT))

font_menu = pygame.font.Font('Shivansh Python\Files/Mossy.ttf', 80)

pygame.mixer.music.load("Shivansh Python\Files/Main_menu_ost.wav")
pygame.mixer.music.play(-1, 0, 300)

BG = pygame.image.load("Shivansh Python\Files/Floor.png").convert_alpha()
BG = pygame.transform.scale(BG, (screen_width, 50))

font = pygame.font.Font("Shivansh Python\Files\\m5x7.ttf", 36)
pause_font = pygame.font.Font("Shivansh Python\Files\\m5x7.ttf", 108)

#init in different position because pygame was being funky about it
pygame.mixer.init()

#setting up the window
WIN = pygame.display.set_mode((WIDTH, HEIGHT))


#Menu stuff
surface = pygame.Surface((WIDTH, HEIGHT))

#Paused buttons
quit_button_surface = pygame.Surface((400,100))
quit_button_surface.set_alpha(50)

options_button_surface = pygame.Surface((400,100))
options_button_surface.set_alpha(50)

resume_button_surface = pygame.Surface((400,100))
resume_button_surface.set_alpha(50)

#options buttons
back_button_surface = pygame.Surface((400,100))
back_button_surface.set_alpha(50)

text_button_surface = pygame.Surface((1200,100))
text_button_surface.set_alpha(50)

#setting caption
pygame.display.set_caption("The Jungle Thingy")

#level_width
level_width = 3



def draw(player, enemies, camera_offset, fps_text, wave_text, paused, 
         in_selection, in_options, in_menu, direction_inst, position, 
         level_text, xp_text, last_atk_type, Game_over
         ):

    #game draw
    if not in_menu and not Game_over:
        sky.sky_gen()

        for i in range(level_width):        
            WIN.blit(BG, (WIDTH * i + camera_offset[0], HEIGHT - 50 + camera_offset[1])) 
        for enemy in enemies:
            enemy.draw(camera_offset)
        hp_text = font.render(f"HP: {player.hp}", True, "white")
        player.draw(camera_offset, direction_inst)
        WIN.blit(hp_text, (player.rect.x - hp_text.get_width()//2 + player.width//2 + camera_offset[0], player.rect.y - 20))
        WIN.blit(wave_text, (WIDTH//2 - wave_text.get_width()//2, 10))
        WIN.blit(fps_text, (10, 10))
        WIN.blit(level_text, (10, 30))
        WIN.blit(xp_text, (10, 50))
        particle.jump(player, camera_offset)

        
        for enemy in enemies:
            if enemy.i_frames < 6 and len(player.slash_rect_list) > 0 and last_atk_type:
                particle.hit(position, direction_inst, camera_offset, player.scale)
        


        
    if in_selection and not Game_over:
        surface.fill((0,0,0))
        surface.set_alpha(100)
        perks.draw()


    #pause menu
    if paused and not in_selection and not in_options and not Game_over:

        quit_text = pause_font.render(f"Quit", True, "white")
        options_text = pause_font.render(f"Options", True, "white")
        resume_text = pause_font.render(f"Resume", True, "white")
        WIN.blit(quit_button_surface, (WIDTH//2 - 200, HEIGHT - 400))
        WIN.blit(options_button_surface, (WIDTH//2 - 200, HEIGHT - 525))
        WIN.blit(resume_button_surface, (WIDTH//2 - 200, HEIGHT - 650))
        surface.fill((0,0,0))
        surface.set_alpha(100)
        WIN.blit(surface, (0,0))
        WIN.blit(quit_text, (WIDTH//2 - quit_text.get_width()//2 , HEIGHT - 400))
        WIN.blit(options_text, (WIDTH//2 - options_text.get_width()//2 , HEIGHT - 525))
        WIN.blit(resume_text, (WIDTH//2 - resume_text.get_width()//2 , HEIGHT - 650))


    #empty mind
    if in_options and not Game_over:
        back_text = pause_font.render(f"Back <", True, "white")
        text_text = pause_font.render(f"Shit's as empty as your mind", True, "white")
        WIN.blit(back_button_surface, (WIDTH//2 - 200, HEIGHT - 250))
        WIN.blit(back_text, (WIDTH//2 - back_text.get_width()//2 , HEIGHT - 250))
        WIN.blit(text_button_surface, (WIDTH//2 - 600, HEIGHT - 650))
        WIN.blit(text_text, (WIDTH//2 - text_text.get_width()//2 , HEIGHT - 650))

    #starting screen
    if in_menu and not Game_over:

        WIN.blit(BG_menu, (0,0))
        text = font_menu.render('CLICK    TO    START', True, "black")
        textRect = text.get_rect()
        textRect.center = (WIDTH// 2,HEIGHT // 2)
        WIN.blit(text, textRect)

    if Game_over:
        WIN.fill((0,0,0))
        dead_text = pause_font.render(f"Imagine Dying Click to redeem \n yourself and make your \n parents think you aren't a failure \n (I am not responsible if your \n parents keep thinking you are \n a failure)", True, "white")
        deadRect = dead_text.get_rect()  
        deadRect.center = (WIDTH// 2,HEIGHT // 2)
        WIN.blit(dead_text, deadRect)

    pygame.display.update()



def main():
    clock = pygame.time.Clock()
    player = Player(100, 74, 7, 1, 500, WIDTH//2, HEIGHT - 50)
    enemies = [] 
    camera_offset = [0,0]
    wave_no = 1
    level_length = WIDTH * level_width
    floor = pygame.FRect(0, HEIGHT - 50, level_length, 50) #might need later
    Enemy.spawn(Enemy, enemies, wave_no, level_length)
    gigantified = False
    counter_gigatification = 0
    jump_counter = 0
    paused = False
    in_selection = False
   
    fps = None

    running = True
    camera_offset[1] = 0
 
    in_options = False
    on_back = False
    in_menu = True
    wave_text = None
    on_quit = False
    on_options = False
    on_resume = False
    fps_text = None
    x,y = None,None
    x_add, y_add = 0,0
    direction_inst = None
    direction_list = []
    level_text, xp_text = None, None
    Game_over = False
    
    position = []
    level_up_frame = False
    on_perk_1, on_perk_2, on_perk_3 = False, False, False
    last_atk_type = None #if false then melee else slash
    hp_last = player.hp

    #if adding in new things here make sure to implement them in the game over thingy

    

    while running:

        #Tick setting
        clock.tick(60)

        #checking for events (pausing, clicks and etc)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.MOUSEBUTTONDOWN and on_quit):
                running = False
                break
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_ESCAPE] and not in_selection:
                    paused = not paused
            if event.type == pygame.MOUSEBUTTONDOWN and on_options:
                in_options = True
                on_options = False
            if event.type == pygame.MOUSEBUTTONDOWN and (on_back and in_options):
                in_options = False
                on_back = False
            if event.type == pygame.MOUSEBUTTONDOWN and on_resume:
                paused = not paused
                on_resume = False
            if event.type == pygame.MOUSEBUTTONDOWN and in_selection:
                perks.selected(on_perk_1, on_perk_2, on_perk_3)
                if on_perk_1 or on_perk_2 or on_perk_3:
                    perks.apply(player, gigantified)
                    in_selection = False
            if event.type == pygame.MOUSEBUTTONDOWN and Game_over:
                Game_over = False
            if event.type == pygame.MOUSEBUTTONDOWN and in_menu and not Game_over:
                in_menu = False
                pygame.mixer.music.fadeout(500)

        
        #main game logic    
        if not paused and not in_options and not in_menu and not in_selection and not Game_over:

            if hp_last > player.hp:
                player.hurt_sound.play()
            hp_last = player.hp
            

            if level_up_frame:
                player.Level_up_sound.play()
                level_up_frame = False
                perks.select()
                in_selection = True

            #making commonly used variables
            fps = int(clock.get_fps())
            keys = pygame.key.get_pressed()

            #counters
            player.attack_delay -= 1
            if not player.is_jumping:
                jump_counter += 1

            #make the FPS text
            fps_text = font.render(f"FPS: {fps}", True, 'white')
            wave_text = font.render(f"Wave Number: {wave_no}", True, "white")


            #Camera offset logic
            if player.rect.x > WIDTH//2 and player.rect.x <= level_length - (WIDTH//2):
                camera_offset[0] = -player.rect.x + WIDTH // 2

            #updates the star position to avoid having to blit stars across the entire level length
            if player.walking and player.rect.x > WIDTH//2 and not (player.walking and player.rect.x >= level_length - (WIDTH//2)):
                sky.update_stars_position(player.velocity, player.facing)

            #movement
            player.move(keys, level_length)
            player.sound_walk()
                
            if keys[pygame.K_SPACE] and jump_counter > 10:
                player.is_jumping = True
                jump_counter = 0

            player.jump()

            #gigantification 
            if keys[pygame.K_f] and not gigantified and counter_gigatification < 0 and player.jump_finished:
                player.scale = 2
                level_temp = player.level
                xp_temp = player.xp
                player = Player(player.width,player.height,player.velocity, player.scale, player.hp, player.x, player.y + player.height)
                gigantified = True
                perks.apply(player, gigantified)
                player.xp = xp_temp
                player.level = level_temp

            if gigantified:
                if counter_gigatification <= 0:
                    counter_gigatification = 0
                counter_gigatification += 1
                if counter_gigatification >= player.giant_form_time and player.jump_finished:
                    level_temp = player.level
                    xp_temp = player.xp
                    player = Player(player.width / player.scale,player.height / player.scale,player.velocity / player.scale, player.scale / player.scale, player.hp, player.x, player.y + player.height)
                    gigantified = False
                    perks.apply(player, gigantified)
                    player.xp = xp_temp
                    player.level = level_temp
            else:
                counter_gigatification -= 0.5 * player.giant_form_time/1200


            #attacking logic
            if keys[pygame.K_q] or not player.shoot_animation_finished:
                if player.attack_delay <= 0 or not player.shoot_animation_finished:
                    player.shoot()
                    last_atk_type = False

            if keys[pygame.K_r] and len(player.slash_rect_list) < player.max_slash_no or not player.attack_animation_finished:
                if player.attack_delay <= 0 or not player.attack_animation_finished:
                    
                    player.Big_attack()
                    last_atk_type = True
                    if player.attack_delay == player.Big_attack_delay:
                        direction_inst = player.facing
                        particle.hit_particles = []
                        particle.time_alive = 60

            rect_to_remove = []
                        
            #Slash formation (Made me wanna kms 15 times)
            for slash_rect in player.slash_rect_list:
                direction_list.append(direction_inst)
                if slash_rect.x < 0 - camera_offset[0] or slash_rect.x > WIDTH - camera_offset[0]: #camera_offset is negative 
                    direction_list.remove(direction_list[player.slash_rect_list.index(slash_rect)])
                    rect_to_remove.append(slash_rect)
                    continue


                x_add = player.slash_speed 
                y_add = 0


                if direction_inst:
                    slash_rect.x += x_add 
                else:
                    slash_rect.x -= x_add

                slash_rect.y += y_add

            for remove in rect_to_remove:
                player.slash_rect_list.remove(remove)


            if not (keys[pygame.K_q] and player.attack_delay <= 0) and player.shoot_animation_finished:
                player.attack_sprite = None

            #player's invincibility logic

            if player.i_frames < 6: 
                player.i_frames += 0.25
            if player.hp <= 0:
                Game_over = True

            #enemy logic
            for enemy in enemies:

                #enemy attacks
                if not player.attacking and player.i_frames >= 6:
                    if player.rect.colliderect(enemy.rect):
                        player.hp -= 50
                        player.i_frames = 0

                
                #enemy invincibility logic
                if enemy.i_frames < 6:
                    enemy.i_frames += 1
                
                #Enemy direction setting
                if player.rect.x <= enemy.rect.x:
                    enemy.facing = False
                else:
                    enemy.facing = True

                #move the mf 
                enemy.move(player.rect.y, player.height, level_length, player.rect.x)

                #slash collision detection
                for slash in player.slash_rect_list:
                    if slash.colliderect(enemy.rect) and enemy.i_frames == 6:
                        player.DOT_check(enemy, last_atk_type)
                        enemy.hit = True    
                        enemy.hp -= player.Big_attack_dmg
                        enemy.i_frames = 0
                        position = []
                        particle.hit_particles = []
                        particle.time_alive = 60
                        position.append([slash.x, slash.y, slash.width, slash.height])
                        

                        
                        
                #melee detection
                if player.attacking:        
                    if player.attacking_rect.colliderect(enemy.rect) and enemy.i_frames == 6:
                        player.DOT_check(enemy, last_atk_type)
                        if player.Big_attacking:
                            enemy.hit = True    
                            enemy.hp -= player.Big_attack_dmg 
                            enemy.i_frames = 0
                        else:
                            #DOT check
                            enemy.hit = True    
                            enemy.hp -= player.dmg  
                            enemy.i_frames = 0

                #damage dot
                enemy.Burn(player.burn_tick, player.burn_sustain, player.burn_dmg, player.both_dot_increase)
                enemy.Poison(player.poison_tick, player.poison_sustain, player.poison_dmg, player.both_dot_increase)
                enemy.Slash_Burn(player.slash_burn_tick, player.slash_burn_sustain, player.slash_burn_dmg, player.both_dot_increase)
                enemy.Slash_Poison(player.slash_poison_tick, player.slash_poison_sustain, player.slash_poison_dmg, player.both_dot_increase)

                #death detection
                if enemy.hp <= 0:
                    if player.hp < player.max_hp:
                        if player.hp + 100 <= player.max_hp:
                            player.hp += 100
                        else:
                            player.hp = player.max_hp
                    player.xp += 50
                    if player.xp >= 100 * player.level * 1.5:
                        player.level += 1
                        level_up_frame = True
                        player.xp = 0
                    enemies.remove(enemy)

            level_text = font.render(f"Level: {player.level}", True, "white")
            xp_text = font.render(f"Experience needed: {player.xp} / {100 * player.level * 1.5}", True, "white")

            #checks if all the enemies are dead if yes new wave
            if len(enemies) == 0:
                wave_no += 1
                Enemy.spawn(Enemy, enemies, wave_no, level_length) #spawns more enemies 

            draw(
                player, enemies, camera_offset, fps_text, wave_text, paused, 
                in_selection, in_options, in_menu, direction_inst, position, 
                level_text, xp_text, last_atk_type, Game_over
                )

        #pause menu logic 
        if paused and not in_options and not in_menu and not in_selection and not Game_over:
            #FPS
            fps = int(clock.get_fps())
            fps_text = font.render(f"FPS: {fps}", True, 'white')
            
            #getting mouse position 60 times per second
            x,y = pygame.mouse.get_pos()
            
            #checks if the mouse is on a button (Looks complex but it's just addition)
            if (x < WIDTH//2 - 200 + quit_button_surface.get_width() and x > WIDTH//2 - 200) and (y > HEIGHT - 400 and y < HEIGHT - 400 + quit_button_surface.get_height()):
                quit_button_surface.set_alpha(100)
                on_quit = True
            else:
                quit_button_surface.set_alpha(50)
                on_quit = False

            if (x < WIDTH//2 - 200 + options_button_surface.get_width() and x > WIDTH//2 - 200) and (y > HEIGHT - 525 and y < HEIGHT - 525 + options_button_surface.get_height()):
                options_button_surface.set_alpha(100)
                on_options = True
            else:
                options_button_surface.set_alpha(50)
                on_options = False

            if (x < WIDTH//2 - 200 + resume_button_surface.get_width() and x > WIDTH//2 - 200) and (y > HEIGHT - 650 and y < HEIGHT - 650 + resume_button_surface.get_height()):
                resume_button_surface.set_alpha(100)
                on_resume = True
            else:
                resume_button_surface.set_alpha(50)
                on_resume = False


            draw(
                player, enemies, camera_offset, fps_text, wave_text, paused, 
                in_selection, in_options, in_menu, direction_inst, position, 
                level_text, xp_text, last_atk_type, Game_over
                )
            
            

        if in_options and not Game_over:
            #FPS
            fps = int(clock.get_fps())
            fps_text = font.render(f"FPS: {fps}", True, 'white')
            #Mouse position getting
            x,y = pygame.mouse.get_pos()

            #same ol
            if (x < WIDTH//2 - 200 + back_button_surface.get_width() and x > WIDTH//2 - 200) and (y > HEIGHT - 250 and y < HEIGHT - 250 + back_button_surface.get_height()):
                back_button_surface.set_alpha(100)
                on_back = True
            else:
                back_button_surface.set_alpha(50)
                on_back = False




            draw(
                player, enemies, camera_offset, fps_text, wave_text, paused, 
                in_selection, in_options, in_menu, direction_inst, position, 
                level_text, xp_text, last_atk_type, Game_over
                )

        if in_menu and not Game_over:
            draw(
                player, enemies, camera_offset, fps_text, wave_text, paused, 
                in_selection, in_options, in_menu, direction_inst, position,
                level_text, xp_text, last_atk_type, Game_over
                )
            
        if in_selection and not Game_over:

            #FPS
            fps = int(clock.get_fps())
            fps_text = font.render(f"FPS: {fps}", True, 'white')
            #Mouse position getting
            x,y = pygame.mouse.get_pos()

            if x > (WIDTH//3 - WIDTH//5 - WIDTH//10 + 108) and x < (WIDTH//3 - WIDTH//5 - WIDTH//10 + 108) + perks.pick_1.get_width():
                if y < (HEIGHT - HEIGHT//1.6 - 200) + perks.pick_1.get_height() and y > (HEIGHT - HEIGHT//1.6 - 200):
                    perks.pick_1.set_alpha(220)
                    on_perk_1 = True
                else:
                    on_perk_1 = False
                    perks.pick_1.set_alpha(150)
            else:
                on_perk_1 = False
                perks.pick_1.set_alpha(150)

            if x > (WIDTH//2 - WIDTH//10) and x < (WIDTH//2 - WIDTH//10) + perks.pick_2.get_width():
                if y < (HEIGHT - HEIGHT//1.6 - 200) + perks.pick_2.get_height() and y > (HEIGHT - HEIGHT//1.6 - 200):
                    perks.pick_2.set_alpha(220)
                    on_perk_2 = True
                else:
                    on_perk_2 = False
                    perks.pick_2.set_alpha(150)
            else:
                on_perk_2 = False
                perks.pick_2.set_alpha(150)

            if x > (WIDTH - WIDTH//5 - WIDTH//10) and x < (WIDTH - WIDTH//5 - WIDTH//10) + perks.pick_3.get_width():
                if y < (HEIGHT - HEIGHT//1.6 - 200) + perks.pick_3.get_height() and y > (HEIGHT - HEIGHT//1.6 - 200):
                    perks.pick_3.set_alpha(220)
                    on_perk_3 = True
                else:
                    on_perk_3 = False
                    perks.pick_3.set_alpha(150)
            else:
                on_perk_3 = False
                perks.pick_3.set_alpha(150)


            draw(
                player, enemies, camera_offset, fps_text, wave_text, paused, 
                in_selection, in_options, in_menu, direction_inst, position,
                level_text, xp_text, last_atk_type, Game_over
                )
        
        if Game_over:

            clock = pygame.time.Clock()
            player = Player(100, 74, 7, 1, 500, WIDTH//2, HEIGHT - 50)
            enemies = [] 
            camera_offset = [0,0]
            wave_no = 1
            level_length = WIDTH * level_width
            floor = pygame.FRect(0, HEIGHT - 50, level_length, 50) #might need later
            Enemy.spawn(Enemy, enemies, wave_no, level_length)
            gigantified = False
            counter_gigatification = 0
            jump_counter = 0
            paused = False
            in_selection = False

            fps = None

            running = True
            camera_offset[1] = 0

            in_options = False
            on_back = False
            in_menu = True
            wave_text = None
            on_quit = False
            on_options = False
            on_resume = False
            fps_text = None
            x,y = None,None
            x_add, y_add = 0,0
            direction_inst = None
            direction_list = []
            level_text, xp_text = None, None
            position = []
            level_up_frame = False
            on_perk_1, on_perk_2, on_perk_3 = False, False, False
            last_atk_type = None #if false then melee else slash
            hp_last = player.hp


            draw(
                player, enemies, camera_offset, fps_text, wave_text, paused, 
                in_selection, in_options, in_menu, direction_inst, position,
                level_text, xp_text, last_atk_type, Game_over
                )

    pygame.quit()

if __name__ == "__main__":
    main()