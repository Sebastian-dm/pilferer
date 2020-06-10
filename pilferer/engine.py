import tcod

from input_handlers import handle_keys
from render_functions import clear_all, render_all
from entity import Entity
from map_objects.game_map import GameMap
from fov_functions import initialize_fov, recompute_fov

VERSION = "0.1"
FONT = 'assets/arial10x10.png'
screen_width = 80
screen_height = 50
map_width = 80
map_height = 45
room_max_size = 10
room_min_size = 6
max_rooms = 30
fov_algorithm = 0
fov_light_walls = True
fov_radius = 10
colors = {
    'dark_wall': tcod.Color(0, 0, 0),
    'light_wall': tcod.Color(120, 120, 80),
    'dark_ground': tcod.Color(100, 100, 100),
    'light_ground': tcod.Color(200, 200, 170)
}


def main():
    """ Main game function """

    player = Entity(int(screen_width / 2), int(screen_height / 2), '@', tcod.white)
    npc = Entity(int(screen_width / 2 - 5), int(screen_height / 2), '@', tcod.yellow)
    entities = [npc, player]

    # Import font
    tcod.console_set_custom_font(FONT, tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)

    # Console initialization
    tcod.console_init_root(screen_width, screen_height, 'Pilferer %s'%VERSION, False, vsync=False)
    con = tcod.console.Console(screen_width, screen_height)

    # Mapping
    game_map = GameMap(map_width, map_height)
    game_map.make_map(max_rooms, room_min_size, room_max_size, map_width, map_height, player)

    # FOV
    fov_recompute = True
    fov_map = initialize_fov(game_map)

    # Variables for holding input
    key = tcod.Key()
    mouse = tcod.Mouse()

    # Main game loop
    while not tcod.console_is_window_closed():
        # FOV
        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, fov_radius, fov_light_walls, fov_algorithm)

        # Draw
        render_all(con, entities, game_map, fov_map, fov_recompute, screen_width, screen_height, colors)
        fov_recompute = False
        tcod.console_flush()
        clear_all(con, entities)

        # Input handling
        tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS, key, mouse)
        action = handle_keys(key)

        move = action.get('move')
        if move:
            dx, dy = move
            if not game_map.is_blocked(player.x + dx, player.y + dy):
                player.move(dx, dy)
                fov_recompute = True

        exit = action.get('exit')
        if exit:
            return True

        fullscreen = action.get('fullscreen')
        if fullscreen:
            tcod.console_set_fullscreen(not tcod.console_is_fullscreen())


if __name__ == '__main__':
    main()