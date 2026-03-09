from ursina import *
from game.textures import blocks as BLOCK_TEXTURES
from game.graphics.particles import spawn_particles

class Voxel(Button):
    """Classe representando um bloco no mundo"""
    
    def __init__(self, position=(0,0,0), texture=None, block_type="grass", parent=None):
        if texture is None:
            texture = BLOCK_TEXTURES.get("grass")
        
        super().__init__(
            parent=parent,
            position=position,
            model='cube',
            origin_y=0.5,
            texture=texture,
            color=color.white,
            scale=1,
            collider='box',
            highlight_color=color.lime
        )
        
        self.block_type = block_type
        self.texture_ref = texture
    
    def input(self, key):
        """Gerencia interação com o bloco"""
        if self.hovered:
            # Quebrar bloco (botão esquerdo)
            if key == 'left mouse down':
                self.break_block()
            
            # Colocar bloco (botão direito)
            elif key == 'right mouse down':
                self.place_block()
    
    def break_block(self):
        """Quebra o bloco"""
        # Criar partículas
        spawn_particles(
            position=self.position,
            count=15,
            color=self.color,
            scale=0.05,
            spread=1.0,
            lifetime=0.5,
            gravity=True
        )
        
        # Tocar som (você pode adicionar sons)
        # Audio('break_sound.wav', pitch=random.uniform(0.9, 1.1))
        
        destroy(self)
    
    def place_block(self):
        """Coloca um bloco adjacente"""
        # Determinar a face que foi clicada
        hit_info = self.model.hit
        if hit_info:
            # Calcular posição do novo bloco baseado na normal da face
            normal = round(hit_info.normal)
            new_pos = self.position + normal
            
            # Criar novo bloco na posição adjacente
            Voxel(
                position=new_pos,
                texture=self.texture_ref,
                block_type=self.block_type,
                parent=self.parent
            )

class VoxelWorld(Entity):
    """Gerenciador do mundo de voxels"""
    
    def __init__(self):
        super().__init__()
        self.blocks = {}
    
    def create_block(self, position, block_type="grass"):
        """Cria um bloco na posição especificada"""
        pos_key = tuple(position)
        if pos_key not in self.blocks:
            texture = BLOCK_TEXTURES.get(block_type, BLOCK_TEXTURES["grass"])
            block = Voxel(
                position=position,
                texture=texture,
                block_type=block_type,
                parent=self
            )
            self.blocks[pos_key] = block
            return block
        return None
    
    def remove_block(self, position):
        """Remove um bloco na posição especificada"""
        pos_key = tuple(position)
        if pos_key in self.blocks:
            block = self.blocks[pos_key]
            destroy(block)
            del self.blocks[pos_key]
    
    def get_block(self, position):
        """Retorna o bloco na posição especificada"""
        pos_key = tuple(position)
        return self.blocks.get(pos_key, None)
    
    def clear_all(self):
        """Remove todos os blocos"""
        for block in list(self.blocks.values()):
            destroy(block)
        self.blocks.clear()