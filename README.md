# Genetic Algorithm for the Job-Shop Scheduling Problem

## Requirements: 
- python3
- numpy
- plotly

## Usage
You can select yout own instance of the problem from the cases folder or add your own casses with the following structure:

    2 2
    0 10 1 20
    1 20 0 10

The first line corresponds to job number(jn) and machine number(mn)
next line every row represents a job with mn pair of numbers "x y"
where "x" represents the number of the machine of the sequence and "y" represent the time usage for that machine.

You can change the case in the main.py file:

    times, machines, n = readFilePairs("cases/15_15_1")

You can find more examples with their optimal results [here](https://github.com/tamy0612/JSPLIB)

To run it:

    python3 main.py
    
Then input the configuration in the cli (Example):

    Please input the size of population (default: 30): 40
    Please input the size of Mutation Rate (default 0.2): 0.1
    Please input number of iteration (default 2000): 4000