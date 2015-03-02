#!/bin/sh

source ~/Develop/venv/propagator/bin/activate
echo "PyEphem"
python run_ephem.py -i bin/TLEs/dmc.txt -s 2015-01-01_18:21:26 -e 2015-01-02_18:21:26 -o ./bin/result/pyephem

echo "PyOrbital"
python run_orbital.py -i bin/TLEs/dmc.txt -s 2015-01-01_18:21:26 -e 2015-01-02_18:21:26 -o ./bin/result/pyorbital
