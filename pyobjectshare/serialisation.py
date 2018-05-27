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

import pickle
import copy
from .exceptions import UnableToSerialise, UnableToDeserialise
# Imports go here.


def serialise(obj):
    # Serialises any type of object into a string.
    try:
        return pickle.dumps(copy.deepcopy(obj)).hex()
    except BaseException:
        raise UnableToSerialise(
            "Unable to serialise the object that was given."
        )


def deserialise(string: str):
    # De-serialises a serialised string into a object.
    try:
        return pickle.loads(bytes.fromhex(string))
    except BaseException:
        raise UnableToDeserialise(
            "Unable to de-serialize the string that was given."
        )
