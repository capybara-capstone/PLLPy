## PLLPython
This project provides an open-source Python simulation library that allows users to easily configure and simulate PLLs and view the effect of PLL design choices
on the performance of their SerDes systems. Additionally, the tool is usable as a stand-alone PLL simulation tool. 


**Out of the Box Setup:**

1. Install cmake:

```
sudo apt install cmake
```

2. Start a python virtural environment, and install PLLPython from the Python package manager:

```
python -m venv example_venv
source ./example_venv/bin/activate
pip install pllpython
```

3. Download the examples by running the following command:

```
pllpython_tutorial
``` 

4. You should be good to go, for an out-the-box demo, run

```
python pllpython_tutorial/run_sim.py
```
