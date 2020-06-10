import tcod

from input_handlers import handle_keys
from game_states import GameStates
from render_functions import clear_all, render_all
from entity import Entity, get_blocking_entity_at_location
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
max_monsters_per_room = 3
colors = {
    'dark_wall': tcod.Color(0, 0, 0),
    'light_wall': tcod.Color(120, 120, 80),
    'dark_ground': tcod.Color(100, 100, 100),
    'light_ground': tcod.Color(200, 200, 170)
}


def main():
    """ Main game function """

    player = Entity(0, 0, '@', tcod.white, 'Player', blocks=True)
    entities = [player]

    # Import font
    tcod.console_set_custom_font(FONT, tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)

    # Console initialization
    tcod.console_init_root(screen_width, screen_height, 'Pilferer %s'%VERSION, False, vsync=False)
    con = tcod.console.Console(screen_width, screen_height)

    # Mapping
    game_map = GameMap(map_width, map_height)
    game_map.make_map(max_rooms, room_min_size, room_max_size, map_width,
                      map_height, player, entities, max_monsters_per_room)

    # FOV
    fov_recompute = True
    fov_map = initialize_fov(game_map)

    # Variables for holding input
    key = tcod.Key()
    mouse = tcod.Mouse()

    # Game state
    game_state = GameStates.PLAYERS_TURN

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
        if move and game_state == GameStates.PLAYERS_TURN:
            dx, dy = move
            destination_x = player.x + dx
            destination_y = player.y + dy
            if not game_map.is_blocked(destination_x, destination_y):
                target = get_blocking_entity_at_location(entities, destination_x, destination_y)
                if target:
                    print('You kick the ' + target.name + ' in the shins, much to its annoyance!')
                else:
                    player.move(dx, dy)

                    fov_recompute = True
                game_state = GameStates.ENEMY_TURN

        exit = action.get('exit')
        if exit:
            return True

        fullscreen = action.get('fullscreen')
        if fullscreen:
            tcod.console_set_fullscreen(not tcod.console_is_fullscreen())
        
        if game_state == GameStates.ENEMY_TURN:
            for entity in entities:
                if entity != player:
                    print('The ' + entity.name + ' ponders the meaning of its existence.')

            game_state = GameStates.PLAYERS_TURN


if __name__ == '__main__':
    main()