#pgzero
import pgzrun
from pgzero import actor, clock
import random
import math

WIDTH = 960
HEIGHT = 540
TITLE = "KuyoMuyo: Bullet Hell Project"
FPS = 30
HAZARD_SPEED = 2

# Player and background
player = actor.Actor("geishukuu", (100, 270))
player.hp = 50
player.ssc = 3

bg = actor.Actor("background_a")


# Boss 1
enemy_1 = actor.Actor("triangle_2", (850, 270))
enemy_1.hp = 300

# Use the available triangle sprite until triangle_3 is supplied.
enemy_1_2 = actor.Actor("triangle_1", (100, 270))
enemy_1_3 = actor.Actor("triangle_1", (500, 270))
enemy_barrier = actor.Actor("enemybarrier", (850, 270))


# Boss 2
enemy_2 = actor.Actor("xeclion_2", (1120, 270))
enemy_2.hp = 500


# Game state
mode = "boss_1"
phase = 1

# Enemy bullet images for each phase (blank uses the default bullet)
PHASE_BULLET_IMAGES = {
    ("boss_1", 1): "blue_bullet",
    ("boss_1", 2): "red_ball",
    ("boss_1", 3): "blackrose",
    ("boss_2", 1): "redknife",
    ("boss_2", 2): "teal_star",
    ("boss_2", 3): ""
}

# Images for the larger phase hazards (blank uses white circles)
PHASE_HAZARD_IMAGES = {
    ("boss_1", 1): "blackovalbullett",
    ("boss_1", 2): "red_musicnote",
    ("boss_1", 3): "red_spear",  # black_spearr is not available.
    ("boss_2", 1): "red_spear",
    ("boss_2", 2): "",
    ("boss_2", 3): ""
}

enemy_bullets = []
player_bullets = []
hazards = []

player_invincible = 0
transition_timer = 0
phase_timer = 0
orbit_angle = 0

boss_2_target_x = 720


# Bomb settings
BOMB_IMAGE = ""  # Add your laser image name later
BOMB_DAMAGE = 100
bomb_frames = 0

bomb_x = 0
bomb_y = 0
bomb_target_x = 0
bomb_target_y = 0


# --------------------------------------------------
# Player shooting
# --------------------------------------------------

def player_shoot():
    if mode not in ("boss_1", "boss_2"):
        return

    bullet = actor.Actor("player_cards")
    bullet.pos = player.pos
    player_bullets.append(bullet)


clock.schedule_interval(player_shoot, 0.15)


# --------------------------------------------------
# Enemy shooting
# --------------------------------------------------

def enemy_shoot():

    if mode == "boss_1":
        shooter = enemy_1
    elif mode == "boss_2":
        shooter = enemy_2
    else:
        return

    image_name = PHASE_BULLET_IMAGES.get(
        (mode, phase), ""
    )

    if image_name == "":
        image_name = "blackovalbullett"

    # Fire three bullets in a spread
    for spread in (-3, 0, 3):

        bullet = actor.Actor(image_name)
        bullet.x = shooter.x
        bullet.y = shooter.y

        bullet.speed_x = random.choice([-9, -8, -7])
        bullet.speed_y = spread + random.choice([-1, 0, 1])

        enemy_bullets.append(bullet)


clock.schedule_interval(enemy_shoot, 1.2)


# --------------------------------------------------
# Bomb attack: press E
# --------------------------------------------------

def use_bomb():
    global bomb_frames
    global bomb_x, bomb_y
    global bomb_target_x, bomb_target_y
    global phase_timer, mode

    if mode not in ("boss_1", "boss_2"):
        return

    if player.ssc <= 0 or bomb_frames > 0:
        return

    # Consume one spell card
    player.ssc -= 1

    bomb_x = int(player.x)
    bomb_y = int(player.y)

    # Damage the active boss
    if mode == "boss_1":
        bomb_target_x = int(enemy_1.x)
        bomb_target_y = int(enemy_1.y)
        enemy_1.hp = max(0, enemy_1.hp - BOMB_DAMAGE)

    else:
        bomb_target_x = int(enemy_2.x)
        bomb_target_y = int(enemy_2.y)
        enemy_2.hp = max(0, enemy_2.hp - BOMB_DAMAGE)

    # Clear hazards and enemy projectiles
    enemy_bullets[:] = []
    hazards[:] = []
    phase_timer = 0

    # Show laser for a short time
    bomb_frames = 18

    # Handle a boss defeated by the bomb
    if mode == "boss_1" and enemy_1.hp <= 0:
        start_boss_2()

    elif mode == "boss_2" and enemy_2.hp <= 0:
        player_bullets[:] = []
        mode = "clear"


# Draw the bomb laser
def draw_bomb():
    if bomb_frames <= 0:
        return

    # Use your image once you have added it
    if BOMB_IMAGE != "":
        beam = actor.Actor(
            BOMB_IMAGE,
            (
                (bomb_x + bomb_target_x) // 2,
                (bomb_y + bomb_target_y) // 2
            )
        )

        beam.angle = int(math.degrees(math.atan2(
            bomb_target_y - bomb_y,
            bomb_target_x - bomb_x
        )))

        beam.draw()
        return

    # Temporary laser effect if the image name is blank
    dx = bomb_target_x - bomb_x
    dy = bomb_target_y - bomb_y
    length = math.sqrt(dx * dx + dy * dy)

    if length == 0:
        return

    px = -dy / length
    py = dx / length

    for offset in range(-12, 13, 3):
        start = (
            int(bomb_x + px * offset),
            int(bomb_y + py * offset)
        )

        end = (
            int(bomb_target_x + px * offset),
            int(bomb_target_y + py * offset)
        )

        if offset in (-3, 0, 3):
            color = "white"
        else:
            color = (0, 255, 255)

        screen.draw.line(start, end, color)


def on_key_down(key):
    if key == keys.E:
        use_bomb()


# --------------------------------------------------
# Boss 2 entrance
# --------------------------------------------------

def start_boss_2():
    global mode, transition_timer

    mode = "transition"
    transition_timer = 0

    enemy_bullets[:] = []
    player_bullets[:] = []
    hazards[:] = []

    enemy_2.pos = (1120, 270)
    enemy_2.hp = 500


def boss_2_transition():
    global mode, transition_timer
    global phase, phase_timer

    transition_timer += 1

    if enemy_2.x > boss_2_target_x:
        enemy_2.x -= 12

        if enemy_2.x < boss_2_target_x:
            enemy_2.x = boss_2_target_x

    elif transition_timer >= 60:
        mode = "boss_2"
        phase = 1
        phase_timer = 0
        make_phase()


# --------------------------------------------------
# Phase hazard system
# --------------------------------------------------

def add_hazard(x, y, dx, dy, size):
    hazards.append([x, y, dx, dy, size])


def make_phase():
    hazards[:] = []

    # Boss 1
    if mode == "boss_1":

        # Phase 1: falling hazards
        if phase == 1:
            for x in range(80, 961, 110):
                add_hazard(x, -20, 0, 3, 7)

        # Phase 2: crossing patterns
        elif phase == 2:
            for i in range(7):
                add_hazard(i * 150, -20, 2, 3, 8)
                add_hazard(960 - i * 150, -20, -2, 3, 8)

        # Phase 3: faster horizontal patterns
        elif phase == 3:
            for i in range(8):
                add_hazard(-20, 70 + i * 55, 5, 0, 8)
                add_hazard(980, 100 + i * 55, -5, 0, 8)

    # Boss 2: jester patterns
    elif mode == "boss_2":

        # Phase 1: diagonal patterns
        if phase == 1:
            for i in range(6):
                dx = 3 if i % 2 == 0 else -3
                add_hazard(120 + i * 140, 100, dx, 3, 8)

        # Phase 2: radial patterns
        elif phase == 2:
            for i in range(12):
                angle = math.radians(i * 360 / 16)

                dx = int(math.cos(angle) * 4)
                dy = int(math.sin(angle) * 4)

                add_hazard(
                    int(enemy_2.x),
                    int(enemy_2.y),
                    dx,
                    dy,
                    9
                )

        # Phase 3: fast patterns from different sides
        elif phase == 3:
            for i in range(16):
                side = i % 4

                if side == 0:
                    add_hazard(-20, i * 35, 6, 1, 9)
                elif side == 1:
                    add_hazard(980, i * 35, -6, 1, 9)
                elif side == 2:
                    add_hazard(i * 60, -20, 1, 6, 9)
                else:
                    add_hazard(i * 60, 560, 1, -6, 9)


def update_hazards():
    for h in hazards[:]:
        h[0] += h[2] * HAZARD_SPEED
        h[1] += h[3] * HAZARD_SPEED

        if (
            h[0] < -50 or h[0] > WIDTH + 50
            or h[1] < -50 or h[1] > HEIGHT + 50
        ):
            hazards.remove(h)


def draw_hazards():
    image_name = PHASE_HAZARD_IMAGES.get((mode, phase), "")

    for h in hazards:
        x = int(h[0])
        y = int(h[1])

        if image_name != "":
            hazard_image = actor.Actor(image_name, (x, y))
            hazard_image.draw()
        else:
            screen.draw.filled_circle(
                (x, y),
                h[4],
                "white"
            )


# Change phases as the boss loses HP
def check_phase():
    global phase, phase_timer

    if mode == "boss_1":
        if enemy_1.hp > 200:
            new_phase = 1
        elif enemy_1.hp > 100:
            new_phase = 2
        else:
            new_phase = 3

    elif mode == "boss_2":
        if enemy_2.hp > 333:
            new_phase = 1
        elif enemy_2.hp > 166:
            new_phase = 2
        else:
            new_phase = 3

    else:
        return

    if new_phase != phase:
        phase = new_phase
        phase_timer = 0
        make_phase()


# --------------------------------------------------
# Move bullets
# --------------------------------------------------

def move_bullets():
    for bullet in player_bullets[:]:
        bullet.x += 20

        if bullet.x > WIDTH:
            player_bullets.remove(bullet)

    for bullet in enemy_bullets[:]:
        bullet.x += bullet.speed_x
        bullet.y += bullet.speed_y

        if (
            bullet.x < -50 or bullet.x > WIDTH + 50
            or bullet.y < -50 or bullet.y > HEIGHT + 50
        ):
            enemy_bullets.remove(bullet)


# --------------------------------------------------
# Collisions
# --------------------------------------------------

def collisions():
    global mode, player_invincible

    # Player bullets vs Boss 1
    if mode == "boss_1":
        for bullet in player_bullets[:]:
            if bullet.colliderect(enemy_1):
                player_bullets.remove(bullet)
                enemy_1.hp -= 1

        if enemy_1.hp <= 0:
            enemy_1.hp = 0
            start_boss_2()
            return

    # Player bullets vs Boss 2
    elif mode == "boss_2":
        for bullet in player_bullets[:]:
            if bullet.colliderect(enemy_2):
                player_bullets.remove(bullet)
                enemy_2.hp -= 1

        if enemy_2.hp <= 0:
            enemy_2.hp = 0
            enemy_bullets[:] = []
            player_bullets[:] = []
            hazards[:] = []
            mode = "clear"
            return

    # Player vs boss, enemy projectiles, and hazards
    if player_invincible <= 0 and mode in ("boss_1", "boss_2"):
        hit = False

        if mode == "boss_1":
            if (
                player.colliderect(enemy_1)
                or player.colliderect(enemy_1_2)
                or player.colliderect(enemy_1_3)
            ):
                hit = True

        elif mode == "boss_2":
            if player.colliderect(enemy_2):
                hit = True

        if not hit:
            for bullet in enemy_bullets[:]:
                if player.colliderect(bullet):
                    enemy_bullets.remove(bullet)
                    hit = True
                    break

        if not hit:
            for h in hazards:
                dx = player.x - h[0]
                dy = player.y - h[1]

                if dx * dx + dy * dy < (18 + h[4]) ** 2:
                    hit = True
                    break

        if hit:
            player.hp -= 1
            player_invincible = 30

    # Game over
    if player.hp <= 0:
        player.hp = 0
        enemy_bullets[:] = []
        player_bullets[:] = []
        hazards[:] = []
        mode = "game_over"


# --------------------------------------------------
# Draw
# --------------------------------------------------

def draw():
    bg.draw()

    if mode == "boss_1":
        player.draw()
        enemy_1.draw()
        enemy_1_2.draw()
        enemy_1_3.draw()
        enemy_barrier.draw()

        screen.draw.text(
            "BOSS 1",
            (20, 90),
            fontsize=22,
            color="white"
        )

        screen.draw.text(
            "HP: " + str(enemy_1.hp),
            (820, 20),
            fontsize=20,
            color="white"
        )

    elif mode == "transition":
        player.draw()
        enemy_2.draw()

        screen.draw.text(
            "WARNING",
            center=(480, 100),
            fontsize=45,
            color="white"
        )

        screen.draw.text(
            "A new boss approaches!",
            center=(480, 150),
            fontsize=22,
            color="white"
        )

    elif mode == "boss_2":
        player.draw()
        enemy_2.draw()

        screen.draw.text(
            "JESTER BOSS",
            (20, 90),
            fontsize=22,
            color="white"
        )

        screen.draw.text(
            "HP: " + str(enemy_2.hp),
            (820, 20),
            fontsize=20,
            color="white"
        )

    elif mode == "game_over":
        screen.draw.text(
            "GAME OVER",
            center=(480, 230),
            fontsize=50,
            color="white"
        )

        screen.draw.text(
            "Click to restart",
            center=(480, 310),
            fontsize=24,
            color="white"
        )

    elif mode == "clear":
        screen.draw.text(
            "STAGE CLEAR!",
            center=(480, 230),
            fontsize=50,
            color="white"
        )

        screen.draw.text(
            "Click to play again",
            center=(480, 310),
            fontsize=24,
            color="white"
        )

    # Bullets and hazards
    if mode in ("boss_1", "boss_2"):
        for bullet in player_bullets:
            bullet.draw()

        for bullet in enemy_bullets:
            bullet.draw()

        draw_hazards()

        screen.draw.text(
            "PHASE " + str(phase),
            (440, 25),
            fontsize=20,
            color="white"
        )

    # Bomb laser
    if bomb_frames > 0:
        draw_bomb()

        # Player HUD: show one icon and its count
    if mode in ("boss_1", "boss_2", "transition"):

        # HP
        heart = actor.Actor("pink_heart")
        heart.pos = (25, 20)
        heart.draw()

        screen.draw.text(
            "x " + str(player.hp),
            (45, 10),
            fontsize=22,
            color="white"
        )

        # Bombs / spell cards
        star = actor.Actor("green_starr")
        star.pos = (25, 55)
        star.draw()

        screen.draw.text(
            "x " + str(player.ssc),
            (45, 45),
            fontsize=22,
            color="white"
        )


# --------------------------------------------------
# Update
# --------------------------------------------------

def update(dt):
    global player_invincible
    global phase_timer
    global orbit_angle
    global bomb_frames

    if player_invincible > 0:
        player_invincible -= 1

    if bomb_frames > 0:
        bomb_frames -= 1

    if mode == "boss_1":
        move_bullets()
        update_hazards()
        collisions()

        if mode == "boss_1":
            check_phase()

            phase_timer += 1
            if phase_timer >= 120:
                phase_timer = 0
                make_phase()

            # Rotate and orbit Boss 1's triangles
            enemy_barrier.angle += 10
            enemy_1_2.angle += 10
            enemy_1_3.angle -= 10

            orbit_angle += 3
            angle = math.radians(orbit_angle)

            enemy_1_2.x = int(
                enemy_1.x + math.cos(angle) * 120
            )
            enemy_1_2.y = int(
                enemy_1.y + math.sin(angle) * 120
            )

            enemy_1_3.x = int(
                enemy_1.x + math.cos(angle + math.pi) * 180
            )
            enemy_1_3.y = int(
                enemy_1.y + math.sin(angle + math.pi) * 180
            )

    elif mode == "transition":
        boss_2_transition()

    elif mode == "boss_2":
        move_bullets()
        update_hazards()
        collisions()

        if mode == "boss_2":
            check_phase()

            phase_timer += 1
            if phase_timer >= 120:
                phase_timer = 0
                make_phase()


# --------------------------------------------------
# Mouse controls
# --------------------------------------------------

def on_mouse_move(pos):
    if mode in ("boss_1", "boss_2", "transition"):
        player.pos = pos

        if player.x < 20:
            player.x = 20
        if player.x > WIDTH - 20:
            player.x = WIDTH - 20
        if player.y < 20:
            player.y = 20
        if player.y > HEIGHT - 20:
            player.y = HEIGHT - 20


# --------------------------------------------------
# Restart
# --------------------------------------------------

def on_mouse_down(button, pos):
    global mode, phase, phase_timer
    global player_invincible, bomb_frames

    if mode in ("game_over", "clear"):
        player.hp = 15
        player.ssc = 3
        player.pos = (100, 270)

        enemy_1.hp = 300
        enemy_2.hp = 500
        enemy_2.pos = (1120, 270)

        enemy_bullets[:] = []
        player_bullets[:] = []
        hazards[:] = []

        phase = 1
        phase_timer = 0
        player_invincible = 0
        bomb_frames = 0
        mode = "boss_1"

        make_phase()


# Start Boss 1 Phase 1
make_phase()

pgzrun.go()
