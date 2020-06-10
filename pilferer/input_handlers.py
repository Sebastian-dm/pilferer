import tcod


def handle_keys(key):
    key_char = chr(key.c)

    # Movement keys
    if key.vk == tcod.KEY_KP8 or key.vk == tcod.KEY_UP or key_char == 'k':
        return {'move': (0, -1)}
    elif key.vk == tcod.KEY_KP2 or key.vk == tcod.KEY_DOWN or key_char == 'j':
        return {'move': (0, 1)}
    elif key.vk == tcod.KEY_KP4 or key.vk == tcod.KEY_LEFT or key_char == 'j':
        return {'move': (-1, 0)}
    elif key.vk == tcod.KEY_KP6 or key.vk == tcod.KEY_RIGHT or key_char == 'l':
        return {'move': (1, 0)}
    elif key.vk == tcod.KEY_KP7 or key_char == 'y':
        return {'move': (-1, -1)}
    elif key.vk == tcod.KEY_KP9 or key_char == 'u':
        return {'move': (1, -1)}
    elif key.vk == tcod.KEY_KP1 or key_char == 'b':
        return {'move': (-1, 1)}
    elif key.vk == tcod.KEY_KP3 or key_char == 'n':
        return {'move': (1, 1)}

    if key.vk == tcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle full screen
        return {'fullscreen': True}

    elif key.vk == tcod.KEY_ESCAPE:
        # Exit the game
        return {'exit': True}

    # No key was pressed
    return {}