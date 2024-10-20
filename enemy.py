import pygame
import random
import math
pygame.init()

infoObject = pygame.display.Info()
WIDTH, HEIGHT = infoObject.current_w, infoObject.current_h
WIN = pygame.display.set_mode((WIDTH, HEIGHT))


class Enemy:
    def __init__(self, x, y, width, height, velocity, hp, dmg, attack_range_x, attack_range_y):
        self.max_hp = hp
        self.hp = hp 
        self.dmg = dmg
        self.x = x
        self.y = y
        self.attack_range_x = attack_range_x
        self.attack_range_y = attack_range_y
        self.width = width
        self.height = height
        self.is_jumping = False
        self.jump_height = 10
        self.gravity = 0.5

        self.rect = pygame.FRect(x - self.width//2, y - self.height, self.width, self.height)
        self.attack_range_rect = pygame.FRect(x - self.width//2, y - self.height, self.width + self.attack_range_x, self.height  + self.attack_range_y)
        self.velocity = velocity
        self.facing = True
        self.hit = False
        self.i_frames = 6
        self.sprite = []
        self.sprite_counter = 0
        self.sprite_index = 0
        self.fly_counter = 0
        self.fly_up = False
        self.current_sprite = None
        for i in range(1,6):
            self.sprite.append(pygame.transform.scale(pygame.image.load(f"Shivansh Python\Files\\bat_red{i}_w_trans.png"), (self.width, self.height)).convert())

        self.burnt = False
        self.poisoned = False
        self.both_dot = False
        self.time_burning = 0
        self.burning_ticks = 0
        self.time_poisoned = 0
        self.poisoned_ticks = 0

        self.slash_burnt = False
        self.slash_poisoned = False
        self.slash_both_dot = False
        self.slash_time_burning = 0
        self.slash_burning_ticks = 0
        self.slash_time_poisoned = 0
        self.slash_poisoned_ticks = 0

        self.charge = False
        self.charge_counter = 0


    def move(self, player_y, player_height, level_length, player_x):
        self.attack_range_rect.x = self.rect.x - self.attack_range_x//2
        self.attack_range_rect.y = self.rect.y - self.attack_range_y//2
        a = 0
        b = 0
        

        if self.facing:
            self.rect.x += self.velocity
            if self.hit and (self.rect.x - (self.velocity * 6)) > 0:
                self.rect.x -= self.velocity * 6 
                self.is_jumping = True
        else:
            self.rect.x -= self.velocity
            if self.hit and (self.rect.x + self.width  + (self.velocity * 6)) < level_length:
                self.rect.x += self.velocity * 6 
                self.is_jumping = True

        if player_y + player_height//3 < self.rect.y:
            self.rect.y -= self.velocity // 1.5
        else:
            self.rect.y += self.velocity // 1.5

        if self.rect.y > player_y:
            a = random.randint(1,120)
        if a == 1:
            self.fly_up = True
        
        if (self.rect.x < player_x + 500 and self.rect.x > player_x - 500) and self.rect.y > player_y:
            b = random.randint(1,30)
        if b == 1:
            self.charge = True

        if self.charge:
            self.charge_counter += 1
            self.rect.x += 12 if self.facing else - 12
            if self.charge_counter >= 35:
                self.charge_counter = 0
                self.charge = False


        if self.fly_up:
            self.fly_counter += 1
            self.rect.y -= 8
            if self.fly_counter >= 40:
                self.fly_up = False
                self.fly_counter = 0

        if self.is_jumping:
            if self.jump_height >= -10:
                neg = 1
                if self.jump_height < 0:
                    neg = -1
                self.rect.y -= (self.jump_height ** 2) * 0.5 * neg * self.gravity 
                self.jump_height -= 1
            else:
                self.is_jumping = False
                self.jump_height = 10
                self.hit = False


    def spawn(self, enemies, wave_no, level_length):
        k = None
        k2 = None
        sign_thingy = 1
        max_hp = 150
        max_hp += 30 * wave_no * 1.5
        spawn_range = (wave_no ** 2)/1.25 if wave_no >= 4 else 3 * wave_no
        for i in range(spawn_range//1):
            speed = random.randint(4,6) + random.randint(1,9) / 10
            y = random.randint(0,HEIGHT)
            if k is not None:
               k2 = k 
            k = random.randint(0, level_length)
            while k2 is not None and k - k2 * sign_thingy < 300:
                k = random.randint(0, level_length)
                if k - k2 < 0:
                    sign_thingy = -1
                else:
                    sign_thingy = 1

            enemies.append(Enemy(k, y, 64, 48, speed, max_hp, 50, 120, 80))

    def outline(self, camera_offset):
        x_pos, y_pos = self.rect.x + camera_offset[0], self.rect.y

        # Calculate mask surface once
        mask = pygame.mask.from_surface(self.current_sprite)
        self.alpha = round(self.hp / (self.max_hp / 255))
        mask_surf = mask.to_surface(setcolor=(255, 0, 0, self.alpha)).convert()
        mask_surf.set_colorkey((0, 0, 0))

        # Use a loop for BLIT operations
        offsets = [(1, 0), (-1, 0), (0, -1), (0, 1)]
        for offset in offsets:
            WIN.blit(mask_surf, (x_pos + offset[0], y_pos + offset[1]))

    def Burn(self, ticks, sustain, dmg, both_dot_increase):

        if self.burnt and self.time_burning <= sustain:
            self.time_burning += 1
            if self.burning_ticks < ticks:
                self.burning_ticks += 1

            if self.burning_ticks == ticks:
                self.hp -= dmg * both_dot_increase if self.both_dot else dmg
                self.burning_ticks = 0
        else:
            self.burnt = False
            

    def Poison(self, ticks, sustain, dmg, both_dot_increase):
        if self.poisoned and self.time_poisoned <= sustain:
            self.time_poisoned += 1
            if self.poisoned_ticks < ticks:
                self.poisoned_ticks += 1

            if self.poisoned_ticks == ticks:
                self.hp -= dmg * both_dot_increase if self.both_dot else dmg
                self.poisoned_ticks = 0
                
        else:
            self.poisoned = False

    def Slash_Burn(self, ticks, sustain, dmg, both_dot_increase):

        if (self.slash_burnt or self.burnt) and (self.slash_poisoned or self.poisoned):
            self.slash_both_dot = True 
        else:
            self.slash_both_dot = False

        if self.slash_burnt and self.slash_time_burning <= sustain:
            self.slash_time_burning += 1
            if self.slash_burning_ticks <= ticks:
                self.slash_burning_ticks += 1

            if self.slash_burning_ticks == ticks:
                self.hp -= dmg * both_dot_increase if self.slash_both_dot else dmg
                self.slash_burning_ticks = 0
        else:
            self.slash_burnt = False
            

    def Slash_Poison(self, ticks, sustain, dmg, both_dot_increase):

        if (self.slash_burnt or self.burnt) and (self.slash_poisoned or self.poisoned):
            self.slash_both_dot = True 
        else:
            self.slash_both_dot = False


        if self.slash_poisoned and self.slash_time_poisoned <= sustain:
            self.slash_time_poisoned += 1
            if self.slash_poisoned_ticks <= ticks:
                self.slash_poisoned_ticks += 1

            if self.slash_poisoned_ticks == ticks:
                self.hp -= dmg * both_dot_increase if self.slash_both_dot else dmg
                self.slash_poisoned_ticks = 0
                
        else:
            self.slash_poisoned = False
            

    def Poison_draw(self, camera_offset):
        x_pos, y_pos = self.rect.x + camera_offset[0], self.rect.y

        # Calculate mask surface once
        mask = pygame.mask.from_surface(self.current_sprite)
        mask_surf = mask.to_surface(setcolor=(48, 204, 39, 50))#.convert()
        mask_surf.set_colorkey((0, 0, 0))

        WIN.blit(mask_surf, (x_pos, y_pos))

    def Burn_draw(self, camera_offset):
        x_pos, y_pos = self.rect.x + camera_offset[0], self.rect.y

        # Calculate mask surface once
        mask = pygame.mask.from_surface(self.current_sprite)
        mask_surf = mask.to_surface(setcolor=(235, 149, 50, 50))#.convert()
        mask_surf.set_colorkey((0, 0, 0))

        WIN.blit(mask_surf, (x_pos, y_pos))
        



    def draw(self, camera_offset):
        #pygame.draw.rect(WIN, 'red', self.attack_range_rect.move(camera_offset))
        #pygame.draw.rect(WIN, 'blue', self.rect.move(camera_offset))
        self.current_sprite = self.sprite[self.sprite_index]
        #if self.current_sprite is not None:
        #    self.outline(camera_offset)


        WIN.blit(self.sprite[self.sprite_index], (self.rect.x + camera_offset[0], self.rect.y - camera_offset[1]))
        if self.poisoned or self.slash_poisoned:
            self.Poison_draw(camera_offset)

        if self.burnt or self.slash_burnt:
            self.Burn_draw(camera_offset)

        self.sprite_counter += 0.25
        if self.sprite_counter % 1 == 0:
            if self.sprite_index < len(self.sprite) - 1:
                self.sprite_index += 1
            else:
                self.sprite_index = 0
            self.sprite_counter = 0




