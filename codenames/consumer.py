import json
from itertools import cycle
from channels.generic.websocket import AsyncWebsocketConsumer

from codenames.Game import Game

players = {}
game = None
red_team = None
blue_team = None


class MyEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__


def find_next_user_in_team(team):
    if team == 'blue':
        return next(blue_team)
    else:
        return next(red_team)


class CodenamesConsumer(AsyncWebsocketConsumer):
    class Player:
        name = ''
        channel_name = ''
        team = ''
        master = None

        def __init__(self, name, channel_name, team='none', master=False):
            self.name = name
            self.channel_name = channel_name
            self.team = team
            self.master = master

    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = 'codenames_%s' % self.room_id

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        players[self.room_group_name] = [x for x in players[self.room_group_name] if x.channel_name != self.channel_name]

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'join',
                'players': json.dumps(players[self.room_group_name], cls=MyEncoder)
            }
        )

    # TODO: end_turn lekezelese
    # TODO: next_tipp lekezelese

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)

        if data['event'] == 'start_game':
            global red_team, blue_team, game
            game = Game()
            red_team = cycle(list(filter(lambda x: x.team == 'red' and not x.master, players[self.room_group_name])))
            blue_team = cycle(list(filter(lambda x: x.team == 'blue' and not x.master, players[self.room_group_name])))
            game.start_game()
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'game_start',
                    'matrix': json.dumps(game.words_map, cls=MyEncoder),
                    #'starting_team': self.game.starting_team
                    'starting_team': 'blue'

                }
            )
        elif data['event'] == 'spymaster_submit':
            tokens = data['data'].split(' ')
            game.spymaster_count = int(tokens[1])
            spymaster_text = data['data']
            if len(tokens) != 2:
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'error',
                        'msg': 'a helyes formatum: szo[szokosz]szam!',
                        'to_user': list(filter(lambda x: x.channel_name == self.channel_name, players[self.room_group_name]))[0].name
                    }
                )
                return
            try:
                int(tokens[1])
            except ValueError:
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'error',
                        'msg': 'rossz szamot adtal meg probald ujra',
                        'to_user': list(filter(lambda x: x.channel_name == self.channel_name, players[self.room_group_name]))[0].name
                    }
                )
                return
            first_user = find_next_user_in_team(game.starting_team)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'spymaster_submit',
                    'data': spymaster_text,
                    'first_user_to_tipp': json.dumps(first_user, cls=MyEncoder),
                }
            )
        elif data['event'] == 'socket_connected':
            user_player = self.Player(data['username'], self.channel_name)
            if self.room_group_name in players.keys():
                players[self.room_group_name].append(user_player)
            else:
                players[self.room_group_name] = [user_player]

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'join',
                    'players': json.dumps(players[self.room_group_name], cls=MyEncoder)
                }
            )
        elif data['event'] == 'change_team':
            await self.change_team(data)

        elif data['event'] == 'user_tipp':
            game.user_tipp_count += 1
            pos = data['pos'].split('_')
            user = self.get_player_by_username(data['user'])
            akt_card = game.words_map[int(pos[0])][int(pos[1])]
            opposite_team = 'red' if user.team == 'blue' else 'blue'
            game.kitalal(pos)

            if game.user_tipp_count < game.spymaster_count:
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'end_turn',
                        'matrix': json.dumps(game.words_map, cls=MyEncoder),
                        'next_player': json.dumps(find_next_user_in_team(opposite_team), cls=MyEncoder)
                    }
                )

            if akt_card.team == 'civil' or akt_card.team == opposite_team:
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'end_turn',
                        'matrix': json.dumps(game.words_map, cls=MyEncoder),
                        'next_player': json.dumps(find_next_user_in_team(opposite_team), cls=MyEncoder)

                    }
                )
            elif akt_card.team == 'killer' or game.check_game_is_over():
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'game_over',
                        'winner': opposite_team
                    }
                )
            else:
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'next_tipp',
                        'next_user': json.dumps(find_next_user_in_team(user.team), cls=MyEncoder),
                        'matrix': json.dumps(game.words_map, cls=MyEncoder)
                    }
                )

    # send join to socket
    async def game_over(self, data):
        await self.send(text_data=json.dumps({
            'event': 'game_over',
            'winner': data['winner']
        }))

    async def join(self, event):
        await self.send(text_data=json.dumps({
            'event': 'join',
            'players': event['players']
        }))

    async def error(self, event):
        await self.send(text_data=json.dumps({
            'event': 'error',
            'msg': event['msg'],
            'to_user': event['to_user']
        }))

    async def game_start(self, event):
        await self.send(text_data=json.dumps({
            'event': 'game',
            'matrix': event['matrix'],
            'starting_team': event['starting_team']
        }))

    async def spymaster_submit(self, data):
        await self.send(text_data=json.dumps({
            'event': 'spymaster_submit',
            'spyInput': data['data'],
            'first_user_to_tipp': data['first_user_to_tipp']
        }))

    async def change_team(self, data):
        # ellenorizni hogy van-e mar a adott csapat spymastereben valaki
        # csak 1 spy master lehet mindket csapatban!!!!
        user = next((x for x in players[self.room_group_name] if x.name == data['user']), None)
        team = data['team'].split('_')[0]
        master = data['team'].split('_')[1] == 'master'
        if master:
            master_user = [x for x in players[self.room_group_name] if x.team == team and x.master]
            if not master_user:  # ha ures akkor nincs meg az adott team master csoportjaban senki
                # tehat a felhasznalo atlephet masterbe
                user.team = team
                user.master = master
            else:
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'error',
                        'msg': 'Csak egy spy master lehet csapatonkent!',
                        'to_user': user['name']
                    }
                )
        else:
            user.team = team
            user.master = master

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'join',
                'players': json.dumps(players[self.room_group_name], cls=MyEncoder)
            }
        )

    def get_player_by_username(self, username):
        return next(x for x in players[self.room_group_name] if x.name == username)
