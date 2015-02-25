# -*- encoding: utf-8 -*-

##########################################################################
# Copyright 2014 Samuel Gongora Garcia (s.gongoragarcia@gmail.com)
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
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##########################################################################
# Author: s.gongoragarcia[at]gmail.com
##########################################################################


from os import getcwd


class Read_data(object):

    def __init__(self, index_pyephem, index_predict, index_pyorbital,
                 index_orbitron, sat_selected, index_STK, STK_dir,
                 orbitron_dir):

        # Orbitron stuff
        self.file = '/home/case/Orbitron/Output/output.txt'
        self.index_orbitron = index_orbitron + 1
        self.sat_selected = sat_selected
        # PyEphem stuff
        self.index_pyephem = index_pyephem
        # predict stuff
        self.index_predict = index_predict + 1
        # PyOrbital stuff
        self.index_pyorbital = index_pyorbital
        # STK stuff
        self.index_STK = index_STK
        self.STK_dir = STK_dir
        self.orbitron_dir = orbitron_dir

        self.directorio_script = getcwd()
