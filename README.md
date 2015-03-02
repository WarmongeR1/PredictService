PredictService
===========


It is project for generate predictions of satellite with different tools, for example

- predict
- PyEphem
- PyOrbital
- STK
- orbitron

You can generate predictions in console for
 
- predict
- PyEphem
- PyOrbital


Usage
-----

Generate predictions:

```bash
#!/bin/sh

START_TIME=2015-01-01_18:21:26
END_TIME=2015-01-02_18:21:26
TLE_PATH=bin/TLEs/dmc.txt

echo "PyEphem"
python run_ephem.py -i $TLE_PATH -s $START_TIME -e $END_TIME -o ./bin/result/pyephem

echo "PyOrbital"
python run_orbital.py -i $TLE_PATH -s $START_TIME -e $END_TIME -o ./bin/result/pyorbital

echo "Predict"
python run_predict.py -i $TLE_PATH -s $START_TIME -e $END_TIME -o ./bin/result/predict
```

Run gui:

```python
python gui.py
```

Compare results:

![Compare results](/resources/image.png)

