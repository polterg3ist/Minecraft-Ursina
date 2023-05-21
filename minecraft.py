from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController


class Game(Entity):
    def __init__(self):
        super().__init__()

        # models
        self.block_model = "assets/block"

        # game textures
        self.grass_texture = load_texture('assets/grass_block.png')
        self.stone_texture = load_texture('assets/stone_block.png')
        self.brick_texture = load_texture('assets/brick_re.png')
        self.dirt_texture = load_texture('assets/dirt_block.png')
        self.sky_texture = load_texture('assets/skybox.png')
        self.arm_texture = load_texture('assets/arm_texture.png')

        # audio
        self.punch_sound = Audio('assets/punch_sound.wav', loop=False, autoplay=False)

        # player
        self.player = FirstPersonController()

        # sky
        self.sky = Sky(sky_texture=self.sky_texture)

        # hand
        self.hand = Hand(arm_texture=self.arm_texture)

        # item selection
        self.picked_block = 1
        self.blocks = {
            1: self.grass_texture,
            2: self.stone_texture,
            3: self.brick_texture,
            4: self.dirt_texture
        }

    def update(self):
        # preventing player from endless fall
        if self.player.y < -15:
            self.player.position = Vec3(0, 0, 0)

        # hand animation
        if held_keys['left mouse'] or held_keys['right mouse']:
            self.hand.active()
        else:
            self.hand.passive()

        # item selection
        if held_keys['1']: self.picked_block = 1
        if held_keys['2']: self.picked_block = 2
        if held_keys['3']: self.picked_block = 3
        if held_keys['4']: self.picked_block = 4

    def get_block_texture(self):
        return self.blocks[self.picked_block]

    def play_sound(self, sound):
        sound.play()

    def create_world(self):
        for z in range(30):
            for x in range(30):
                voxel = Voxel(get_texture=self.get_block_texture,
                              play_punch_sound=lambda: self.play_sound(self.punch_sound),
                              model=self.block_model,
                              position=(x, 0, z))


class Voxel(Button):
    def __init__(self, get_texture, play_punch_sound, model, position=(0, 0, 0)):
        self.get_texture = get_texture
        self.play_punch_sound = play_punch_sound
        self.block_model = model

        super().__init__(
            parent=scene,
            position=position,
            model=self.block_model,
            origin_y=0.5,
            texture=self.get_texture(),
            color=color.color(0, 0, random.uniform(0.9, 1)),
            highlight_color=color.light_gray,
            scale=0.5
        )

    def input(self, key):
        if self.hovered:
            if key == 'left mouse down':
                self.play_punch_sound()
                position = self.position + mouse.normal
                voxel = Voxel(get_texture=self.get_texture,
                              play_punch_sound=self.play_punch_sound,
                              model=self.block_model,
                              position=position)

            if key == 'right mouse down':
                self.play_punch_sound()
                destroy(self)


class Sky(Entity):
    def __init__(self, sky_texture):
        super().__init__(
            parent=scene,
            model='sphere',
            texture=sky_texture,
            scale=150,
            double_sided=True
        )


class Hand(Entity):
    def __init__(self, arm_texture):
        super().__init__(
            parent=camera.ui,
            model='assets/arm',
            texture=arm_texture,
            scale=0.2,
            rotation=Vec3(150, -15, 0),
            position=Vec2(0.4, -0.7)
        )

    def active(self):
        self.position = Vec2(0.3, -0.6)

    def passive(self):
        self.position = Vec2(0.4, -0.7)


# initialize
app = Ursina()
game = Game()

# general
#window.fps_counter.visible = False
window.exit_button.visible = False

# running the game
game.create_world()
app.run()

