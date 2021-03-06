import os


async def application(scope, receive, send):
    if scope['type'] == 'lifespan':
        with open('version', 'w+') as f:
            f.write(
                scope['asgi']['version'] + ' ' + scope['asgi']['spec_version']
            )
        while True:
            message = await receive()
            if message['type'] == 'lifespan.startup':
                os.remove('startup')
                await send({'type': 'lifespan.startup.complete'})
            elif message['type'] == 'lifespan.shutdown':
                os.remove('shutdown')
                await send({'type': 'lifespan.shutdown.complete'})
                return

    if scope['type'] == 'http':
        await send(
            {
                'type': 'http.response.start',
                'status': 204,
                'headers': [(b'content-length', b'0'),],
            }
        )
