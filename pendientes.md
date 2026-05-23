- 2.1.1
    - Most VRP are NP-hard, and so is the BCP, this ex-
plains why most research efforts have focused on heu-
ristics. Various approaches to solve the classical VRP
have been investigated over the past decades. These
range from the use of pure optimization methods for
solving small size problems to the use of heuristics and
meta-heuristics that provide near-optimal solutions for
medium and large-size problems with complex cons-
traints (Cordeau et al., 2002; Toth & Vigo, 2002). Most
of these methods focus on minimizing an aprioristic
cost function subject to a set of well-defined constraints.
However, and because real-life problems are complex
enough so that not all possible constraints, costs and
desirable solution properties can be considered in
advance, there is a need for methods capable to provide
a large set of alternative near-optimal solutions, so that
decision-makers can choose among them according to
their specific necessities and preferences.
In most meta-heuristics, each stage (iteration) of the
search algorithm starts with a solution (or set of so-
lutions). In the next stage a new candidate (or set of
candidates) is evaluated within the local space of the
previous solution. The evaluation will estimate the
performance of the new candidate and compare with
the performance reached in the previous stages. Based
on this evaluation, the candidate or candidates can be
accepted, becoming part of the solution for that stage,
or rejected, in which case the solution is maintained.
The process is repeated until certain stopping criteria
are met.