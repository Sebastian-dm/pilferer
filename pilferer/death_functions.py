import tcod

from game_states import GameStates
from render_functions import RenderOrder


def kill_player(player):
    player.char = '%'
    player.color = tcod.grey

    return 'You died!', GameStates.PLAYER_DEAD


def kill_monster(monster):
    death_message = '{0} is dead!'.format(monster.name.capitalize())

    monster.char = '%'
    monster.color = tcod.dark_red
    monster.render_order = RenderOrder.CORPSE
    monster.blocks = False
    monster.fighter = None
    monster.ai = None
    monster.name = 'remains of ' + monster.name

    return death_message