# -*- encoding: utf-8 -*-

from src.base.comparator import BaseComparator
from src.pyorbital.datareader import DataReader as SecondReader
from src.stk.datareader import DataReader as FirstReader


class Comparator(BaseComparator):

    def __init__(self, data_folder, index_first,
                 index_second):
        super().__init__(data_folder, index_first,
                         index_second, FirstReader, SecondReader)
