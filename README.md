# PWFA-eProbe

The unit-test-blowout branch contains plotting macros for visualizing and cross-checking the behavior of electrons within the blowout regime of a plasma wakefield. Macros can be selected by setting
the boolean variables at the top of the eProbe.py script.

### Running the Simulation
To run without a pre-defined initial condition file use
```
python3 eProbe.py
```
and you will be prompted to input the initial conditions in normalized units.

You can also add an initialization file in the `input` folder, such as the file `example.py`, which would be input to the simulation using
```
python3 eProbe.py input.example
```
### Requirements
This simulation requires the python packages h5py, importlib, numpy, and matplotlib.

### Contact
Contact Marisa Petrusky (marisapetrusky@gmail.com) for questions about this code. Source code can be found at https://github.com/marisapetrusky/PWFA-eProbe/
