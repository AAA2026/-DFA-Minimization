Implementing Deterministic Finite Automaton (DFA) 
minimization, which reduces the number of states in a given DFA 
while preserving its behavior. The algorithm ensures that the 
minimized DFA recognizes the same language as the original but with 
fewer states, making it more efficient for computational tasks. It 
follows three main steps: removing unreachable states, merging 
equivalent states using Hopcroft’s algorithm, and handling dead 
states. The project reads an input DFA from a file, processes it, and 
outputs the minimized DFA
