
# USTEP online logparser

This is the code for the paper "USTEP: Unfixed Search Tree for Efficient Log Parsing" accepted at IEEE ICDM 2021.

USTEP is an Unfixed Search Tree for Efficient Parsing. Based on an evolving tree structure, it can discover, and encodes new parsing rules while processing logs. 
USTEP achieves constant parsing time and can effectively parse raw log messages in a streaming manner.

This project is a fork of the [logpai/logparser](https://github.com/logpai/logparser/) repository. We add here the code and our work around USTEP and the experience presented within our paper.

# Installation

The libraries needed are listed inside the requirements.txt file.

You can install them all at once by running `pip install -r requirements.txt`

# Running the project

The main code for the parser is located inside /logparser/USTEP/ folder.

You will find a USTEP benchmark at /Benchmark/USTEP_benchmark.py

To execute it, simply run it with Python: `python /Benchmark/USTEP_benchmark.py`

If you want only want to run a demo, you can do it by running: `python /demo/USTEP_demo.py`

# Opening an issue

For any questions or feedback, please post to [the issue page](https://github.com/ArthurVOutscale/logparser/issues).

# Contributing

No contributions accepted for this project.

# License

BSD 3-Clause License, see `LICENSE` file.