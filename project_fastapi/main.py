import uvicorn
from fastapi import FastAPI, WebSocket, BackgroundTasks, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
import redis
from py_fastapi_logging.middlewares.logging import LoggingMiddleware



app = FastAPI()

app.add_middleware(LoggingMiddleware, app_name='app')

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>websocket</title>
    </head>
    <body>
        <div style="display:flex; align-items: center;
    flex-direction: column;">
            <h1>WebSocket Чайник</h1>

            <button id='stop'>Выключить</button>
            <ul id='messages'>
            </ul>
        </div>
        

        <script>

    var ws = new WebSocket("ws://localhost:8000/ws");
           
    ws.onmessage = function(event) {
        var messages = document.getElementById('messages')
        var message = document.createElement('li')
        var content = document.createTextNode(event.data)
        message.appendChild(content)
        messages.appendChild(message)

    };
        let stop = document.getElementById('stop').addEventListener("click", function(e){
            ws.close();

        });

        </script>
    </body>
</html>
"""


@app.get("/")
async def get():
    return HTMLResponse(html)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    print('Accepting client connection...')

    await websocket.accept()

    while True:
        with redis.Redis(host='localhost', port=6379) as redis_client:
            result = redis_client.brpop('zxc')[1].decode('utf-8')
            await websocket.send_text(str(result))


