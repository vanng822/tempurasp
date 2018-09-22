import asyncio
from aiohttp import web
from aiohttp.web import Response
from aiohttp_sse import sse_response
from datetime import datetime

RASP_CPU_TEMPER = "/cpu_temp"

async def temper_handler(request):
    loop = request.app.loop
    async with sse_response(request) as resp:
        while True:
            temper = ''
            with open(RASP_CPU_TEMPER, "r") as fd:
                temper = fd.read()
            if temper:
                temper = round(tempur/1000.0)
            data = 'Time: {}, Temperature: {}'.format(
                datetime.now(),
                temper)
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
                    document.getElementById('response').innerText = e.data
                }
            </script>
            <h1>Response from server:</h1>
            <div id="response"></div>
        </body>
    </html>
    """
    return Response(text=d, content_type='text/html')


app = web.Application()
app.router.add_route('GET', '/temper', temper_handler)
app.router.add_route('GET', '/', index)
web.run_app(app, host='0.0.0.0', port=8080)
