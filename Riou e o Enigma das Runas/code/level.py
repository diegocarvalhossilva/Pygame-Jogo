import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug
from support import *
from random import choice
from weapon import Weapon
from ui import UI
from enemy import Enemy

class Level:
    def __init__(self):

        self.display_surface = pygame.display.get_surface()
        
        #sprites
        self.visible_sprites = YSortCameraGroup()
        self.obstacles_sprites = pygame.sprite.Group()

        self.current_attack = None

        self.create_map()

        #interface
        self.ui = UI()

    def create_map(self):
        layouts = {
            'boundary': import_csv_layout('../map/TileMap_FloorBlocks.csv'),
            'grass': import_csv_layout('../map/TileMap_Grass.csv'),
            'object': import_csv_layout('../map/TileMap_Objects.csv'),
            'entities': import_csv_layout('../map/TileMap_Entities.csv')
        }

        graphics = {
            'grass': import_folder('../graphics/grass'),
            'objects': import_folder('../graphics/objects')
        }

        for style, layout in layouts.items():
            for row_index,row in enumerate (layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x,y), [self.obstacles_sprites], 'invisible')

                        if style == 'grass': #Cria os tiles de grama em lugares aleatórios
                            random_grass_image = choice(graphics['grass'])
                            Tile((x,y),[self.visible_sprites,self.obstacles_sprites],'grass', random_grass_image)

                        if style == 'object': #Cria os tiles de objeto
                            surf = graphics['objects'][int(col)]
                            Tile((x,y),[self.visible_sprites,self.obstacles_sprites],'object',surf)

                        if style == 'entities':
                            if col == '17':
                                self.player = Player(
                                    (x,y),
                                    [self.visible_sprites],
                                    self.obstacles_sprites,
                                    self.create_attack,
                                    self.destroy_attack,
                                    self.create_magic
                                )

                            else:
                                if col == '18': monster_name = 'bamboo'
                                elif col == '19': monster_name = 'spirit'
                                elif col == '20': monster_name = 'squid'
                                elif col == '21': monster_name = 'raccoon'
                                elif col == '22': monster_name = 'toad'
                                else: monster_name = 'toad_king'

                                Enemy(monster_name,(x,y),[self.visible_sprites],self.obstacles_sprites)

    def create_attack(self):
        self.current_attack = Weapon(self.player,[self.visible_sprites])

    def create_magic(self,style,strenght,cost):
        print(style)
        print(strenght)
        print(cost)

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def run(self):
        #atualiza a tela e renderiza os sprites
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.visible_sprites.enemy_update(self.player)
        self.ui.display(self.player)

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        #Cria o chão
        self.floor_surf = pygame.image.load('../graphics/tilemap/ground.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))

    def custom_draw(self,player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        #Desenha o chão
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        #for sprite in self.sprites():
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image,offset_pos) #A imagem é desenhada no retângulo do sprite

    def enemy_update(self,player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite,'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)