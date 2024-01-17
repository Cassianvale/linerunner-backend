from channels.routing import ProtocolTypeRouter
from . import consumers  # 导入你的消费者

application = ProtocolTypeRouter({
    'websocket': URLRouter([
        path('ws/notifications/', consumers.NotificationConsumer.as_asgi()),
    ]),
})