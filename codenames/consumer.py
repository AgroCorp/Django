import json
from channels.generic.websocket import AsyncWebsocketConsumer

players = {}


class Player(dict):
    def __init__(self, name, channel_name, team='none', master=False):
        dict.__init__(self, name=name, team=team, master=master, channel_name=channel_name)


class CodenamesConsumer(AsyncWebsocketConsumer):
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
        global players
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        print('')
        players[self.room_group_name] = [x for x in players[self.room_group_name] if x['channel_name'] != self.channel_name]

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'join',
                'players': players[self.room_group_name]
            }
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)

        if data['event'] == 'start_game':
            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'join',
                }
            )
        elif data['event'] == 'socket_connected':
            global players
            user_player = Player(data['username'], self.channel_name)
            if self.room_group_name in players.keys():
                players[self.room_group_name].append(user_player)
            else:
                players[self.room_group_name] = [user_player]

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'join',
                    'players': players[self.room_group_name]
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

    async def change_team(self, data):
        # ellenorizni hogy van-e mar a adott csapat spymastereben valaki
        # csak 1 spy master lehet mindket csapatban!!!!
        user = next((x for x in players[self.room_group_name] if x['name'] == data['user']), None)
        team = data['team'].split('_')[0]
        master = data['team'].split('_')[1] == 'master'
        if master:
            master_user = [x for x in players[self.room_group_name] if x['team'] == team and x['master']]
            if not master_user:  # ha ures akkor nincs meg az adott team master csoportjaban senki
                # tehat a felhasznalo atlephet masterbe
                user['team'] = team
                user['master'] = master
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
            user['team'] = team
            user['master'] = master

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'join',
                'players': players[self.room_group_name]
            }
        )
