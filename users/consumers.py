import json,queue,time,asyncio

from channels.generic.websocket import AsyncWebsocketConsumer
from datetime import datetime
from pynput.mouse import Listener
from threading import Thread
from .cacheService import get_activity_time_with_cache,update_activity_time_with_cache

class Consumers(AsyncWebsocketConsumer):
    async def connect(self):
        self.users_group_name = 'users'
        # Join room group
        await self.channel_layer.group_add(
            self.users_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.users_group_name,
            self.channel_name
        )
    async def on_message(message):
        print("message")

    # Receive message from WebSocket
    async def receive(self, text_data):
        await self.channel_layer.group_send(
            self.users_group_name,
            {
                'type': 'users_activity'
            }
        )
        

    async def users_activity(self,event):
        global q
        q = queue.Queue()
        thread = Thread(target=self.detFun)
        thread.start()

        message=None

        while True:
            init_time = get_activity_time_with_cache()
            if q.empty():
                diff_time = (datetime.now().time().hour * 60 + datetime.now().time().minute) - (init_time.hour *60 + init_time.minute)
            else:
                diff_time = (q.get().hour * 60 + q.get().minute) - (init_time.hour *60 + init_time.minute)
                
            if diff_time < 1:
                message = 'online'
            elif diff_time == 1:
                message= 'away'
            elif diff_time > 1 and diff_time <= 3:
                message= 'disconnected'
            else:
                message= 'offline'

            #Send message to WebSocket    
            await asyncio.sleep(0.05)
            await self.send(text_data=json.dumps({'message': message}))

    def detFun(self):
        with Listener(on_move=self.on_move, on_click=self.on_click, on_scroll=self.on_scroll) as listener:
            listener.join()
            
    def on_move(self,x, y):
        update_activity_time_with_cache()
        q.put(datetime.now().time())
        pass

    def on_click(self,x, y, button, pressed):
        update_activity_time_with_cache()
        q.put(datetime.now().time())
        pass

    def on_scroll(self,x, y, dx, dy):
        update_activity_time_with_cache()
        q.put(datetime.now().time())
        pass
