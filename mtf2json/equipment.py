# https://github.com/juk0de/mtf2json
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
This module handles all equipment that has to be added to the
'Weapons and Equipment' section of the record sheet by storing
it in a dedicated 'equipment' section in the JSON data.

Because that kind of equipment is scattered across the various
critical slot entries in the MTF files (with different equipment
having different format, e. g. some contain a ':SIZE:' value),
it is added after the JSON conversion, in a separate step.

Another issue is that some MTF files contain some equipment in the
'Weapons' sections while others don't. This module is responsible
for cleaning that mess up a bit.
"""
