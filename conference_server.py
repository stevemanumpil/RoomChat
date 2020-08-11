import asyncio
import websockets
import json
from client import Client

rooms = {}

async def consumer(websocket, path):
    room_id = ''
    user_id = ''
    person = Client(websocket, path)
    print('[CONNECTION] Connect with', websocket.remote_address)
    async for message in websocket:
        try:
            new_msg = json.loads(message)
            print(new_msg)
            if new_msg['action'] == 'join-room':
                if rooms.get(new_msg['room_id']):
                    msg = json.dumps({
                        'action' : 'user-connected',
                        'user_id' : new_msg['user_id']
                    })
                    await asyncio.wait([user.send(msg) for user in rooms[new_msg['room_id']]])
                    rooms[new_msg['room_id']].append(person.getConn())
                else:
                    rooms[new_msg['room_id']] = []
                    rooms[new_msg['room_id']].append(person.getConn())

                room_id = new_msg['room_id']
                user_id = new_msg['user_id']
                
        except Exception as e:
            print("[ERROR] :",e)

    
    print("[CLOSE] Connection",person.getConn().remote_address,"close")
    rooms[room_id].remove(person.getConn())

    msg = json.dumps({
        'action' : 'user-disconnected',
        'user_id' : user_id
    })
    try:
        await asyncio.wait([user.send(msg) for user in rooms[room_id]])
    except Exception as e:
        print('delete room key')
        rooms.pop(room_id)
        print(rooms)


server = websockets.serve(consumer, '127.0.0.1',5576)

asyncio.get_event_loop().run_until_complete(server)
asyncio.get_event_loop().run_forever()