# Broken-Printer

Write a program to find solutions to the problem of converting a starting colour in the `k`-bit colour format to a `LEGAL` colour using the following 6 search strategies: **BFS, DFS, IDS, Greedy, A\*, and Hill-climbing**.

Here, `k` can be any integer from `3` to `12` inclusive. Use the smallest Hamming distance from any `LEGAL` colour for the heuristic in Greedy and A\* search, and as an evaluation function in hill-climbing algorithms.

You will need to adhere to the following constraints:

1. Cycles should be avoided whenever possible: when selecting the next node to expand from the fringe, if it has not been expanded yet then expand it. Otherwise, discard it and select a new node.
2. When expanding a node, generate its children in ascending order of the index being flipped. That is, the first child generated has the 1st bit from the left flipped, and the last child generated has the `k`-th bit from the left flipped.
3. For the heuristic search strategies and the hill-climbing algorithm, if two or more nodes have the same priority for expansion, expand the oldest of those nodes.
4. Set a limit of **1000 expanded nodes maximum**. If the limit is reached and a goal node has not been found, stop the search and print the message `SEARCH FAILED`.

As your program will be automatically tested, it is important that you adhere to these strict rules for program input and output.

## Input

Your program must have the filename `broken_printer.py`, and will be run from the command line in the following format:

```text
python broken_printer.py <char> <filename>
```

- `<char>` denotes what search strategy to run.
  - `B` for BFS
  - `D` for DFS
  - `I` for IDS
  - `G` for Greedy
  - `A` for A*
  - `H` for Hill-climbing
- `<filename>` refers to the `.txt` file that describes the start state, `LEGAL` states and `UNSAFE` states.

The input file format is described below:

```text
start-state
legal-state-1,legal-state-2,...,legal-state-m
unsafe-state-1,unsafe-state-2,...,unsafe-state-n
```

The third line may be left blank if there are no unsafe states.

For example, the input file `simple.txt` might contain:

```text
101
100,010
11X
```

Here, the `X` denotes that both `111` and `110` are in `UNSAFE`.

The `X` character can only appear in legal-state and unsafe-state inputs. Additionally, more than one `X` may be present in an input. Your program should also be able to automatically determine `k`, the bit-depth of the colour from the inputs. You may assume that all input files are valid input files.

## Output

Your program will produce a **two-line output**.

### Line 1

This line should express the path found to the solution, beginning with the start state and finishing at a goal state. The path is a sequence of binary strings separated by commas.

If the maximum expanded nodes are reached, or if there are no more nodes to expand but a goal-state has not been reached, write the line:

```text
SEARCH FAILED
```

### Line 2

This line should express the order in which nodes are expanded in the search process. The goal state node is considered expanded. The path is a sequence of binary strings separated by commas.

## Examples

### Example 1

Given the input text file with contents:

```text
000
111
110,101
```

The outputs of the various algorithms are:

#### BFS

```text
000,010,011,111
000,100,010,001,011,111
```

#### DFS

```text
000,010,011,111
000,100,010,011,111
```

#### IDS

```text
000,010,011,111
000,000,100,010,001,000,100,010,011,001,000,100,010,011,111
```

#### Greedy

```text
000,010,011,111
000,100,010,011,111
```

#### A*

```text
000,010,011,111
000,100,010,001,011,111
```

#### Hill-Climbing

```text
SEARCH FAILED
000,100
```
