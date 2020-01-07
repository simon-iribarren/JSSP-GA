from utils import readFilePairs, printTable
from calculateMakespan import calculateMakespan
from plotResult import plotResult


sequence = [11, 10, 9, 2, 1, 13, 8, 0, 2, 4, 13, 0, 4, 4, 5, 0, 7, 4, 5, 11, 12, 12, 4, 10, 5, 2, 11, 6, 6, 3, 12, 6, 0, 9, 9, 14, 1, 12, 7, 9, 13, 2, 6, 14, 2, 8, 5, 3, 6, 5, 12, 9, 8, 1, 4, 6, 7, 1, 10, 14, 3, 7, 6, 11, 14, 14, 8, 0, 1, 7, 9, 5, 9, 10, 2, 4, 3, 13, 5, 4, 3, 12, 6, 0, 7, 12, 6, 11, 2, 0, 8, 12, 13, 2, 2, 6, 12, 0, 8, 6, 13, 13, 11, 10, 10, 3, 10, 1, 13, 12, 9, 1, 1, 1, 14, 2, 7, 10, 14, 0, 11, 14, 11, 9, 4, 11, 3, 9, 6, 12, 11, 10, 13, 10, 4, 9, 7, 7, 5, 10, 8, 13, 3, 0, 12, 6, 2, 7, 14, 2, 1, 2, 8, 11, 14, 9, 8, 0, 8, 4, 2, 1, 7, 1, 10, 3, 7, 5, 7, 1, 8, 14, 11, 8, 3, 11, 3, 0, 13, 13, 10, 3, 5, 1, 6, 9, 4, 12, 4, 7, 3, 0, 14, 14, 5, 4, 14, 7, 0, 13, 12, 11, 14, 3, 13, 6, 1, 8, 9, 4, 3, 10, 9, 2, 12, 10, 5, 5, 11, 13, 5, 8, 5, 0, 8]
times, machines, n = readFilePairs("cases/15_15_1")

result, table =  calculateMakespan(times, machines, sequence, n)

print("RESULT: %s" %result)
print("Sequence: ")
print(sequence)
printTable(table)
plotResult(table, result)
