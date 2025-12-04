from ursina import *

menu_panel = None
settings_panel = None

def build_main_menu():
    global menu_panel, settings_panel

    menu_panel = Entity(parent=camera.ui, enabled=True)

    Text('pythoncraft', parent=menu_panel, scale=3, y=0.25)
    Text('bycaiovisuals', parent=menu_panel, y=0.1, scale=0.8, color=color.gray)

    def on_play():
        import main
        main.start_game()

    Button('Jogar', parent=menu_panel, scale=(0.25, 0.08), y=-0.05, on_click=on_play)
    Button('Sair', parent=menu_panel, scale=(0.12,0.06), y=-0.20, x=0.18,
           color=color.lime, on_click=application.quit)

    settings_panel = WindowPanel(
        title='Configurações',
        enabled=False,
        content=(
            Text('Volume: (mock)'),
            Text('Sensibilidade: (mock)')
        ),
        scale=(0.6, 0.6)
    )
    settings_panel.parent = camera.ui
    settings_panel.y = 0

def toggle_settings_panel():
    settings_panel.enabled = not settings_panel.enabled
    mouse.locked = not settings_panel.enabled
