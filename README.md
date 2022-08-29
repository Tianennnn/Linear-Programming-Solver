# Linear Programming Solver

The project is a linear programming (LP) solver written in python which reads a text-based representation of a
linear program from standard input and outputs the result of solving the LP. The solver is implemented using the dictionary-based Simplex Method. To prevent numerical anomalies from accumulating over time and result in unwanted behavior, the program represents numerical values as fractions. The solver will solve initially infeasible LP's using Primal-Dual Methods. Moreover, the solver uses the Largest-Increase Rule when picking the entering variables for pivot operations and will use Bland’s Rule if cycling is detected.

Some sample input files and corresponding output results is provided in the folder "test_cases".

# Input Format
The input format is a simple text_based encoding of a maximziation LP in standard form.  Consider the LP:

<img src="https://github.com/Tianennnn/Linear_Programming_Solver/blob/main/README%20Picture%201.png" width="253" height="144.6">

It would be encoded as: </br>
0.5&nbsp;&nbsp;&nbsp;&nbsp;3 </br>
1&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;4&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;4 </br>
4&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;4 </br>
3&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;4&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;5 </br>
5&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1.8&nbsp;&nbsp;&nbsp;&nbsp;5 </br>

# Output Format
The output is printed to standard output. If the input LP is infeasible, the output will be the following single line:
<p align="center">
infeasible
</p>

If the input LP is unbounded, the output will be the following single line:
<p align="center">
unbounded
</p>

Otherwise, if the input LP is bounded and feasible, the output will consist of three lines. The first line will be the single word "optimal". The second line will be the optimal objective value.
The third line will be the optimal assignment of each optimization variable $x_1$, $x_2$, ... , $x_n$, seperated by whitespaces. 

