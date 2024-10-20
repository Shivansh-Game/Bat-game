import pygame
import random

pygame.init()

infoObject = pygame.display.Info()
WIDTH, HEIGHT = infoObject.current_w, infoObject.current_h
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

class Particles():
    def __init__(self):
        self.jump_particles = []
        self.jump_counter = 0 
        self.inst_player_pos = []
        self.hit_counter = 0
        self.hit_particles = []
        self.time_alive = 60

        
            

    def jump(self, player, camera_offset):
        if player.jumping_index_counter != 0:
            self.jump_counter += 1
        else:
            self.jump_particles = []
            self.jump_counter = 0
            camera_offset = []
            self.inst_player_pos = [] 

        

        if self.jump_counter <= 20 and player.jumping_index_counter != 0:
            if player.jumping_index_counter <= 6:
                if player.jumping_index_counter == 1:
                    self.inst_player_pos.append(player.rect.x)
                    self.inst_player_pos.append(player.rect.y)

                size_list = []
                for i in range(5):
                    width,height = random.randint(0,15), random.randint(0,15)
                    while [width, height] in size_list:
                        width,height = width,height = random.randint(0,15), random.randint(0,15)

                    size_list.append([width,height])
                    self.jump_particles.append(pygame.FRect(self.inst_player_pos[0] + width + height, self.inst_player_pos[1] + player.height,width,height))

                for i in range(12):
                    for rect in self.jump_particles:
                        rect.x += random.randint(-3, 3)
                        rect.y -= random.randint(-1,1)


                for rect in self.jump_particles:
                    pygame.draw.circle(WIN, (75, 60, 41), (rect.x + camera_offset[0], rect.y), rect.width//2 + rect.height//2)

            else:
                for i in range(15):
                    for rect in self.jump_particles:
                        rect.x += random.randint(-3, 3)
                        rect.y -= random.randint(-1,1)
                for rect in self.jump_particles:
                    pygame.draw.circle(WIN, (75, 60, 41), (rect.x + camera_offset[0], rect.y), rect.width//2 + rect.height//2)
                    if rect.width > 3:
                        rect.width -= 1
                    if rect.height > 3:
                        rect.height -= 1

    def hit(self, position, direction_inst, camera_offset, player_scale):

        
        
        self.time_alive -= 3 
        player_scale = 1.5 if player_scale == 2 else player_scale//2
        if player_scale < 1:
            player_scale = 1
        if len(self.hit_particles) == 0:
            size_list_hit = []
            self.time_alive = 60



        size_list_hit = []
        for _ in range(5):
            width,height = random.randint(0,15) * player_scale, random.randint(0,15) * player_scale
    
            while [width, height] in size_list_hit:
                width,height = width,height = random.randint(0,15) * player_scale, random.randint(0,15) * player_scale
    
            size_list_hit.append([width,height])
            for i in position:
                self.hit_particles.append(pygame.FRect((position[0][0],position[0][1]), (width, height)))
        
        for rect in self.hit_particles:

            if direction_inst:
                rect.x += random.randint(-7, 3) * player_scale
                rect.y -= random.randint(-7 * 4, 4 * 4) * player_scale
                
            else:
                rect.x -= random.randint(-7, 3) * player_scale
                rect.y -= random.randint(-7 * 4, 4 * 4)  * player_scale
                

        for rect in self.hit_particles:
            if rect.width > 1:
                rect.width -= 1.5
            if rect.height > 1:
                rect.height -= 1.5


                    
        for rect in self.hit_particles:
            direction_adjustment =  0 if not direction_inst else position[0][2]
            pygame.draw.circle(WIN, "red", (rect.x + camera_offset[0] + direction_adjustment, rect.y), rect.width//2 + rect.height//2)

        rects_remove = []
        for rect in self.hit_particles:
            if rect.width <= 1 and rect.height <= 1:
                rects_remove.append(rect)

        for rect in rects_remove:
            self.hit_particles.remove(rect)


        if self.time_alive <= 0:
            size_list_hit = []
            self.hit_particles = []
            self.time_alive = 60