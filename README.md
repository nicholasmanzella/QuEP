# PWFA-eProbe

This code was developed to simulate an electron probe's trajectory through a plasma wakefield accelerator. It does so by taking previously simulated fields and propagating an electron through these fields. This allows us to quickly estimate the trajectories of multiple electrons without the repeated use of computationally expensive simulations.

The master branch contains the most up-to-date code.

The code is presently compatible with the following simulations:
Quasi3D

The code presently offers the following electron probe shapes:
Circle
Rectangle
Vertical Line
Horizontal Line
Single Electron

### Running the Simulation
To run the simulation, add an initialization file in the `input` folder, such as the file `example.py`, which would be input to the simulation using
```
python3 eProbe.py input.example
```

Aside from the electrons' initial momenta, the center of the probe, and the location of the screen, the following parameters must be specified in the initialization file (case insensitive):
• simulation_name - quasi3D
• shape - circle, rectangle, vline, hline, or single
• density - Number of electrons to be distributed throughout shape
• iterations - Maximum number of steps before tracking is stopped
• Shape Parameters - Define the dimensions of the shape (see initialization files under include for specifications)

### Requirements
This simulation requires the python packages h5py, importlib, numpy, and matplotlib.

### Contact
Contact Marisa Petrusky (marisapetrusky@gmail.com) for questions about this code. Source code can be found at https://github.com/marisapetrusky/PWFA-eProbe/
