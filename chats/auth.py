# from channels.auth import AuthMiddlewareStack
# from channels.db import database_sync_to_async
# from channels.middleware import BaseMiddleware
# from django.contrib.auth.models import AnonymousUser
# from rest_framework.authtoken.models import Token
# from urllib.parse import parse_qs


# @database_sync_to_async
# def get_user(scope):
#     query_string = scope.get('query_string').decode()
#     params = parse_qs(query_string)
#     token_key = params.get('token')[0] if params.get('token') else None

#     if token_key is not None and token_key != "":
#         token = Token.objects.filter(key=token_key).first()
#         if token:
#             return token.user
#     return AnonymousUser()

# class TokenAuthMiddleware(BaseMiddleware):

#     async def __call__(self, scope, receive, send):
#         scope['user'] = await get_user(scope)
#         return await super().__call__(scope, receive, send)


# TokenAuthMiddlewareStack = lambda inner: TokenAuthMiddleware(AuthMiddlewareStack(inner))

