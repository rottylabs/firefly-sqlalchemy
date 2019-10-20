#  Copyright (c) 2019 JD Williams
#
#  This file is part of Firefly, a Python SOA framework built by JD Williams. Firefly is free software; you can
#  redistribute it and/or modify it under the terms of the GNU General Public License as published by the
#  Free Software Foundation; either version 3 of the License, or (at your option) any later version.
#
#  Firefly is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the
#  implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
#  Public License for more details. You should have received a copy of the GNU Lesser General Public
#  License along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#  You should have received a copy of the GNU General Public License along with Firefly. If not, see
#  <http://www.gnu.org/licenses/>.

from typing import Dict

from sqlalchemy import MetaData


class MetadataRegistry:
    def __init__(self):
        self._metadata = {}

    def add(self, context_name: str, metadata: MetaData):
        self._metadata[context_name] = metadata

    def get(self, context_name: str) -> MetaData:
        return self._metadata.get(context_name)

    def all(self) -> Dict[str, MetaData]:
        return self._metadata
