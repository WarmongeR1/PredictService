# -*- encoding: utf-8 -*-
from src.base.comparator import BaseComparator

from src.predict.datareader import DataReader as SecondReader
from src.stk.datareader import DataReader as FirstReader


class Comparator(BaseComparator):
    def __init__(self, data_folder_first, data_folder_second, index_first,
                 index_second):
        super().__init__(data_folder_first, data_folder_second, index_first,
                         index_second, FirstReader, SecondReader)