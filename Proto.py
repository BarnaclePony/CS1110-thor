"""
This code is used to prototype some features of the game by Nick Chandler and Reza Mirzaiee


Here is a general run-down of the game we're gonna make:

- top-down hack n slash where you play as thor with a hammer
- throwing the hammer pushes you back + pushes enemies back
- Hold arrow keys to charge hammer
- you can gravitate towards hammer when it is thrown.
- random enemy generation
- damage dealt counter = score
- player is fully animated
- most animations hand-made
- want to incorporate sounds if we have time / engine support

Notes:
    - make thor walk slower with hammer, reduce animation speed.
    - figure out how to add sounds
    - make special attack for when connecting with hammer if space is pressed.
    - more speed = more damage


rmm3ya.

"""
import pygame
import gamebox   # gamebox written by Luther Tychonievich
import math

CAMERA_WIDTH, CAMERA_HEIGHT = 800, 600
BOX_WIDTH, BOX_HEIGHT = 10, 10
walksprite_frame = 0
framecountforplayerwalk = 0
camera = gamebox.Camera(CAMERA_WIDTH, CAMERA_HEIGHT)  # size of window and camera points to the center
player = gamebox.from_image(camera.x, camera.y,
                            gamebox.load_sprite_sheet("/Users/rezamirzaiee/Desktop/GAME/Graphics/chara5.png", 8, 12)[1])

hammer = gamebox.from_color(player.x, player.y, "black", 10, 10)

hammer_thrown = False
has_stood = False
playerdirection = gamebox.from_image(camera.x, camera.y,
                            gamebox.load_sprite_sheet("/Users/rezamirzaiee/Desktop/GAME/Graphics/chara5.png", 8, 12)[1])
player_xspeed = 0
player_yspeed = 0
hammer_xspeed = 0
hammer_yspeed = 0
hammer_air = { 'hammer_xspeed_air': 0, 'hammer_yspeed_air': 0}

power = 0
# center gamebox x, center gamebox y, color, width of gamebox, height of gamebox



power_hud = gamebox.from_color(camera.x - 280, camera.y - 280, "purple", 205, 10)
power_hud_fill_x = 1
power_hud_fill_y = 8
power_hud_fill = gamebox.from_color(camera.x - 280, camera.y - 280, "black", power_hud_fill_x, power_hud_fill_y)


def hammer_mechanics(keys):
    global player, movement_vector, walksprite_frame, framecountforplayerwalk, playerdirection, player_xspeed, \
        player_yspeed, has_stood, hammer_thrown, power, power_hud_fill_x, hammer_xspeed, hammer_yspeed,\
        hammer_air

    if power > 180 and pygame.K_l not in keys \
            and pygame.K_j not in keys \
            and pygame.K_i not in keys \
            and pygame.K_k not in keys:
        power = 0
        hammer_thrown = True




    if hammer_thrown is True:
        hammer_xspeed = hammer_air['hammer_xspeed_air']
        hammer_yspeed = hammer_air['hammer_yspeed_air']


        hammer.x += hammer_xspeed
        hammer.y += hammer_yspeed

        if hammer.x != player.x or hammer.x != player.y:
            hammer.x

        camera.draw(hammer)
    else:
        hammer_yspeed, hammer_xspeed = 0, 0
        hammer.x, hammer.y = player.x, player.y

    camera.draw(power_hud)
    camera.draw(power_hud_fill)


def controls(keys):

    global player, movement_vector, walksprite_frame, framecountforplayerwalk, playerdirection, player_xspeed,\
        player_yspeed, has_stood, hammer_thrown, power, power_hud_fill_x

    player_h_sprite = gamebox.load_sprite_sheet("/Users/rezamirzaiee/Desktop/GAME/Graphics/hammer_run.png", 4, 3)
    player_h_charge_sprite = gamebox.load_sprite_sheet("/Users/rezamirzaiee/Desktop/GAME/Graphics/hammer_charge.png", 4, 3)
    playerstand_h_sprite = gamebox.load_sprite_sheet("/Users/rezamirzaiee/Desktop/GAME/Graphics/hammer_stand.png", 4, 3)
    player_sprite = gamebox.load_sprite_sheet("/Users/rezamirzaiee/Desktop/GAME/Graphics/nohammer_run.png", 4, 3)
    player = playerdirection
    player.x += player_xspeed
    player.y += player_yspeed

    if hammer_thrown is False:
        player_sprite_type = player_h_sprite

    if hammer_thrown is True:
        player_sprite_type = player_sprite

    if pygame.K_l in keys \
            or pygame.K_j in keys \
            or pygame.K_i in keys \
            or pygame.K_k in keys:
        player_sprite_type = player_h_charge_sprite

        playerdirection = gamebox.from_image(player.x, player.y, player_sprite_type[walksprite_frame])
    hammer_facing_up = player.x + 2, player.y - 4
    hammer_facing_down = player.x - 2, player.y + 4
    hammer_facing_left = player.x - 4, player.y + 2
    hammer_facing_right = player.x + 4, player.y - 2

    player_face_up = gamebox.from_image(player.x, player.y, player_sprite_type[9 + walksprite_frame])
    player_face_down = gamebox.from_image(player.x, player.y, player_sprite_type[walksprite_frame])
    player_face_left = gamebox.from_image(player.x, player.y, player_sprite_type[3 + walksprite_frame])
    player_face_right = gamebox.from_image(player.x, player.y, player_sprite_type[6 + walksprite_frame])

    framecountforplayerwalk += 1

    if framecountforplayerwalk > 1000:
        framecountforplayerwalk = 0

    if framecountforplayerwalk % 5 == 0:

        if walksprite_frame == 0 and has_stood is True:
            walksprite_frame = 1
            has_stood = not has_stood
        elif walksprite_frame == 1 and has_stood is False:
            walksprite_frame = 0
        elif walksprite_frame == 0 and has_stood is False:
            walksprite_frame = 2
        elif walksprite_frame == 2:
            walksprite_frame = 0
            has_stood = not has_stood

    if pygame.K_w in keys:
        playerdirection = player_face_up
        player_yspeed = -4

    elif pygame.K_s in keys:
        playerdirection = player_face_down
        player_yspeed = 4

    elif .1 > player_yspeed > -.1:
        player_yspeed = 0

    elif player_yspeed != 0 and player_yspeed > -.1:
      #  if player.xspeed > 0:
     #       player = gamebox.from_image(player.x, player.y, player_h_graphic[23 + (walkframe)])
     #   elif player.xspeed < 0:
     #       player = gamebox.from_image(player.x, player.y, player_h_graphic[11 + (walkframe)])

        player_yspeed *= .9

    elif player_yspeed != 0 and player_yspeed < .1:
   #     if player.xspeed > 0:
    #        player = gamebox.from_image(player.x, player.y, player_h_graphic[23 + (walkframe)])
    #    elif player.xspeed < 0:
    #        player = gamebox.from_image(player.x, player.y, player_h_graphic[11 + (walkframe)])

        player_yspeed *= .9

    else:
        player_yspeed = 0

    if player_xspeed < 2 or player_xspeed > -2:

        if pygame.K_a in keys:
            if abs(player_xspeed) >= abs(player_yspeed):
                playerdirection = player_face_left

            player_xspeed = -4

        elif pygame.K_d in keys:

            if abs(player_xspeed) >= abs(player_yspeed):
                playerdirection = player_face_right

            player_xspeed = 4
        elif .1 > player_xspeed > -.1:
            player_xspeed = 0

        elif player_xspeed > .1:
            player_xspeed *= .9

        elif player_xspeed < -.1:
            player_xspeed *= .9

        else:

            player_xspeed = 0

    if pygame.K_l in keys \
            or pygame.K_j in keys \
            or pygame.K_i in keys \
            or pygame.K_k in keys:


        if pygame.K_l in keys:
            hammer_xspeed = 10 + player_xspeed * 2.5
            hammer_yspeed = player_yspeed * .8
            hammer_air['hammer_xspeed_air'] = hammer_xspeed
            hammer_air['hammer_yspeed_air'] = hammer_yspeed
            if pygame.K_j in keys:
                keys.remove(pygame.K_j)



        if pygame.K_j in keys:
            hammer_xspeed = -10 + player_xspeed * 2.5
            hammer_yspeed = player_yspeed * .8
            hammer_air['hammer_xspeed_air'] = hammer_xspeed
            hammer_air['hammer_yspeed_air'] = hammer_yspeed
            if pygame.K_l in keys:
                keys.remove(pygame.K_l)

        # else:
        # hammer_xspeed = hammer_air['hammer_xspeed_air']

        if pygame.K_i in keys:
            hammer_yspeed = 10 + player_yspeed * 2.5
            hammer_xspeed = player_xspeed * .8
            hammer_air['hammer_xspeed_air'] = hammer_xspeed
            hammer_air['hammer_yspeed_air'] = hammer_yspeed
            if pygame.K_k in keys:
                keys.remove(pygame.K_k)

        if pygame.K_k in keys:
            hammer_yspeed = -10 + player_yspeed * 2.5
            hammer_xspeed = player_xspeed * .8
            hammer_air['hammer_xspeed_air'] = hammer_xspeed
            hammer_air['hammer_yspeed_air'] = hammer_yspeed
            if pygame.K_i in keys:
                keys.remove(pygame.K_i)

        # else:
        # hammer_yspeed = hammer_air['hammer_yspeed_air']

        power += 2

        if power_hud_fill_x <= 200:
            power_hud_fill_x += 2
            power_hud_fill.size = 2 + power_hud_fill_x, 10

        power_hud_fill.color = 'orange'

    # elif power >= 1:

      #  power *= .9

    else:

        power_hud_fill_x = 0
        power_hud_fill.size = 2 + power_hud_fill_x, 10
        power_hud_fill_x = 1
        power_hud_fill.color = 'black'
    if power > 0:
        None
        
enemies = {}
Player_HP = 100
Player_HP_bar = gamebox.from_color(CAMERA_WIDTH-200, 100, "black", 200, 10)
Player_HP_bar.right = CAMERA_WIDTH
enemy_counter = 1
health_bars = []
counter = 0
def generate_enemy():
    """
    Makes an enemy at a random location
    enemies are blue squares as a placeholder (will change later)
    Will change later so enemies cant spawn in lava
    might add health bars if i can figure that out

    """
    global enemy_counter
    global health_bars
    enemy_name = "enemy " + str(enemy_counter)
    enemies[enemy_name] = [gamebox.from_color(random.randint(0, 800), random.randint(0, 600), "blue", 20, 20), 100]
    enemy_counter += 1


def enemy_chase():
    """Makes enemies chase the player"""
    enemy_speed = 2
    for enemy in enemies.values():
        if type(enemy) != str:
            if player.x > enemy[0].x:
                enemy[0].x += enemy_speed
            if player.x < enemy[0].x:
                enemy[0].x -= enemy_speed
            if player.y > enemy[0].y:
                enemy[0].y += enemy_speed
            if player.y < enemy[0].y:
                enemy[0].y -= enemy_speed


def enemy_death():
    """
    Not possible to delete values in a for loop so enemy gameboxes are changed to just be the string "Dead" when dead
    """
    for enemy in enemies:
        if type(enemies[enemy]) != str:
            if enemies[enemy][1] <= 0:
                enemies[enemy] = "Dead"


def damage():
    global Player_HP
    """

    This will need a lot of changing in the future
    Made enemies take damage when they touch the hammer to test how lava will work
    Still have to add in Player health/damage
    Damage might have to be the last thing I add (need code for hammer throws and stuff like that first

    """
    for enemy in enemies.values():
        if type(enemy) != str:
            if hammer.touches(enemy[0]):
                enemy[1] -= 10
            if enemy[0].touches(player):
                Player_HP -= 1
    if hammer.touches(player):
        Player_HP -= 3


Player_HP_bar_fill = gamebox.from_color(CAMERA_WIDTH-200, 100, "purple", Player_HP * 1.99, 8)
Player_HP_bar_fill.right = CAMERA_WIDTH


def fix_overlap():
    """ enemies cannot walk inside of each other """
    for enemy in enemies.values():
        if type(enemy) != str:
            for villain in enemies.values():
                if type(villain) != str:
                    if enemy[0].touches(villain[0]):
                        villain[0].move_both_to_stop_overlapping(enemy[0])


def lose_health():
    global Player_HP_bar_fill
    Player_HP_bar_fill = gamebox.from_color(CAMERA_WIDTH-200, 100, "purple", Player_HP * 1.99, 8)
    Player_HP_bar_fill.left = Player_HP_bar.left + 1
 

def tick(keys):

    global power
    global power_hud, power_hud_fill, power_hud_fill_x, power_hud_fill_y

    camera.clear("red")         # set a red background color

    # draw gamebox to buffer, a memory representation of window





    controls(keys)
    hammer_mechanics(keys)
    camera.draw(player)
    # camera.x -= 1.33
        if counter == 0:
        for i in range(5):
            generate_enemy()
    counter += 1
    enemy_chase()
    damage()
    enemy_death()
    lose_health()
    for enemy in enemies.values():
        if type(enemy) != str:
            camera.draw(enemy[0])
    fix_overlap()
    for item in health_bars:
        camera.draw(item)
    walk_controls(keys)
    if Player_HP > 0:
        camera.draw(player)
        print(Player_HP)
    else:
        print('YOU LOSE')
    camera.draw(Player_HP_bar)
    camera.draw(Player_HP_bar_fill)
    camera.display()    # draw the buffer to the window

TICKS_PER_SECOND = 60


gamebox.timer_loop(TICKS_PER_SECOND, tick)
