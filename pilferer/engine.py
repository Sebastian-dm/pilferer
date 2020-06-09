import tcod

from input_handlers import handle_keys
from render_functions import clear_all, render_all
from entity import Entity

FONT = 'assets/arial10x10.png'
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
VERSION = "0.0.1"

def main():
    """ Main game function """

    player = Entity(int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 2), '@', tcod.white)
    npc = Entity(int(SCREEN_WIDTH / 2 - 5), int(SCREEN_HEIGHT / 2), '@', tcod.yellow)
    entities = [npc, player]

    # Import font
    tcod.console_set_custom_font(FONT, tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)

    # Create screen
    tcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'Pilferer %s'%VERSION, False)
    con = tcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)

    # Variables for holding input
    key = tcod.Key()
    mouse = tcod.Mouse()

    # Main game loop
    while not tcod.console_is_window_closed():
        tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS, key, mouse)

        # Draw
        render_all(con, entities, SCREEN_WIDTH, SCREEN_HEIGHT)
        tcod.console_flush()
        clear_all(con, entities)

        # Input handling
        action = handle_keys(key)

        move = action.get('move')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        if move:
            dx, dy = move
            player.move(dx, dy)

        if exit:
            return True

        if fullscreen:
            tcod.console_set_fullscreen(not tcod.console_is_fullscreen())


if __name__ == '__main__':
    main()