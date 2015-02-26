# -*- encoding: utf-8 -*-

from src.comparators.stk.pyephem import Comparator as PyEphem
from src.comparators.stk.pyorbital import Comparator as PyOrbital
from src.comparators.stk.orbitron import Comparator as Orbitron
from src.comparators.stk.predict import Comparator as Predict


def compare(direct, index_first, index_second, folder, deviation=True):
    comparators = {
        'predict': Predict,
        'pyephem': PyEphem,
        'pyorbital': PyOrbital,
        'orbitron': Orbitron,
    }

    compar = comparators.get(direct)(index_first, index_second, folder)
    if deviation:
        result = compar.compare_deviation()
    else:
        result = compar.compare()
    return result
