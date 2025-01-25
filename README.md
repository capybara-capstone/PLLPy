# PLLpy
A Python library for PLL simulation

## Table of Contents
* [General Info](#general-information)
* [Features](#features)
* [Contents](#contents)
* [Setup](#setup)

## General Information

PLLPy is a Python library for simulating different PLL architectures. Based on [Wireline-Simulink](https://github.com/tchancarusone/Wireline-Simulink), PLLPy aims at being a modular and configurable PLL simulator
for use as a design aide and a teaching tool. It is also fully integratable with [SerDesPy](https://github.com/richard259/serdespy), a SerDes modelling and simulation tool.

## Features
  * Basic PLL blocks: VCO, PFD Loop Filter, Linear Phase Detector, Divider
  * Non-Ideal PLL Blocks: 

## Contents
  * [docs](docs/): Documentation and documentation generator scripts.
  * [components](components/): PLL block implementations.
  * [utils](utils/): Helper functions for the simulator.
  * [tests](tests/): Unit tests to test PLL functionality.
  * [run_sim.py](run_sim.py): An example top-level for the simulator.

## Setup
You will need to install Python 3.7+. Once you've installed Python 3.7+, enter the directory this repo is cloned in, and run:
```
pip install -r requirements
```

## Usage 
```
python run_sim.py
```
 
To change the configuration file with which to run the simulator, you will need to edit run_sim.py as follows:

```
sim = Sim("my_config_file.json") # "my_config_file.json" is the name of your configuration file.
sim.add_pll()
sim.start()
```

If no configuration file is passed in (as in the default run_sim.py code), the settings will be set to their defaults (see [settings.py](components/settings.py)).




