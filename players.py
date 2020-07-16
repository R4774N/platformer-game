import arcade
import math, random, os
from settings import *


def load_texture_pair(filename):
    """
    Load a texture pair, with the second being a mirror image.
    """
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, mirrored=True)
    ]

class PlayerCharacter(arcade.Sprite):
    def __init__(self):

        # Set up parent class
        super().__init__()

        # Default to face-right
        self.character_face_direction = RIGHT_FACING

        # Used for flipping between image sequences
        self.cur_texture = 0

        # Track out state
        self.is_jumping = False
        self.climbing = False
        self.is_on_ladder = False
        self.is_attacking = False
        self.is_dead = False
        self.scale = CHARACTER_SCALING

        # Adjust the collision box. Default includes too much empty space
        # side-to-side. Box is centered at sprite center, (0, 0)
        #self.points = [[-22, -64], [22, -64], [22, 28], [-22, 28]]

        # --- Load Textures ---

        # Images from Kenney.nl's Asset Pack 3
        # main_path = ":resources:images/animated_characters/female_adventurer/femaleAdventurer"
        # main_path = ":resources:images/animated_characters/female_person/femalePerson"
        # main_path = ":resources:images/animated_characters/male_person/malePerson"
        # main_path = ":resources:images/animated_characters/male_adventurer/maleAdventurer"
        # main_path = ":resources:images/animated_characters/zombie/zombie"
        # main_path = ":resources:images/animated_characters/robot/robot"
        
        # self.player_sprite = arcade.Sprite(f"{ASSET_PATH}/HeroKnight/HeroKnight/Run/HeroKnight_Run_0.png", CHARACTER_SCALING)

        # Load textures for idle standing
        HERO_KNIGHT_PATH = f"{ASSET_PATH}/HeroKnight/HeroKnight/"
        # self.idle_texture_pair = load_texture_pair(f"{main_path}_idle.png")
        self.idle_textures = []
        for i in range(8):
            texture = load_texture_pair(f"{ASSET_PATH}/HeroKnight/HeroKnight/Idle/HeroKnight_Idle_{i}.png")
            self.idle_textures.append(texture)

        # Load textures for walking
        self.walk_textures = []
        for i in range(10):
            # texture = load_texture_pair(f"{main_path}_walk{i}.png")
            texture = load_texture_pair(f"{ASSET_PATH}/HeroKnight/HeroKnight/Run/HeroKnight_Run_{i}.png")
            self.walk_textures.append(texture)

        #Load textures for attacking
        self.attack_textures = []
        for i in range(6):
            texture = load_texture_pair(f"{ASSET_PATH}/HeroKnight/HeroKnight/Attack1/HeroKnight_Attack1_{i}.png")
            self.attack_textures.append(texture)

        #Load textures for dying
        self.death_textures = []
        for i in range(10):
            texture = load_texture_pair(f"{ASSET_PATH}/HeroKnight/HeroKnight/Death/HeroKnight_Death_{i}.png")
            self.death_textures.append(texture)

        #Load textures for dying
        self.jumping_textures = []
        for i in range(3):
            texture = load_texture_pair(f"{ASSET_PATH}/HeroKnight/HeroKnight/Jump/HeroKnight_Jump_{i}.png")
            self.jumping_textures.append(texture)
    
    def _walk(self):
        self.cur_texture += 1
        if self.cur_texture > 9 * UPDATES_PER_FRAME:
            self.cur_texture = 0
        self.texture = self.walk_textures[self.cur_texture // UPDATES_PER_FRAME][self.character_face_direction]

    def _attack(self):
        self.cur_texture += 1
        if self.cur_texture > 5 * UPDATES_PER_FRAME:
            self.cur_texture = 0
            self.is_attacking = False
        self.texture = self.attack_textures[self.cur_texture // UPDATES_PER_FRAME][self.character_face_direction]

    def _idle(self):
        self.cur_texture += 1
        if self.cur_texture > 7 * UPDATES_PER_FRAME:
            self.cur_texture = 0
        self.texture = self.idle_textures[self.cur_texture // UPDATES_PER_FRAME][self.character_face_direction]
   
    def _jump(self):
        self.cur_texture = 0
        # if self.cur_texture > 2 * UPDATES_PER_FRAME:
        #     self.cur_texture = 0
        #     #self.is_jumping = False
        self.texture = self.jumping_textures[self.cur_texture // UPDATES_PER_FRAME][self.character_face_direction]

    def _death(self):
        self.cur_texture += 1
        if self.cur_texture > 7 * UPDATES_PER_FRAME:
            return
        self.texture = self.death_textures[self.cur_texture // UPDATES_PER_FRAME][self.character_face_direction]
   
    def update_animation(self, delta_time: float = 1/60):

        # Figure out if we need to flip face left or right
        if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        elif self.change_x > 0 and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING

        # Idle animation
        if self.is_dead:
            self._death()
        elif self.is_jumping:
            self._jump()
        elif self.is_attacking:
            self.change_x = 0
            self.change_y = 0
            self._attack()
        elif self.change_x != 0:
            self._walk()
        else:
            self._idle()
        
