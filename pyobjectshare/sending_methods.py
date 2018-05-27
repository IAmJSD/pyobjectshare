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

import aiohttp
import asyncio
import socket
import json
from .exceptions import PortRequired
# Imports go here.


class SendingMethod:
    def __init__(self, hostname, port, password, port_required=False):
        self.hostname = hostname
        if port is None and port_required:
            raise PortRequired(
                "A port is required for this sender."
            )
        self.port = port
        self.password = password
# A class that all sending methods have to inherit.


class TCPSender(SendingMethod):
    # This sends the Python object over TCP.
    # This is NOT secure for across the internet (meant for LAN).
    # If you want to send something over the internet, use POSTSender.

    def __init__(self, hostname, port, password):
        super().__init__(
            hostname,
            port,
            password,
            True
        )

    def send_non_async(self, string):
        sock = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM
        )
        sock.bind(("", self.port))
        data_str = json.dumps(
            {"password": self.password, "python_obj": string}
        )
        sock.sendto(
            data_str.encode(), (self.hostname, self.port)
        )

    async def send(self, string):
        await asyncio.get_event_loop().run_in_executor(
            None,
            self.send_non_async,
            string
        )


class POSTSender(SendingMethod):
    # This sends the Python object in a HTTP POST request.

    def __init__(self, hostname, port, password):
        super().__init__(
            hostname,
            port,
            password,
            False
        )

    async def send(self, string):
        async with aiohttp.ClientSession() as session:
            await session.post(self.hostname, data={
                "password": self.password,
                "data": string
            })
