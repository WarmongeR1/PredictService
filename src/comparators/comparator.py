# -*- encoding: utf-8 -*-

from src.comparators.pyephem.orbitron import Comparator as Orbitron
from src.comparators.pyephem.predict import Comparator as Predict
from src.comparators.pyephem.pyorbital import Comparator as PyOrbital
from src.comparators.pyephem.stk import Comparator as STK


def compare(direct, index_first, index_second, folder, deviation=True):
    comparators = {
        'predict': Predict,
        'stk': STK,
        'pyorbital': PyOrbital,
        'orbitron': Orbitron,
    }
    comparator = comparators.get(direct)(folder, index_first, index_second)
    if deviation:
        result = comparator.compare_deviation()
    else:
        result = comparator.compare()
    return result
