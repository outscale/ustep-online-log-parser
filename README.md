
# USTEP Online Logparser
[![Project Archived](https://docs.outscale.com/fr/userguide/_images/Project-Archived-red.svg)](https://docs.outscale.com/en/userguide/Open-Source-Projects.html)

This is the code for the paper "USTEP: Unfixed Search Tree for Efficient Log Parsing" accepted at IEEE ICDM 2021.

Log parsers learn to separate variable parts of a log message from the constant ones.
USTEP is an Unfixed Search Tree for Efficient Parsing. Based on an evolving tree structure, it can discover, and encodes new parsing rules while processing log messages. 
USTEP achieves constant parsing time and can effectively parse raw log messages in a streaming manner.

This project is a fork of the [logpai/logparser](https://github.com/logpai/logparser/) repository. We add here the code of our log parsing method USTEP, and of the experience related to it.

<p align="center"><img src="./docs/img/logparsing.jpg" width="502"><br>An illustrative example of log parsing</p>

:telescope: If you use USTEP in your research for publication, please kindly cite the following paper.
+ [**ICDM'21**] Arthur Vervaet, Raja Chiky, Mar Callau-Zori. "USTEP: Unfixed Search Tree for Efficient Log Parsing" *International Conference on Data Mining (ICDM)*, 2021.

# Installation

The libraries needed are listed inside the requirements.txt file.

You can install them all at once by running `pip install -r requirements.txt`

# Running the Project

The main code for the parser is located inside /logparser/USTEP/ folder.

You will find a USTEP benchmark at /Benchmark/USTEP_benchmark.py

To execute it, simply run it with Python: `python /Benchmark/USTEP_benchmark.py`

If you want only want to run a demo, you can do it by running: `python /demo/USTEP_demo.py`

# Opening an Issue

For any questions or feedback, please post to [the issue page](https://github.com/ArthurVOutscale/logparser/issues).

# Contributing

Thank you for considering contributing to this repository.

Potential contributions include:

- Reporting and fixing bugs.
- Adding features.
- Cleaning up the code.
- Improving the documentation.

In order to report bugs or request features, search the issue tracker to check for a duplicate.
It’s totally acceptable to create an issue when you’re unsure whether
something is a bug or not. We’ll help you figure it out.

We’ll do our best to review your pull request (or “PR” for short) quickly.

Each PR should, as much as possible, address just one issue and be self-contained.
Smaller the set of changes in the pull request is, the quicker it can be reviewed and
merged - if you have ten small, unrelated changes, then go ahead and submit ten PRs.

# License

See [LICENSE.md](LICENSE.md) file.

# Contact us
**By mail:** publicworkloadtrace@outscale.com
