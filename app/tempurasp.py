import asyncio
from aiohttp import web
from aiohttp.web import Response
from aiohttp_sse import sse_response
from datetime import datetime
import json

RASP_CPU_TEMPER = "/cpu_temp"
RASP_GPU_TEMPER = "/gpu_temp"

async def temper_handler(request):
    loop = request.app.loop
    async with sse_response(request) as resp:
        while True:
            cpu_temper = ''
            gpu_temper = ''

            with open(RASP_CPU_TEMPER, "r") as fd:
                cpu_temper = fd.read()

            if cpu_temper:
                cpu_temper = round(float(cpu_temper)/1000.0, 2)

            with open(RASP_GPU_TEMPER, "r") as fd:
                gpu_temper = fd.read()

            if gpu_temper:
                gpu_temper = float(gpu_temper)

            data = json.dumps({
                "time": datetime.now().isoformat(),
                "cpu_temperature": cpu_temper,
                "gpu_temperature": gpu_temper,
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
                    document.getElementById('cpu_temperature').innerText = data.cpu_temperature;
                    document.getElementById('gpu_temperature').innerText = data.gpu_temperature;
                }
            </script>
            <h1>Raspberry pi temperature:</h1>
            <div>
                <div><span>Time: </span><span id="time"></span></div>
                <div><span>CPU Temperature: </span><span id="cpu_temperature"></span></div>
                <div><span>GPU Temperature: </span><span id="gpu_temperature"></span></div>
            </div>
        </body>
    </html>
    """
    return Response(text=d, content_type='text/html')


app = web.Application()
app.router.add_route('GET', '/temper', temper_handler)
app.router.add_route('GET', '/', index)
web.run_app(app, host='0.0.0.0', port=8080)
