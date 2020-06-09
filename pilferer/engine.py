import tcod as libtcod

from input_handlers import handle_keys

FONT = 'assets/arial10x10.png'
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
VERSION = "0.0.1"

def main():
    """ Main game function """

    player_x = int(SCREEN_WIDTH / 2)
    player_y = int(SCREEN_HEIGHT / 2)

    # Import font
    libtcod.console_set_custom_font(FONT, libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)

    # Create screen
    libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'Pilferer %s'%VERSION, False)
    con = libtcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)

    # Variables for holding input
    key = libtcod.Key()
    mouse = libtcod.Mouse()

    # Main game loop
    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)

        # Draw
        libtcod.console_set_default_foreground(con, libtcod.white)
        libtcod.console_put_char(con, player_x, player_y, '@', libtcod.BKGND_NONE)
        libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)
        libtcod.console_flush()

        # Input handling
        action = handle_keys(key)

        move = action.get('move')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        if move:
            dx, dy = move
            player_x += dx
            player_y += dy

        if exit:
            return True

        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())


if __name__ == '__main__':
    main()