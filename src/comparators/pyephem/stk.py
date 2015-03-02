# -*- encoding: utf-8 -*-

from src.base.comparator import BaseComparator
from src.predictors.pyephem.datareader import DataReader as FirstReader
from src.predictors.stk.datareader import DataReader as SecondReader


class Comparator(BaseComparator):

    def __init__(self, data_folder, index_first,
                 index_second):
        super().__init__(data_folder, index_first,
                         index_second, FirstReader, SecondReader)
