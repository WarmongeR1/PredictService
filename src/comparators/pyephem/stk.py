# -*- encoding: utf-8 -*-
import os
from src.base.comparator import BaseComparator

from src.pyephem.datareader import DataReader as FirstReader
from src.stk.datareader import DataReader as SecondReader


class Comparator(BaseComparator):

    def __init__(self, data_folder, index_first,
                 index_second):
        super().__init__(data_folder, index_first,
                         index_second, FirstReader, SecondReader)
