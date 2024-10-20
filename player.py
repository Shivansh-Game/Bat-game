import pygame
import math 

pygame.init()

infoObject = pygame.display.Info()
WIDTH, HEIGHT = infoObject.current_w, infoObject.current_h
WIN = pygame.display.set_mode((WIDTH, HEIGHT))


class Player():
    def __init__(self, width, height, velocity, scale, hp, x, y):
        self.hp = hp
        self.max_hp = 500
        self.width = width * scale 
        self.height = height * scale 
        self.x = x
        self.y = y - self.height 
        self.scale = scale 
        self.right_attack = []
        self.left_attack = []
        self.left_walk = []
        self.right_walk = []
        self.idle_left = []
        self.idle_right = []
        self.jump_right = []
        self.jump_left = []
        self.fall_left = []
        self.fall_right = []
        self.Big_attack_sprites = []
        self.Big_attack_sprites_mirrored = []

        for i in range(4):
            self.Big_attack_sprites.append(pygame.transform.scale(pygame.image.load(f"Shivansh Python\Files/adventurer-air-attack1-0{i}.png").convert_alpha(), (self.width, self.height)))
            self.Big_attack_sprites_mirrored.append(pygame.transform.scale(pygame.image.load(f"Shivansh Python\Files/adventurer-air-attack1-0{i}_mirrored.png").convert_alpha(), (self.width, self.height)))

        for i in range(2):
            self.fall_right.append(pygame.transform.scale(pygame.image.load(f"Shivansh Python\Files/adventurer-fall-0{i}.png").convert_alpha(), (self.width, self.height)))
            self.fall_left.append(pygame.transform.scale(pygame.image.load(f"Shivansh Python\Files/adventurer-fall-mirrored-0{i}.png").convert_alpha(), (self.width, self.height)))   

        for i in range(4):
            self.jump_right.append(pygame.transform.scale(pygame.image.load(f"Shivansh Python\Files/adventurer-jump-0{i}.png").convert_alpha(), (self.width, self.height)))
            self.jump_left.append(pygame.transform.scale(pygame.image.load(f"Shivansh Python\Files/adventurer-jump-mirrored-0{i}.png").convert_alpha(), (self.width, self.height)))
        
        for i in range(4):
            self.idle_left.append(pygame.transform.scale(pygame.image.load(f"Shivansh Python\Files/adventurer-idle-mirrored-0{i}.png").convert_alpha(), (self.width, self.height)))
            self.idle_right.append(pygame.transform.scale(pygame.image.load(f"Shivansh Python\Files/adventurer-idle-0{i}.png").convert_alpha(), (self.width, self.height)))

        for i in range(3):
            self.left_attack.append(pygame.transform.scale(pygame.image.load(f"Shivansh Python\Files/adventurer-air-attack2-mirrored{i}.png").convert_alpha(), (self.width, self.height)))
            self.right_attack.append(pygame.transform.scale(pygame.image.load(f"Shivansh Python\Files/adventurer-air-attack2-0{i}.png").convert_alpha(), (self.width, self.height)))
        
        for i in range(6):   
            self.left_walk.append(pygame.transform.scale(pygame.image.load(f"Shivansh Python\Files/adventurer-run-0{i}-mirrored.png").convert_alpha(), (self.width, self.height)))
            self.right_walk.append(pygame.transform.scale(pygame.image.load(f"Shivansh Python\Files/adventurer-run-0{i}.png").convert_alpha(), (self.width, self.height)))        
        
        self.velocity = velocity * scale 
        self.dmg = 60 * scale  
        self.rect = pygame.FRect(self.x, self.y, self.width//2, self.height) #50 is for adjusting for the platform on the background to make it look cohesive
        self.attacking_rect = pygame.FRect(self.x, self.y, self.width * 1.5, self.height)
        self.facing = True #True = right ; False = Left
        self.walking_left = False
        self.walking_right = False
        self.shoot_index_counter = 0
        self.player_sprites_attack = [self.left_attack, self.right_attack]
        self.attack_sprite = None
        self.walking_index = 0
        self.idle_index = 0
        self.walking_frame_tickrate = 0
        self.shoot_frame_tickrate = 0
        self.idle_frame_tickrate = 0
        self.is_jumping = False

        if self.scale > 1:
            self.jump_velo = 18 * (self.scale / 3 + self.scale / 3)
        else:
            self.jump_velo = 18
        self.jump_angle = math.radians(70)
        self.jump_velo_x = self.jump_velo * math.cos(self.jump_angle)
        self.jump_velo_y = round(self.jump_velo * math.sin(self.jump_angle))
        self.jump_counter = 0
        self.jump_sound_played = False
        self.gravity = 1
        self.fall_index = None
        self.fall_counter = 0
        self.jumping_index = None
        self.jumping_index_counter = 0
        self.shoot_animation_finished = True
        self.attacking = False
        self.walking_left_sound = pygame.mixer.Sound("Shivansh Python\Files/Left_step_sound.wav")
        self.walking_right_sound = pygame.mixer.Sound("Shivansh Python\Files/Right_step_sound.wav")
        self.jump_sound = pygame.mixer.Sound("Shivansh Python\Files/Jump_sound.wav")
        self.hurt_sound = pygame.mixer.Sound("Shivansh Python\Files\\Hurt_sound.wav")
        self.Hit_sound = pygame.mixer.Sound("Shivansh Python\Files/Throw_sound.wav")
        self.Level_up_sound = pygame.mixer.Sound("Shivansh Python\Files/Level_up_sound.wav")
        self.walking_sound_counter = 0
        self.sound_played = False
        self.Hit_sound_counter = 0 
        self.attack_delay = 30 #in ticks
        self.walking = False
        self.i_frames = 6
        self.Big_attack_sprite = None
        self.Big_attack_index = None
        self.jump_finished = True
        self.xp = 0
        self.level = 1
        self.Big_attack_counter = 0
        self.attack_animation_finished = True
        self.Big_attack_dmg = (60//2) * scale
        self.Big_attacking = False
        self.slash_list = []
        self.slash_rect_list = []
        self.slash_speed = 20
        self.camera_offset_inst = None
        self.max_slash_no = 1
        self.atk_range_y_increase = 1
        self.atk_range_x_increase = 1

        self.Big_attack_delay = 60
        self.normal_attack_delay = 30
        self.current_sprite = None
        self.alpha = round(self.hp//(self.max_hp/255))

        self.can_burn = False
        self.can_poison = False
        self.both_dot_buff = False

        self.burn_dmg = 60
        self.burn_tick = 60
        self.burn_sustain = 180

        self.poison_dmg = 45
        self.poison_tick = 30
        self.poison_sustain = 180

        self.both_dot_increase = 1

        self.giant_form_time = 1200
        self.giant_form_time_base = 1200

        self.slash_can_burn = False
        self.slash_can_poison = False

        self.slash_burn_dmg = 0
        self.slash_burn_tick = 60
        self.slash_burn_sustain = 180

        self.slash_poison_dmg = 0
        self.slash_poison_tick = 30
        self.slash_poison_sustain = 180


        self.slash_list.append(pygame.transform.scale_by(pygame.image.load("Shivansh Python\Files\\Slash_projectile_1.png").convert_alpha(), 2 * self.scale))
        self.slash_list.append(pygame.transform.scale_by(pygame.image.load("Shivansh Python\Files\\Slash_projectile_1_mirrored.png").convert_alpha(), 2 * self.scale))
        

    def move(self, keys, level_length):
        self.attacking_rect.x = self.rect.x - self.attacking_rect.width//3
        self.attacking_rect.y = self.rect.y
        self.x = self.rect.x
        self.y = self.rect.y
        if keys[pygame.K_a] and self.rect.x > 0 and not(keys[pygame.K_a] and keys[pygame.K_d]):
            self.walking = True
            self.rect.x -= self.velocity
            self.facing = False
            self.attack_sprite = None
            self.walking_left = True
            self.walking_right = False
            self.walking_frame_tickrate += 0.125
            if self.walking_frame_tickrate % 1 == 0:
                if self.walking_index < 5:
                    self.walking_index += 1
                else:
                    self.walking_index = 0
            if self.is_jumping:
                self.rect.x -= self.jump_velo_x
        else:
            self.walking_left = False
            if not self.walking_right:
                self.walking = False


        if keys[pygame.K_d] and self.rect.x <= level_length - self.width//2  and not(keys[pygame.K_a] and keys[pygame.K_d]):
            self.walking = True
            self.rect.x += self.velocity
            self.facing = True
            self.attack_sprite = None
            self.walking_right = True
            self.walking_left = False
            self.walking_frame_tickrate += 0.125
            if self.walking_frame_tickrate % 1 == 0:
                if self.walking_index < 5:
                    self.walking_index += 1
                else:
                    self.walking_index = 0
            if self.is_jumping:
                self.rect.x += self.jump_velo_x
        else:
            self.walking_right = False
            if not self.walking_left:
                self.walking = False
        
    def jump(self):
        if self.is_jumping:
            self.jump_finished = False
            if self.jumping_index_counter < 15 and self.fall_index is None:
                self.jumping_index_counter += 1
            if self.jumping_index_counter <= 3 and self.fall_index is None:
                self.jumping_index = 0
            elif self.jumping_index_counter <= 6 and self.fall_index is None:
                self.jumping_index = 1
            else:
                if self.is_jumping:
                    self.jumping_index = 2
                    if self.jumping_index_counter > 12 and self.fall_index is None:
                        self.jumping_index = 3

                    if not self.jump_sound_played:
                        self.jump_sound.play()
                        self.jump_sound_played = True
                    # If player is in the jumping state, update the y-coordinate
                    self.rect.y -= self.jump_velo_y
                    # Apply gravity to decrease upward velocity
                    self.jump_velo_y -= self.gravity

                    self.jump_counter += 1
                if self.jump_velo_y <= 0:
                    self.fall_counter += 1
                    self.jumping_index = None
                    self.jumping_index_counter = 0
                    if self.fall_counter <= 3:
                        self.fall_index = 0
                    else:
                        self.fall_index = 1
                    if self.jump_counter == 0:
                        self.rect.y -= self.jump_velo_y
                        self.is_jumping = False
                        self.jump_sound_played = False
                        self.fall_counter = 0
                        self.fall_index = None
                        self.jump_velo_y = round(self.jump_velo * math.sin(self.jump_angle))
                        self.jump_counter = 2

                    self.jump_counter -= 2
        else:
            self.jump_finished = True


    def sound_walk(self):
        if self.shoot_animation_finished and not self.is_jumping:
            if self.walking_right and not self.sound_played and (self.walking_index == 1 or self.walking_index == 5): 
                self.walking_left_sound.play()

                self.walking_sound_counter = 1
                self.sound_played = True
            if self.walking_index == 3 and self.walking_sound_counter == 1 and self.sound_played:
                self.walking_right_sound.play()

                self.walking_sound_counter = 0
                self.sound_played = False
            if self.walking_left and not self.sound_played and (self.walking_index == 1 or self.walking_index == 5):
                self.walking_right_sound.play()
                self.walking_sound_counter = 1
                self.sound_played = True
            if self.walking_index == 3 and self.walking_sound_counter == 1 and self.sound_played:
                self.walking_left_sound.play()
                self.walking_sound_counter = 0
                self.sound_played = False

                
    def draw(self, camera_offset, direction_inst):
        self.rect.x += camera_offset[0]
        self.attacking_rect.x = self.rect.x - (self.attacking_rect.width * self.atk_range_x_increase)//(3 * self.atk_range_x_increase)
        self.attacking_rect.y = self.rect.y - (self.attacking_rect.height * self.atk_range_y_increase)//(4 * self.atk_range_y_increase)
        #pygame.draw.rect(WIN, 'red', self.attacking_rect)
        #pygame.draw.rect(WIN, 'white', self.rect)

        
        

        for rect in self.slash_rect_list:
            inst_offset = camera_offset
            rect.x += inst_offset[0]
            #pygame.draw.rect(WIN, 'green', rect)
            
            WIN.blit(self.slash_list[0 if direction_inst else 1], (rect.x, rect.y))
            self.slash_outline(self.slash_list[0 if direction_inst else 1], rect)
            rect.x -= inst_offset[0]


        if self.Big_attack_index is not None:
            if self.facing:
                self.current_sprite = self.Big_attack_sprites[self.Big_attack_index]
                self.outline()
                WIN.blit(self.Big_attack_sprites[self.Big_attack_index], (self.rect.x - 25, self.rect.y + camera_offset[1] ))
            else:
                self.current_sprite = self.Big_attack_sprites_mirrored[self.Big_attack_index]
                self.outline()
                WIN.blit(self.Big_attack_sprites_mirrored[self.Big_attack_index], (self.rect.x - 25, self.rect.y + camera_offset[1] ))

        if self.attack_sprite is not None:
            self.current_sprite = self.attack_sprite
            self.outline()
            WIN.blit(self.attack_sprite, (self.rect.x - 25, self.rect.y + camera_offset[1] ))

        if self.walking_left and self.jumping_index is None and self.fall_index is None:
            self.current_sprite = self.left_walk[self.walking_index]
            self.outline()
            WIN.blit(self.left_walk[self.walking_index], (self.rect.x - 25, self.rect.y + camera_offset[1]))
            
        if self.walking_right and self.jumping_index is None and self.fall_index is None:
            self.current_sprite = self.right_walk[self.walking_index]
            self.outline()
            WIN.blit(self.right_walk[self.walking_index], (self.rect.x - 25, self.rect.y + camera_offset[1]))

        if self.jumping_index is not None and self.Big_attack_index is None and self.attack_sprite is None:
            if self.facing:
                self.current_sprite = self.jump_right[self.jumping_index]
                self.outline()
                WIN.blit(self.jump_right[self.jumping_index], (self.rect.x - 25, self.rect.y + camera_offset[1]))
            else:
                self.current_sprite = self.jump_left[self.jumping_index]
                self.outline()
                WIN.blit(self.jump_left[self.jumping_index], (self.rect.x - 25, self.rect.y + camera_offset[1]))

        if self.fall_index is not None and self.Big_attack_index is None and self.attack_sprite is None:
            if self.facing:
                self.current_sprite = self.fall_right[self.fall_index]
                self.outline()
                WIN.blit(self.fall_right[self.fall_index], (self.rect.x - 25, self.rect.y + camera_offset[1]))
            else:
                self.current_sprite = self.fall_left[self.fall_index]
                self.outline()
                WIN.blit(self.fall_left[self.fall_index], (self.rect.x - 25, self.rect.y + camera_offset[1]))

        if not self.walking_left and not self.walking_right and self.attack_sprite is None and self.jumping_index is None and self.fall_index is None and self.Big_attack_index is None:

            if self.facing:
                self.current_sprite = self.idle_right[self.idle_index]
                self.outline()
                WIN.blit(self.idle_right[self.idle_index], (self.rect.x - 25, self.rect.y + camera_offset[1]))

            else:
                self.current_sprite = self.idle_left[self.idle_index]
                self.outline()
                WIN.blit(self.idle_left[self.idle_index], (self.rect.x - 25, self.rect.y + camera_offset[1]))

            self.idle_frame_tickrate += 0.125
            if self.idle_frame_tickrate % 1 == 0:
                self.idle_frame_tickrate = 0
                if self.idle_index < 3:
                    self.idle_index += 1
                else:
                    self.idle_index = 0
        
        
        self.rect.x -= camera_offset[0]
        self.attacking_rect.x = self.rect.x - self.attacking_rect.width//3


    def outline(self):
        mask = pygame.mask.from_surface(self.current_sprite)
        self.alpha = round(self.hp//(self.max_hp/255)) if self.hp > 0 else 0
        mask_surf = mask.to_surface(setcolor=(255,255,255,self.alpha if self.alpha < 255 else 255))
        mask_surf.set_colorkey((0,0,0))
        x_pos, y_pos = self.rect.x - 25, self.rect.y
        WIN.blit(mask_surf, (x_pos + 1, y_pos))
        WIN.blit(mask_surf, (x_pos - 1, y_pos))
        WIN.blit(mask_surf, (x_pos, y_pos - 1))
        WIN.blit(mask_surf, (x_pos, y_pos + 1))

    def slash_outline(self, img, rect):
        color = None
        slash_mask = pygame.mask.from_surface(img)
        color = (152, 218, 241, 255)
        slash_mask_surf = slash_mask.to_surface(setcolor=color)
        slash_mask_surf.set_colorkey((0,0,0))
        x_pos, y_pos = rect.x, rect.y
        

        if self.slash_can_burn:
            color = (253,82,0)
            slash_mask_surf = slash_mask.to_surface(setcolor=color)
            slash_mask_surf.set_colorkey((0,0,0))


        WIN.blit(slash_mask_surf, (x_pos + 2, y_pos))
        WIN.blit(slash_mask_surf, (x_pos - 2, y_pos))
        WIN.blit(slash_mask_surf, (x_pos, y_pos - 2))
        WIN.blit(slash_mask_surf, (x_pos, y_pos + 2))
        WIN.blit(slash_mask_surf, (x_pos + 1, y_pos))
        WIN.blit(slash_mask_surf, (x_pos - 1, y_pos))
        WIN.blit(slash_mask_surf, (x_pos, y_pos - 1))
        WIN.blit(slash_mask_surf, (x_pos, y_pos + 1))

        if self.slash_can_poison:
            color = (48, 204, 39, 255)
        else:
            color = (152, 218, 241, 255)
        slash_mask_surf = slash_mask.to_surface(setcolor=color)
        slash_mask_surf.set_colorkey((0,0,0))

        WIN.blit(slash_mask_surf, (x_pos, y_pos))

    def shoot(self):
        self.attack_delay = self.normal_attack_delay
        self.walking_left = False
        self.walking_right = False
        self.shoot_animation_finished = False
        self.attacking = True
        if self.Hit_sound_counter == 0:
            self.Hit_sound.play()
        self.Hit_sound_counter = 1
        if self.facing:
            self.attack_sprite = self.player_sprites_attack[1][self.shoot_index_counter]
            self.shoot_frame_tickrate += 0.125
            if self.shoot_frame_tickrate % 1 == 0:
                self.shoot_index_counter += 1
            if self.shoot_index_counter > 2:
                self.shoot_index_counter = 0
        if not self.facing:
            self.attack_sprite = self.player_sprites_attack[0][self.shoot_index_counter]
            self.shoot_frame_tickrate += 0.125
            if self.shoot_frame_tickrate % 1 == 0:
                self.shoot_index_counter += 1
            if self.shoot_index_counter > 2:
                self.shoot_index_counter = 0
        if self.shoot_index_counter == len(self.player_sprites_attack[1]) - 1:
            self.shoot_index_counter = 0
            self.Hit_sound_counter = 0
            self.shoot_animation_finished = True
            self.attacking = False

    def Big_attack(self):
        if not self.attacking:
            self.Big_attack_counter = 0
            self.Big_attack_index = 0
            self.Hit_sound.play()
        self.attack_delay = self.Big_attack_delay
        self.walking_left = False
        self.walking_right = False
        self.attack_animation_finished = False
        self.attacking = True
        self.attack_sprite = None
        self.Big_attacking = True
        

        self.Big_attack_counter += 1
        if self.Big_attack_counter % 4 == 0:
            if self.Big_attack_index < len(self.Big_attack_sprites) - 1:
                self.Big_attack_index += 1
            else:
                
                self.slash_rect_list.append(pygame.Rect(self.rect.x , self.rect.y , 100 * self.scale, 74 * self.scale))
                self.Big_attack_index = None
                self.attacking = False
                self.Big_attack_counter = 0
                self.Big_attacking = False
                self.attack_animation_finished = True


    def DOT_check(self, enemy, last_atk_type):
        if not last_atk_type:
            if self.can_burn:
                enemy.burnt = True
            if self.can_poison:
                enemy.poisoned = True
        else:
            if self.slash_can_burn:
                enemy.burnt = True
            if self.slash_can_poison:
                enemy.poisoned = True


        if self.both_dot_buff:
            enemy.both_dot = True

        