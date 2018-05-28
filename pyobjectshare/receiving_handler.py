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
from .receiving_methods import ReceivingMethod
from .exceptions import ReceivingMethodInvalid
# Imports go here.


class ReceivingHandler:
    def __init__(
        self, method, callback,
        loop=asyncio.get_event_loop(),
        port=None, passwords=None
    ):
        if not issubclass(method, ReceivingMethod):
            raise ReceivingMethodInvalid(
                'Sending method must inherit "SendingMethod".'
            )
        if port:
            port = int(port)
        self.method = method(
            callback,
            loop,
            port,
            passwords
        )

    def run(self):
        self.method.run()
