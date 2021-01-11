# NAND Optimizer
A project to optimize digital circuits constructed from [NAND gates][wikipedia:nand-gate].

## NAND Gate
A _NAND gate_ is

> a logic gate which produces an output which is false only if all its inputs are true

### Truth Table
The [_truth table_][wikipedia:truth-table] of a NAND gate is shown below

| A | B | A *NAND* B |
|---|---|------------|
| 0 | 0 | 1          |
| 0 | 1 | 1          |
| 1 | 0 | 1          |
| 1 | 1 | 0          |

### Universal Gate
A NAND gate is universal, i.e. by using only NAND gates it is possible to implement any digital circuit. 

To see this consider an _n_-input, 1-output digital circuit. Name the inputs _I1_, _I2_, through _In_. Since each input can be either _0_ or _1_ there are a total of 2<sup>n</sup> different input states.

By _AND_-ing each input or its negation, we can form an expression that is only true for a specific input state. For example, If we have a 3-input, 1-output digital circuit only outputs 1 when I1 = 1, I2 = 0 and I3 = 1, we can form the following expression

```
I1 AND (NOT I2) AND I3
```

By _OR_-ing each of the input states together for which the digital circuit outputs 1, we form an expression consisting of AND, NOT and OR gates that express each digital circuit. In other words, the AND, NOT and OR gates together are universal

What remains is to show that each of AND, NOT and OR gates can be expressed solely using NAND gates.

#### NOT
Looking at the truth table of the NAND gate it self, we can see that when both inputs are the same, the output is negated. So we have the following expression.

```
NOT A = A NAND A
```

#### AND
Since NAND is short for Not AND, and that `(NOT NOT A)` cancels to `A`, we find that

```
A AND B = NOT (A NAND B)
```

And since NOT can be expressed solely with NAND gates, so can an AND gate.

#### OR
With [De Morgans laws][wikipedia:de-morgans-laws] one can find the following relations:

```
A OR B = NOT NOT (A OR B) = NOT ((NOT A) AND (NOT B)
```

Again, since we already know that NOT and AND gates can be expressed with NAND gates, so can OR gates.

### Optimalisation
The above construction can be wastefull. For example, if we apply it to the truth table of the NAND gate itself, we would find the following monstrosity.

With inputs A and B, the following expression has the same truth table as the NAND gate.

```
((NOT A) AND (NOT B)) OR (NOT A AND B) OR (A AND NOT B)
```

expanding the ORs gives

```
NOT ((NOT((NOT A) AND (NOT B))) AND (NOT(NOT(NOT (NOT A AND B)) AND (NOT(A AND NOT B))))))
```

expanding the ANDs in the previous expression gives

```
expression will have to wait until a computer can do it for us
```

And finally expanding the NOTs leaves with

```
expression will have to wait until a computer can do it for us
```

and a headache.

## Development
Development is done in Python. Make sure to create a virtual environment

```shell
python3 -m venv .venv
```

and activate it with

```shell
source .venv/bin/activate
```

Then install the dependencies with

```shell
pip install -r requirements.txt
```

[wikipedia:nand-gate]: https://en.wikipedia.org/wiki/NAND_gate
[wikipedia:truth-table]: https://en.wikipedia.org/wiki/Truth_table
[wikipedia:de-morgans-laws]: https://en.wikipedia.org/wiki/De_Morgan%27s_laws
