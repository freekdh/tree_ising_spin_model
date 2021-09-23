# Spin model exercise
This repo is part of an exercise regarding ising model on tree graphs. The reason this problem can be solved in O(N Log(N)) is because of the @lru_cache decorator
which stores the previously calculated values (a dynamic programming implementation)

# Installation
I'm using python version 3.9.7

First install the requirements:
`pip install -r requirements.txt`

Second install the package by:
`pip install -e .`

If you are successful you should be able to run `pytest` in the root directory and all tests should pass:)

# Tests
I'm using `pytest` for the testenvironment. 
To run the test suite call:
`pytest` in the root directory

