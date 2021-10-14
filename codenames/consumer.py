import json
from channels.generic.websocket import AsyncWebsocketConsumer

from codenames.Game import Game


class MyEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__


class CodenamesConsumer(AsyncWebsocketConsumer):
    players = {}

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
        self.players[self.room_group_name] = [x for x in self.players[self.room_group_name] if x.channel_name != self.channel_name]

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'join',
                'players': [player.toJSON() for player in self.players[self.room_group_name]]
            }
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)

        if data['event'] == 'start_game':
            game = Game()
            game.start_game()
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'game',
                    'matrix': json.dumps(game.words_map, cls=MyEncoder),
                    'starting_team': game.starting_team
                }
            )
        elif data['event'] == 'socket_connected':
            user_player = self.Player(data['username'], self.channel_name)
            if self.room_group_name in self.players.keys():
                self.players[self.room_group_name].append(user_player)
            else:
                self.players[self.room_group_name] = [user_player]

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'join',
                    'players': json.dumps(self.players[self.room_group_name], cls=MyEncoder)
                }
            )
        elif data['event'] == 'change_team':
            await self.change_team(data)

    # send join to socket
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

    async def game(self, event):
        await self.send(text_data=json.dumps({
            'event': 'game',
            'matrix': event['matrix'],
            'starting_team': event['starting_team']
        }))

    async def change_team(self, data):
        # ellenorizni hogy van-e mar a adott csapat spymastereben valaki
        # csak 1 spy master lehet mindket csapatban!!!!
        user = next((x for x in self.players[self.room_group_name] if x.name == data['user']), None)
        team = data['team'].split('_')[0]
        master = data['team'].split('_')[1] == 'master'
        if master:
            master_user = [x for x in self.players[self.room_group_name] if x.team == team and x.master]
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
                'players': json.dumps(self.players[self.room_group_name], cls=MyEncoder)
            }
        )
