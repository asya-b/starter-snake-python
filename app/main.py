import json
import os
import random
import bottle
import operator

from api import ping_response, start_response, move_response, end_response

@bottle.route('/')
def index():
    return '''
    Battlesnake documentation can be found at
       <a href="https://docs.battlesnake.com">https://docs.battlesnake.com</a>.
    '''


@bottle.route('/static/<path:path>')
def static(path):
    """
    Given a path, return the static file located relative
    to the static folder.

    This can be used to return the snake head URL in an API response.
    """
    return bottle.static_file(path, root='static/')


@bottle.post('/ping')
def ping():
    """
    A keep-alive endpoint used to prevent cloud application platforms,
    such as Heroku, from sleeping the application instance.
    """
    return ping_response()

@bottle.post('/start')
def start():
    data = bottle.request.json

    """
    TODO: If you intend to have a stateful snake AI,
            initialize your snake state here using the
            request's data if necessary.
    """
    print(json.dumps(data))

    from Snake import Snake
    
    s = Snake(data)
    color = s.COLOUR

    return start_response(color)


@bottle.post('/move')
def move():
    from Direction import Direction
    
    data = bottle.request.json
    print(json.dumps(data))

    up = Direction(0,-1,data)
    down = Direction(0,1,data)
    left = Direction(-1,0,data)
    right = Direction(1,0,data)
    
    rewards = {"up":up.getReward(),"down":down.getReward(),"left":left.getReward(),"right":right.getReward()}
    
    print('REWARDS: ',rewards)
    direction = max(rewards.items(), key=operator.itemgetter(1))[0]
    print('Chose to go {} on turn {}'.format(direction, data['turn']))
    return move_response(direction)


@bottle.post('/end')
def end():
    data = bottle.request.json

    """
    TODO: If your snake AI was stateful,
        clean up any stateful objects here.
    """
    print(json.dumps(data))

    return end_response()


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug=os.getenv('DEBUG', True)
    )
