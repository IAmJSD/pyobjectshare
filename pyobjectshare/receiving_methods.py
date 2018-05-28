"""

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

import asyncio
import aiohttp
from .exceptions import PortRequired, UnableToDeserialise
from .serialisation import deserialise
# Imports go here.


class ReceivingMethod:
    def __init__(
            self, callback, loop=asyncio.get_event_loop(),
            port=None, passwords=None,
            port_required=False
    ):
        self.loop = loop
        self.callback = callback
        if not port and port_required:
            raise PortRequired(
                "A port is required for this sender."
            )
        self.port = port
        self.passwords = passwords
# A class that all receiving methods have to inherit.


class HTTPReceiver(ReceivingMethod):
    # Sets up a simple HTTP server with a "/" route.

    def __init__(self, callback, loop, port, passwords):
        super().__init__(
            callback,
            loop,
            port,
            passwords,
            True
        )

    async def post_handler(self, request):
        jsonic_data = await request.json()
        if self.passwords:
            passwd = jsonic_data.get("password")
            if not passwd:
                return aiohttp.web.HTTPForbidden()
            if passwd not in self.passwords:
                return aiohttp.web.HTTPForbidden()
        data = jsonic_data.get("data")
        if not data:
            return aiohttp.web.HTTPBadRequest()
        try:
            obj = deserialise(data)
        except UnableToDeserialise:
            return aiohttp.web.HTTPBadRequest()
        await self.callback(obj)
        return aiohttp.web.Response(body="Done.")

    def run(self):
        webserver = aiohttp.web.Application()
        webserver.router.add_route(
            "POST", "/", self.post_handler
        )
        x = self.loop.create_server(
            webserver.make_handler(), "0.0.0.0", self.port
        )
        self.loop.run_until_complete(x)
        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            pass
