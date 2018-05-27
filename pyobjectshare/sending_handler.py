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

from .sending_methods import SendingMethod
from .exceptions import SendingMethodInvalid, SendingError
from .serialisation import serialise
# Imports go here.


class SendingHandler:

    def __init__(self, method, hostname: str, password=None, port=None):
        if not isinstance(SendingMethod, method):
            raise SendingMethodInvalid(
                'Sending method must inherit "SendingMethod".'
            )
        if port:
            port = int(port)
        self.method = method(
            hostname,
            port,
            password
        )

    async def send(self, obj):
        s = serialise(obj)
        try:
            await self.method.send(s)
        except BaseException:
            raise SendingError(
                "There was an error sending the object."
            )
