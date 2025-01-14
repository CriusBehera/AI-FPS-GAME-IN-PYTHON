from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

window.fullscreen = True  # Set the game to full screen

# Create a player using FirstPersonController
player = FirstPersonController()
player.enabled = False  # Disable player control initially

# Load the environment
ground = Entity(model='plane', texture='grass', scale=64, collider='box')

# Create walls for hiding
walls = []
wall_positions = [(-10, 1, 10), (10, 1, 10), (-10, 1, -10), (10, 1, -10), (0, 1, 15), (0, 1, -15)]
for pos in wall_positions:
    wall = Entity(model='cube', color=color.gray, scale=(2, 2, 0.5), position=pos, collider='box')
    walls.append(wall)

# Create enemies near the edge of the map
enemies = []
for i in range(8):
    x = random.choice([-30, 30])  # Spawn enemies near the left or right edge of the map
    z = random.choice([-30, 30])  # Spawn enemies near the top or bottom edge of the map
    enemy = Entity(model='cube', color=color.red, scale=(1, 2, 1), position=(x, 1, z), collider='box')
    enemies.append(enemy)

# Handle shooting
bullets = []
enemy_bullets = []

player_health = 10  # Player can take 10 hits

# Add a collider to the player
player.collider = 'box'

game_active = False

def start_game():
    global game_active
    player.enabled = True
    game_active = True
    start_button.disable()

def update():
    global player_health, game_active
    
    if not player.enabled or not game_active:
        return
    
    # Exit the game when ESC key is pressed
    if held_keys['escape']:
        application.quit()
    
    # Shooting mechanics
    if mouse.left:
        bullet = Entity(model='cube', color=color.blue, scale=(0.2, 0.2, 0.2), position=player.position + player.forward * 2, collider='box')
        bullet.look_at(player.forward * 50)
        bullet.animate_position(bullet.position + bullet.forward * 50, duration=1, curve=curve.linear)
        bullets.append(bullet)
        destroy(bullet, delay=1)

    # Collision detection for player bullets
    for bullet in bullets:
        for enemy in enemies:
            if bullet.intersects(enemy).hit:
                print("Enemy hit!")
                enemy.color = color.black  # Enemy hit effect
                destroy(enemy)
                enemies.remove(enemy)
                if not enemies:
                    win_game()
                break
    
    # Collision detection for enemy bullets
    for bullet in enemy_bullets:
        if bullet.intersects(player).hit:
            player_health -= 1
            print("Player hit! Health:", player_health)
            destroy(bullet)
            
            if player_health <= 0:
                game_over()

    # Enemy movement towards player
    for enemy in enemies:
        try:
            direction = (player.position - enemy.position).normalized()
            enemy.position += direction * time.dt
        except:
            pass

    # Enemy shooting
    for enemy in enemies:
        try:
            if random.random() < 0.01:  # Randomly fire bullets
                bullet = Entity(model='cube', color=color.red, scale=(0.2, 0.2, 0.2), position=enemy.position + enemy.forward * 2, collider='box')
                bullet.look_at(player.position)
                bullet.animate_position(bullet.position + bullet.forward * 50, duration=1, curve=curve.linear)
                enemy_bullets.append(bullet)
                destroy(bullet, delay=1)
        except:
            pass

def game_over():
    global game_active
    print("Game Over")
    # Display game-over message and clear the screen
    game_active = False
    destroy_all_enemies_and_bullets()
    player.disable()  # Disable player controls
    game_over_text = Text(text='GAME OVER', position=(0,0), origin=(0,0), scale=2, color=color.red)
    application.pause()  # Pause the game

def win_game():
    global game_active
    print("You Won!")
    # Display win message and clear the screen
    game_active = False
    destroy_all_enemies_and_bullets()
    player.disable()  # Disable player controls
    win_text = Text(text='YOU WON!', position=(0,0), origin=(0,0), scale=2, color=color.green)
    application.pause()  # Pause the game

def destroy_all_enemies_and_bullets():
    for enemy in enemies:
        destroy(enemy)
    for bullet in bullets:
        destroy(bullet)
    for bullet in enemy_bullets:
        destroy(bullet)

# Start button
start_button = Button(text='Start Game', color=color.azure, position=(0,0), scale=(0.2,0.1))
start_button.on_click = start_game

app.run()
