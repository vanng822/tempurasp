import asyncio
from aiohttp import web
from aiohttp.web import Response
from aiohttp_sse import sse_response
from datetime import datetime
import json

RASP_CPU_TEMPER = "/cpu_temp"

async def temper_handler(request):
    loop = request.app.loop
    async with sse_response(request) as resp:
        while True:
            temper = ''
            with open(RASP_CPU_TEMPER, "r") as fd:
                temper = fd.read()
            if temper:
                temper = round(float(temper)/1000.0, 2)
            data = json.dumps({
                "time": datetime.now().isoformat(),
                "temperature": temper,
            })
            print(data)
            await resp.send(data)
            await asyncio.sleep(3, loop=loop)
    return resp


async def index(request):
    d = """
        <html>
        <body>
            <script>
                var evtSource = new EventSource("/temper");
                evtSource.onmessage = function(e) {
                    var data = JSON.parse(e.data);
                    document.getElementById('time').innerText = data.time;
                    document.getElementById('temperature').innerText = data.temperature;
                }
            </script>
            <h1>Raspberry pi temperature:</h1>
            <div>
                <div><span>Time: </span><span id="time"></span></div>
                <div><span>Temperature: </span><span id="temperature"></span></div>
            </div>
        </body>
    </html>
    """
    return Response(text=d, content_type='text/html')


app = web.Application()
app.router.add_route('GET', '/temper', temper_handler)
app.router.add_route('GET', '/', index)
web.run_app(app, host='0.0.0.0', port=8080)
