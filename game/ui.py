from ursina import *

menu_panel = None
settings_panel = None

mainFont = "assets/font/Minecraft.ttf"

def build_main_menu(start_game):
    global menu_panel, settings_panel

    menu_panel = Entity(parent=camera.ui, enabled=True)

    Text(
        "pythoncraft", 
        parent=menu_panel, 
        font=mainFont,
        pixel_perfect=True,
        scale=3.5, 
        origin=(0,0),
        y=0.2,
        x=0
    )

    Text(
        "by caiovisuals", 
        parent=menu_panel, 
        font=mainFont,
        pixel_perfect=True,
        scale=0.8, 
        origin=(0,0),
        y=0.15, 
        x=0,
        color=color.gray
    )

    Button(
        "Jogar", 
        parent=menu_panel, 
        font=mainFont,
        pixel_perfect=True,
        scale=(0.4, 0.06), 
        origin=(0,0),
        y=-0.05,
        color=color.rgb(111, 111, 111),
        highlight_color=color.rgb(121, 121, 121),
        pressed_color=color.rgb(86, 86, 86),
        text_color=color.white,
        radius=0.02,
        on_click=start_game
    )

    Button(
        "Sair", 
        parent=menu_panel, 
        font=mainFont,
        pixel_perfect=True,
        scale=(0.4, 0.06), 
        origin=(0,0),
        y=-0.15,
        color=color.rgb(111, 111, 111),
        highlight_color=color.rgb(121, 121, 121),
        pressed_color=color.rgb(86, 86, 86),
        text_color=color.white,
        radius=0.02,
        on_click=application.quit
    )

    settings_panel = WindowPanel(
        title="Configurações",
        enabled=False,
        content=(
            Text("Volume: (mock)"),
            Text("Sensibilidade: (mock)")
        ),
        scale=(0.6, 0.6)
    )

    settings_panel.parent = camera.ui
    settings_panel.y = 0

def toggle_settings_panel():
    global settings_panel

    if not settings_panel:
        return
    
    settings_panel.enabled = not settings_panel.enabled
    mouse.locked = not settings_panel.enabled
