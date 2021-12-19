# from channels.auth import AuthMiddlewareStack
# from channels.routing import ProtocolTypeRouter, URLRouter
# import chats.routing
# from chats.auth import TokenAuthMiddlewareStack
# from channels.http import AsgiHandler

# application = ProtocolTypeRouter({
#     # "http": AsgiHandler(),
#     'websocket': TokenAuthMiddlewareStack(
#         URLRouter(
#             chats.routing.websocket_urlpatterns
#         )
#     ),
# })

# # application = ProtocolTypeRouter({
# #     # "http": AsgiHandler(),
# #     'websocket': URLRouter(
# #             chats.routing.websocket_urlpatterns
# #         ),
# # })
