# Job-Shop Scheduling Problem

## Requirements: 
- python3
- numpy
- plotly

## Usage
You can select from the cases folder or add your own casses with the following structure:

    2 2
    0 10 1 20
    1 20 0 10

The first line corresponds to job number(jn) and machine number(mn)
next line every row represents a job with mn pair of numbers "x y"
where "x" represents the number of the machine of the sequence and "y" represent the time usage for that machine

You can find more examples with their optimal results [here](https://github.com/tamy0612/JSPLIB)

    python3 main.py