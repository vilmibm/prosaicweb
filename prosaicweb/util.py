# prosaicweb
# Copyright (C) 2016  nathaniel smith
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from typing import Dict, Union

from flask import Response
from flask_login import current_user
from werkzeug.local import LocalProxy

ResponseData = Union[str, Response]
# TODO this is not good:
Request = LocalProxy

def get_method(req: Request) -> str:
    return req.form.get('_method', req.method)

def auth_context(req: Request) -> Dict:
    return {
        'authenticated': current_user.is_authenticated,
        'user': current_user
    }
