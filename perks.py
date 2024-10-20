import pygame
import random
pygame.init()

infoObject = pygame.display.Info()
WIDTH, HEIGHT = infoObject.current_w, infoObject.current_h
WIN = pygame.display.set_mode((WIDTH, HEIGHT))


class Perks:
    def __init__(self):
        #pausing variables
        self.selecting = False

        self.pick_1 = pygame.Surface((WIDTH//5, HEIGHT//1.6))
        self.pick_1.set_alpha(150)

        self.pick_2 = pygame.Surface((WIDTH//5, HEIGHT//1.6))
        self.pick_2.set_alpha(150)

        self.pick_3 = pygame.Surface((WIDTH//5, HEIGHT//1.6))
        self.pick_3.set_alpha(150)

        self.surface = pygame.Surface((WIDTH, HEIGHT))
        self.surface.set_alpha(100)

        self.powerup_1_selected = None
        self.powerup_2_selected = None
        self.powerup_3_selected = None

        self.perks_active = []

        self.powerup_no = 7

        #font
        self.font = pygame.font.Font("Shivansh Python\Files\\m5x7.ttf", 36)
        self.font_header = pygame.font.Font("Shivansh Python\Files\\m5x7.ttf", 54)

        #better melee
        self.better_melee_head = self.font_header.render(f"Sharpened Blade", True, 'white')
        self.better_melee = self.font.render(f"Increases melee \n damage by 20%", True, 'white')
        self.better_melee2 = self.font.render(f"Increases melee \n damage by 30% \n and increases \n vertical range by 15%", True, 'white')
        self.better_melee3 = self.font.render(f"Increases melee \n damage by 50% \n and increases \n range by 20% \n (stacks with downgrades)", True, 'white')
        self.powerup_level_1 = 1
        self.powerup_1 = [self.better_melee_head, self.better_melee, self.better_melee2, self.better_melee3, self.powerup_level_1]
        

        #better slash
        self.better_slash_head = self.font_header.render(f"Honed Edge", True, 'white')
        self.better_slash = self.font.render(f"Increases slash damage\n by 30%", True, 'white')
        self.better_slash2 = self.font.render(f"Increases slash damage\n by 45%", True, 'white')
        self.better_slash3 = self.font.render(f"Increases slash damage\n by 75%", True, 'white')
        self.powerup_level_2 = 1
        self.powerup_2 = [self.better_slash_head, self.better_slash, self.better_slash2, self.better_slash3, self.powerup_level_2]
        

        #Flame melee
        self.flame_head = self.font_header.render(f"Ignited Steel", True, 'white')
        self.flame = self.font.render(f"Melee hits inflict\n burn (40 dps)", True, 'white')
        self.flame2 = self.font.render(f"Burn damage increased\n (70 dps)", True, 'white')
        self.flame3 = self.font.render(f"Burn damage increased \n(100 dps)", True, 'white')
        self.powerup_level_3 = 1
        self.powerup_3 = [self.flame_head, self.flame, self.flame2, self.flame3, self.powerup_level_3]
        

        #Poison melee
        self.poison_head = self.font_header.render(f"Poisoning Stab", True, 'white')
        self.poison = self.font.render(f"Melee hits \n inflict poison \n (25 dps, \n 12.5 dmg per tick,\n 3 seconds)", True, 'white')
        self.poison2 = self.font.render(f"Poison damage increased\n but duration decreased \n (60 dps,\n 30 dmg per proc,\n 2 seconds)", True, 'white')
        self.poison3 = self.font.render(f"Poison damage\n decreased but\n tick rate increased \n (90 dps,\n 15 damage per proc,\n 2 seconds)", True, 'white')
        self.powerup_level_4 = 1
        self.powerup_4 = [self.poison_head, self.poison, self.poison2, self.poison3, self.powerup_level_4]
        

        #boiling blood
        self.heat_poison_head = self.font_header.render(f"Boiling Death", True, 'white')
        self.heat_poison = self.font.render(f"Inflicting both\n burn and poison\n at once increases\n the damage of\n both by 25%", True, 'white')
        self.heat_poison2 =self.font.render(f"Inflicting both\n burn and poison\n at once increases\n the damage of\n both by 50%", True, 'white')
        self.heat_poison3 = self.font.render(f"Inflicting both\n burn and poison\n at once increases\n the damage of\n both by 75%", True, 'white')
        self.powerup_level_5 = 1
        self.powerup_5 = [self.heat_poison_head, self.heat_poison, self.heat_poison2, self.heat_poison3, self.powerup_level_5]

        #--------------Giant_Form_Buffs----------------#
        self.g1_head = self.font_header.render(f"Extended Lifeline", True, 'white')
        self.g1 = self.font.render(f"Increase \n Duration of \n giant form \n by 25%", True, 'white')
        self.g2 =self.font.render(f"Increase \n Duration of \n giant form \n by 50%", True, 'white')
        self.g3 = self.font.render(f"Increase \n Duration of \n giant form \n by 75%", True, 'white')
        self.powerup_level_6 = 1
        self.powerup_6 = [self.g1_head, self.g1, self.g2, self.g3, self.powerup_level_6]



        self.g_2_head = self.font_header.render(f"Giant Hits", True, 'white')
        self.g_2 = self.font.render(f"Increase \n Damage \n while in \n giant form \n by 25%", True, 'white')
        self.g2_2 =self.font.render(f"Increase \n Damage \n while in \n giant form \n by 50%", True, 'white')
        self.g2_3 = self.font.render(f"Increase \n Damage \n while in \n giant form \n by 75%", True, 'white')
        self.powerup_level_7 = 1
        self.powerup_7 = [self.g_2_head, self.g_2, self.g2_2, self.g2_3, self.powerup_level_7]

        #MORE DOT

        #Flame Slash
        self.flame_slash_head = self.font_header.render(f"Fiery Slash", True, 'white')
        self.flame_slash = self.font.render(f"Slash hits inflict\n burn (25 dps)", True, 'white')
        self.flame_slash2 = self.font.render(f"Burn damage increased\n (50 dps)", True, 'white')
        self.flame_slash3 = self.font.render(f"Burn damage increased \n(70 dps)", True, 'white')
        self.powerup_level_8 = 1
        self.powerup_8 = [self.flame_slash_head, self.flame_slash, self.flame_slash2, self.flame_slash3, self.powerup_level_8]
        

        #Poison Slash
        self.poison_slash_head = self.font_header.render(f"Poisoning Pierce", True, 'white')
        self.poison_slash = self.font.render(f"Slash hits \n inflict poison \n (20 dps, \n 10 dmg per tick,\n 3 seconds)", True, 'white')
        self.poison_slash2 = self.font.render(f"Poison damage increased\n but duration decreased \n (40 dps,\n 20 dmg per proc,\n 2 seconds)", True, 'white')
        self.poison_slash3 = self.font.render(f"Poison damage\n decreased but\n tick rate increased \n (72 dps,\n 12 damage per proc,\n 2 seconds)", True, 'white')
        self.powerup_level_9 = 1
        self.powerup_9 = [self.poison_slash_head, self.poison_slash, self.poison_slash2, self.poison_slash3, self.powerup_level_9]


        #damage 0 dot 100 
        self.DOT_head = self.font_header.render(f"Trickster", True, 'white')
        self.DOT = self.font.render(f"Decrease your \n damage by 100% \n but increase DOT \n damage by 75%", True, 'white')
        self.powerup_level_10 = 1
        self.powerup_10 = [self.DOT_head, self.DOT, self.powerup_level_10]

        #E
        self.DOT2_head = self.font_header.render(f"Quick spread", True, 'white')
        self.DOT2 = self.font.render(f"Decrease DOT \n damage by 50% \n but increase the \n tick rate by \n 70% but decrease \n sustain to \n 1 second", True, 'white')
        self.powerup_level_11 = 1
        self.powerup_11 = [self.DOT2_head, self.DOT2, self.powerup_level_11]

        #E2
        self.DOT3_head = self.font_header.render(f"Lethality", True, 'white')
        self.DOT3 = self.font.render(f"Increase DOT \n damage by 75% \n but decrease the \n tick rate by \n 50% increase \n sustain to \n 3 seconds", True, 'white')
        self.powerup_level_12 = 1
        self.powerup_12 = [self.DOT3_head, self.DOT3, self.powerup_level_12]


        #Not_found
        self.powerup_not_found_head = self.font_header.render(f"No More Powerups (:", True, 'white')
        self.powerup_not_found = self.font.render(f"GG's you are \n now a god", True, "white")
        self.powerup_not_found_level = 1
        self.powerup_not_found_1 = [self.powerup_not_found_head, self.powerup_not_found, self.powerup_not_found_level]

        self.powerup_texts = {
            1 : self.powerup_1,
            2 : self.powerup_2,
            3 : self.powerup_3,
            4 : self.powerup_4,
            5 : self.powerup_5,
            6 : self.powerup_6,
            7 : self.powerup_7,
            8 : self.powerup_8,
            9 : self.powerup_9,
            10 : self.powerup_10,
            11 : self.powerup_11,
            12 : self.powerup_12,
            999 : self.powerup_not_found_1
        }
        
    def select(self):
        #____CHANGE_WITH_NEW_POWERUPS____#
        if [1,3] in self.perks_active:
            del self.powerup_texts[1]
        if [2,3] in self.perks_active:
            del self.powerup_texts[2]
        if [3,3] in self.perks_active:
            del self.powerup_texts[3]
        if [4,3] in self.perks_active:
            del self.powerup_texts[4]
        if [5,3] in self.perks_active:
            del self.powerup_texts[5]
        if [6,3] in self.perks_active:
            del self.powerup_texts[6]
        if [7,3] in self.perks_active:
            del self.powerup_texts[7]
        if [8,3] in self.perks_active:
            del self.powerup_texts[8]
        if [9,3] in self.perks_active:
            del self.powerup_texts[9]
        if [10,1] in self.perks_active:
            del self.powerup_texts[10]
        if [11,1] in self.perks_active:
            del self.powerup_texts[11]
        if [12,1] in self.perks_active:
            del self.powerup_texts[12]

        self.powerup_no = len(self.powerup_texts)

        a = None
        b = None
        c = None

        if self.powerup_no <= 3:
            for key in self.powerup_texts:
                if a is None:
                    a = key
                elif b is None:
                    b = key
                else:
                    c = key
            if a is None:
                a = 999
            if b is None:
                b = 999
            if c is None:
                c = 999         

        elif self.powerup_no == 4:
            for key in self.powerup_texts:
                if key == 999:
                    pass
                else:
                    if a is None:
                        a = key
                    elif b is None:
                        b = key
                    else:
                        c = key
        else:
            keys = list(self.powerup_texts.keys())
            if 999 in keys:
                keys.remove(999)
            random.shuffle(keys)
            a = keys[0]
            b = keys[1]
            c = keys[2]

        

        self.powerup_1_selected = self.powerup_texts[a]
        self.powerup_2_selected = self.powerup_texts[b]
        self.powerup_3_selected = self.powerup_texts[c]

        
    def draw(self):
        WIN.blit(self.surface, (0,0))
        WIN.blit(self.pick_1, (WIDTH//3 - WIDTH//5 - WIDTH//10 + 108, HEIGHT - HEIGHT//1.6 - 200))
        WIN.blit(self.pick_2, (WIDTH//2 - WIDTH//10, HEIGHT - HEIGHT//1.6 - 200))
        WIN.blit(self.pick_3, (WIDTH - WIDTH//5 - WIDTH//10, HEIGHT - HEIGHT//1.6 - 200))

        self.pick_1.fill((0,0,0))
        self.pick_2.fill((0,0,0))
        self.pick_3.fill((0,0,0))

        a = self.pick_1.get_width() - self.powerup_1_selected[0].get_width()
        b = self.pick_2.get_width() - self.powerup_2_selected[0].get_width()
        c = self.pick_3.get_width() - self.powerup_3_selected[0].get_width()

        pick_1_text_adjust = self.pick_1.get_width() - self.powerup_1_selected[1].get_width()
        pick_2_text_adjust = self.pick_2.get_width() - self.powerup_2_selected[1].get_width()
        pick_3_text_adjust = self.pick_3.get_width() - self.powerup_3_selected[1].get_width()
        



        self.pick_1.blit(self.powerup_1_selected[0], (0 + a//2, 30))
        self.pick_1.blit(self.powerup_1_selected[1], (0 + pick_1_text_adjust//2, 150))
        self.pick_2.blit(self.powerup_2_selected[0], (0 + b//2, 30))
        self.pick_2.blit(self.powerup_2_selected[1], (0 + pick_2_text_adjust//2, 150))
        self.pick_3.blit(self.powerup_3_selected[0], (0 + c//2, 30))
        self.pick_3.blit(self.powerup_3_selected[1], (0 + pick_3_text_adjust//2, 150))

    def selected(self, on_perk_1, on_perk_2, on_perk_3):
        power_selected = None
        
        if not (on_perk_1 or on_perk_2 or on_perk_3):
            pass
        else:
            if on_perk_1 and self.powerup_1_selected != self.powerup_texts[999]:
                for key in self.powerup_texts:
                    if self.powerup_texts[key] == self.powerup_1_selected:
                        power_selected = key
            elif on_perk_2 and self.powerup_2_selected != self.powerup_texts[999]:
                for key in self.powerup_texts:
                    if self.powerup_texts[key] == self.powerup_2_selected:
                        power_selected = key
            elif on_perk_3 and self.powerup_3_selected != self.powerup_texts[999]:
                for key in self.powerup_texts:
                    if self.powerup_texts[key] == self.powerup_3_selected:
                        power_selected = key

            if self.powerup_1_selected == self.powerup_texts[999] and self.powerup_2_selected == self.powerup_texts[999] and self.powerup_3_selected == self.powerup_texts[999]:
                pass

            elif power_selected == 1:
                if self.powerup_1[-1] == 1:
                    self.perks_active.append([1,1])
                    self.powerup_level_1 += 1
                    self.powerup_1.remove(self.powerup_1[1])
                if self.powerup_1[-1] == 2:
                    self.perks_active.append([1,2])
                    self.powerup_level_1 += 1
                    self.powerup_1.remove(self.powerup_1[1])
                if self.powerup_1[-1] == 3:
                    self.perks_active.append([1,3])

            elif power_selected == 2:
                if self.powerup_2[-1] == 1:
                    self.perks_active.append([2,1])
                    self.powerup_level_2 += 1
                    self.powerup_2.remove(self.powerup_2[1])
                if self.powerup_2[-1] == 2:
                    self.perks_active.append([2,2])
                    self.powerup_level_2 += 1
                    self.powerup_2.remove(self.powerup_2[1])
                if self.powerup_2[-1] == 3:
                    self.perks_active.append([2,3])

            elif power_selected == 3:
                if self.powerup_3[-1] == 1:
                    self.perks_active.append([3,1])
                    self.powerup_level_3 += 1
                    self.powerup_3.remove(self.powerup_3[1])
                if self.powerup_3[-1] == 2:
                    self.perks_active.append([3,2])
                    self.perks_active.remove([3,1])
                    self.powerup_level_3 += 1
                    self.powerup_3.remove(self.powerup_3[1])
                if self.powerup_3[-1] == 3:
                    self.perks_active.append([3,3])
                    self.perks_active.remove([3,2])

            elif power_selected == 4:
                if self.powerup_4[-1] == 1:
                    self.perks_active.append([4,1])
                    self.powerup_level_4 += 1
                    self.powerup_4.remove(self.powerup_4[1])
                if self.powerup_4[-1] == 2:
                    self.perks_active.append([4,2])
                    self.perks_active.remove([4,1])
                    self.powerup_level_4 += 1
                    self.powerup_4.remove(self.powerup_4[1])
                if self.powerup_4[-1] == 3:
                    self.perks_active.append([4,3])
                    self.perks_active.remove([4,2])

            elif power_selected == 5:
                if self.powerup_5[-1] == 1:
                    self.perks_active.append([5,1])
                    self.powerup_level_5 += 1
                    self.powerup_5.remove(self.powerup_5[1])
                if self.powerup_5[-1] == 2:
                    self.perks_active.append([5,2])
                    self.powerup_level_5 += 1
                    self.powerup_5.remove(self.powerup_5[1])
                if self.powerup_5[-1] == 3:
                    self.perks_active.append([5,3])

            elif power_selected == 6:
                if self.powerup_6[-1] == 1:
                    self.perks_active.append([6,1])
                    self.powerup_level_6 += 1
                    self.powerup_6.remove(self.powerup_6[1])
                if self.powerup_6[-1] == 2:
                    self.perks_active.append([6,2])
                    self.powerup_level_6 += 1
                    self.powerup_6.remove(self.powerup_6[1])
                if self.powerup_6[-1] == 3:
                    self.perks_active.append([6,3])

            elif power_selected == 7:
                if self.powerup_7[-1] == 1:
                    self.perks_active.append([7,1])
                    self.powerup_level_7 += 1
                    self.powerup_7.remove(self.powerup_7[1])
                if self.powerup_7[-1] == 2:
                    self.perks_active.append([7,2])
                    self.powerup_level_7 += 1
                    self.powerup_7.remove(self.powerup_7[1])
                if self.powerup_7[-1] == 3:
                    self.perks_active.append([7,3])
            
            elif power_selected == 8:
                if self.powerup_8[-1] == 1:
                    self.perks_active.append([8,1])
                    self.powerup_level_8 += 1
                    self.powerup_8.remove(self.powerup_8[1])
                if self.powerup_8[-1] == 2:
                    self.perks_active.append([8,2])
                    self.powerup_level_8 += 1
                    self.powerup_8.remove(self.powerup_8[1])
                if self.powerup_8[-1] == 3:
                    self.perks_active.append([8,3])
            
            elif power_selected == 9:
                if self.powerup_9[-1] == 1:
                    self.perks_active.append([9,1])
                    self.powerup_level_9 += 1
                    self.powerup_9.remove(self.powerup_9[1])
                if self.powerup_9[-1] == 2:
                    self.perks_active.append([9,2])
                    self.powerup_level_9 += 1
                    self.powerup_9.remove(self.powerup_9[1])
                if self.powerup_9[-1] == 3:
                    self.perks_active.append([9,3])
            elif power_selected == 10:
                if self.powerup_10[-1] == 1:
                    self.perks_active.append([10,1])
                    self.powerup_level_10 += 1
                    self.powerup_10.remove(self.powerup_10[1])
            elif power_selected == 11:
                if self.powerup_11[-1] == 1:
                    self.perks_active.append([11,1])
                    self.powerup_level_11 += 1
                    self.powerup_11.remove(self.powerup_11[1])
            elif power_selected == 12:
                if self.powerup_12[-1] == 1:
                    self.perks_active.append([12,1])
                    self.powerup_level_12 += 1
                    self.powerup_12.remove(self.powerup_12[1])


            self.powerup_1[-1] = self.powerup_level_1
            self.powerup_2[-1] = self.powerup_level_2
            self.powerup_3[-1] = self.powerup_level_3
            self.powerup_4[-1] = self.powerup_level_4
            self.powerup_5[-1] = self.powerup_level_5
            self.powerup_6[-1] = self.powerup_level_6
            self.powerup_7[-1] = self.powerup_level_7
            self.powerup_8[-1] = self.powerup_level_8
            self.powerup_9[-1] = self.powerup_level_9
            self.powerup_10[-1] = self.powerup_level_10
            self.powerup_11[-1] = self.powerup_level_11
            self.powerup_12[-1] = self.powerup_level_12


        self.powerup_texts = {
            1 : self.powerup_1,
            2 : self.powerup_2,
            3 : self.powerup_3,
            4 : self.powerup_4,
            5 : self.powerup_5,
            6 : self.powerup_6,
            7 : self.powerup_7,
            8 : self.powerup_8,
            9 : self.powerup_9,
            10 : self.powerup_10,
            11 : self.powerup_11,
            12 : self.powerup_12,
            999 : self.powerup_not_found_1
        }
                
    def apply(self, player, gigatified):

        #---------------THIS HAS TO BE FIRST IMPORTANT---------------#
        if [7,1] in self.perks_active:
            if gigatified:
                if [7,1] in self.perks_active:
                    player.dmg *= 1.25
                    player.Big_attack_dmg *= 1.25
                
                if [7,2] in self.perks_active:
                    player.dmg *= 1.5
                    player.Big_attack_dmg *= 1.5
                
                if [7,3] in self.perks_active:
                    player.dmg *= 1.75
                    player.Big_attack_dmg *= 1.75
            else:
                player.dmg = 60 * player.scale
                player.Big_attack_dmg = (60//2) * player.scale


    
        if [1,1] in self.perks_active:
            player.dmg *= 1.2
            if [1,2] in self.perks_active:
                player.dmg *= 1.3
                player.atk_range_y_increase += 0.15
            if [1,3] in self.perks_active:
                player.dmg *= 1.5
                player.atk_range_y_increase += 0.20
                player.atk_range_x_increase += 0.20

        if [2,1] in self.perks_active:
            player.Big_attack_dmg *= 1.3
            if [2,2] in self.perks_active:
                player.Big_attack_dmg *= 1.45
            if [2,3] in self.perks_active:
                player.Big_attack_dmg *= 1.75

        if [3,1] in self.perks_active:
            player.can_burn = True
            player.burn_dmg = 40
            if [3,2] in self.perks_active:
                player.burn_dmg = 70
            if [3,3] in self.perks_active:
                player.burn_dmg = 100
        
        if [4,1] in self.perks_active:
            player.can_poison = True
            player.poison_dmg = 12.5
            player.poison_tick = 30
            if [4,2] in self.perks_active:
                player.poison_dmg = 30
                player.poison_sustain = 120
            if [4,3] in self.perks_active:
                player.poison_dmg = 15
                player.poison_tick = 10

        if [5,1] in self.perks_active:
            player.both_dot_buff = True
            player.both_dot_increase = 1.25
            if [5,2] in self.perks_active:
                player.both_dot_increase = 1.5
            if [5,3] in self.perks_active:
                player.both_dot_increase = 1.75
        
        if [6,1] in self.perks_active:
            player.giant_form_time = player.giant_form_time_base * 1.25
            if [6,2] in self.perks_active:
                player.giant_form_time = player.giant_form_time_base * 1.5
            if [6,3] in self.perks_active:
                player.giant_form_time = player.giant_form_time_base * 1.75


        if [8,1] in self.perks_active:
            player.slash_can_burn = True
            player.slash_burn_dmg = 25
            if [8,2] in self.perks_active:
                player.slash_burn_dmg = 50
            if [8,3] in self.perks_active:
                player.slash_burn_dmg = 70
        
        if [9,1] in self.perks_active:
            player.slash_can_poison = True
            player.slash_poison_dmg = 10
            player.slash_poison_tick = 30
            if [9,2] in self.perks_active:
                player.slash_poison_dmg = 20
                player.slash_poison_sustain = 120
            if [9,3] in self.perks_active:
                player.slash_poison_dmg = 12
                player.slash_poison_tick = 10

        if [10,1] in self.perks_active:
            player.dmg = 0
            player.Big_attack_dmg = 0
            player.slash_poison_dmg *= 1.75
            player.slash_burn_dmg *= 1.75
            player.poison_dmg *= 1.75
            player.burn_dmg *= 1.75

        if [11,1] in self.perks_active:
            player.slash_poison_dmg *= 0.5
            player.slash_burn_dmg *= 0.5
            player.poison_dmg *= 0.5
            player.burn_dmg *= 0.5
            player.burn_tick -= (player.burn_tick/100) * 70
            player.poison_tick -= (player.poison_tick/100) * 70
            player.burn_sustain = 60
            player.poison_sustain = 60
            player.slash_burn_tick -= (player.burn_tick/100) * 70
            player.slash_poison_tick -= (player.poison_tick/100) * 70
            player.slash_burn_sustain = 60
            player.slash_poison_sustain = 60


        if [12,1] in self.perks_active:
            player.slash_poison_dmg *= 1.75
            player.slash_burn_dmg *= 1.75
            player.poison_dmg *= 1.75
            player.burn_dmg *= 1.75
            player.burn_tick += (player.burn_tick/100) * 50
            player.poison_tick += (player.poison_tick/100) * 50
            player.burn_sustain = 60 * 3
            player.poison_sustain = 60 * 3
            player.slash_burn_tick += (player.burn_tick/100) * 50
            player.slash_poison_tick += (player.poison_tick/100) * 50
            player.slash_burn_sustain = 60 * 3
            player.slash_poison_sustain = 60 * 3