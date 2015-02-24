#!/bin/sh


INSDIR='./bin'

cp main.sh $INSDIR					# BASH script
# Window routine
cp output_data.py $INSDIR				# Output data to GUI
cp gui.py $INSDIR						# UI
cp configure_simulations.py $INSDIR	# Auxiliary UI
cp scrolledlist.py $INSDIR			# List
# Propagators
cp pyephem_sims.py $INSDIR			# PyEphem script
cp pyorbital_sims.py $INSDIR			# PyOrbital script
cp predict_sims.sh $INSDIR			# predict script
# Auxiliary scripts
cp get_elements.py $INSDIR			# Get elements from TLE
cp get_names.py $INSDIR				# Get satellite names from TLE file
cp update_tles.sh $INSDIR				# Update TLE files from Celestrak
