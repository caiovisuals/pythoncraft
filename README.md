# PYTHONCRAFT

Um jogo sandbox 3D inspirado em **Minecraft**, desenvolvido inteiramente em Python utilizando a engine Ursina.<br/>
O projeto foca em aprendizado, experimentação e construção de sistemas fundamentais de um jogo voxel: mundo, jogador, inventário, itens, entidades e interface.

## Capturas de Telas

![Menu Principal](assets/screenshots/1.png)
![Modo Solo](assets/screenshots/2.png)
![Modo Multiplayer](assets/screenshots/3.png)

## Dependências

- **[Python](https://www.python.org)** - ^3.10+
- **[Ursina Engine](https://www.ursinaengine.org)**
- **[Panda3D](https://www.panda3d.org)**
- **[perlin-noise](https://pypi.org/project/perlin-noise)**

Instale as dependências com:
```
pip install -r requirements.txt
```
E rode o projeto com:
```
python main.py
```

Para habilitar atalhos de desenvolvimento (como `R` para voltar ao menu):
```
python main.py --debug
```

Rode os testes (usam o `unittest` da biblioteca padrão) com:
```
python -m unittest discover tests
```

## Objetivos

- Exploração de um mundo voxel
- Controle em primeira pessoa
- Sistema de inventário e hotbar
- Itens e entidades customizadas
- Interface com menu, configurações e HUD
- Estudos de desenvolvimento de jogos (dessa vez com python)

by caiothevisual<br />
#caiobavisuals #minecraft #python #games #sandbox