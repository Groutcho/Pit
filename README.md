##Pit - Git in Python

As a python pedagogical implementation of Git, Pit aims to reimplement 
the main functions of Git transparently, thus being 100% compatible with 
existing repos.

It is not exhaustive, nor as efficient as the C implementation because:
- Python is not as fast as C
- No optimizations beside trivial ones, to maintain maximum
  code readability.
- Only the common functionality is implemented (add, commit, checkout...)

The ultimate goal is to gain a deep understanding of the design behind Git by
rewriting the core components.

I found that simply reading the source code is not sufficient to gain insight.
Rewriting is much more efficient for the brain.

Uses Python 3.4

Sébastien Guimmara
