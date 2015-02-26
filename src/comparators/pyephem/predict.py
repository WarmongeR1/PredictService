# -*- encoding: utf-8 -*-
import os
from src.base.comparator import BaseComparator


from src.pyephem.datareader import DataReader as FirstReader
from src.predict.datareader import DataReader as SecondReader

class Comparator(BaseComparator):

    def __init__(self, data_folder, index_first,
                 index_second):
        name_first = 'pyephem'
        name_second = 'predict'
        data_folder_first = os.path.join(data_folder, name_first)
        data_folder_second = os.path.join(data_folder, name_second)
        super().__init__(data_folder_first, data_folder_second, index_first,
                         index_second, FirstReader, SecondReader)
