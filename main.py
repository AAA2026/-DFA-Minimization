#!/usr/bin/env python3

import pprint


State = str
TransFunc = dict[State, dict[chr, State]]
Alphabet = set[chr]
DFA = tuple[set[State], Alphabet, TransFunc, State, set[State]]

emptyDFA: DFA = (set(), set(), {}, "", set())


def minimize(dfa: DFA) -> DFA:
    """
    Reduces a Deterministic Finite Automaton (`dfa`) into an equivalent DFA with
    a minimal number of states.
    """

    states, alphabet, trans, initialState, finalStates = dfa

    # This function is split into three steps, marked by [] in a comment.
    # Each step should change the values of the following three variables.
    # The person who wrote a step should write their name between the brackets.

    minStates: set[State] = states     # Minimal states
    minTrans: TransFunc = trans        # Minimal transition function
    minFinal: set[State] = finalStates # Minimal final states

    # Remove unreachable states.

    reachableStates: set[State] = {initialState}
    newStates: set[State] = {initialState}

    while newStates:
        temp = set()
        for state in newStates:
            temp.update(trans[state][char] for char in alphabet)
        newStates = temp - reachableStates
        reachableStates.update(newStates)

    minStates = reachableStates
    minTrans = {
        key: val
        for key, val in minTrans.items()
        if key in minStates
    }
    minFinal &= minStates

    # Merge non-distinguishable states.

    if minStates and alphabet:
        partitions = []
        final_part = frozenset(minFinal)
        non_final_part = frozenset(minStates - minFinal)
        if final_part:
            partitions.append(final_part)
        if non_final_part:
            partitions.append(non_final_part)

        changed = True
        while changed:
            changed = False
            new_partitions = []
            for part in partitions:
                split_dict = {}
                for state in part:
                    key = []
                    for symbol in alphabet:
                        dest = minTrans[state][symbol]
                        for idx, p in enumerate(partitions):
                            if dest in p:
                                key.append(idx)
                                break
                    key_tuple = tuple(key)
                    if key_tuple not in split_dict:
                        split_dict[key_tuple] = []
                    split_dict[key_tuple].append(state)
                for group in split_dict.values():
                    new_part = frozenset(group)
                    new_partitions.append(new_part)
            new_partitions = list({p for p in new_partitions})
            if len(new_partitions) != len(partitions) or any(p not in partitions for p in new_partitions):
                partitions = new_partitions
                changed = True

        state_rep = {}
        for part in partitions:
            rep = min(part)
            for state in part:
                state_rep[state] = rep

        new_minStates = {state_rep[s] for s in minStates}
        new_initial = state_rep[initialState]
        new_minFinal = {state_rep[s] for s in minFinal if state_rep[s] in new_minStates}

        new_trans = {}
        for state in new_minStates:
            new_trans[state] = {}
            for symbol in alphabet:
                orig_dest = minTrans[state][symbol]
                new_trans[state][symbol] = state_rep[orig_dest]

        minStates = new_minStates
        minTrans = new_trans
        initialState = new_initial
        minFinal = new_minFinal

    # Recreate a single dead state.

    dead_states = set()
    for state in minStates:
        if state not in minFinal:
            is_dead = all(minTrans[state][symbol] == state for symbol in alphabet)
            if is_dead:
                dead_states.add(state)

    if len(dead_states) > 1:
        new_dead = 'dead'
        i = 0
        while new_dead in minStates or new_dead in dead_states:
            new_dead = f'dead{i}'
            i += 1

        new_minStates = (minStates - dead_states) | {new_dead}
        new_trans = {}
        for state in new_minStates:
            if state == new_dead:
                new_trans[state] = {symbol: new_dead for symbol in alphabet}
            else:
                new_trans[state] = {}
                for symbol in alphabet:
                    dest = minTrans[state][symbol]
                    new_trans[state][symbol] = new_dead if dest in dead_states else dest

        if initialState in dead_states:
            new_initial = new_dead
        else:
            new_initial = initialState

        new_minFinal = minFinal - dead_states

        minStates = new_minStates
        minTrans = new_trans
        initialState = new_initial
        minFinal = new_minFinal

    # Final output
    minimal: DFA = (minStates, alphabet, minTrans, initialState, minFinal)

    return minimal


def main():

    inputDFA: DFA
    minimalDFA: DFA

    with open("./dfa.py") as file:
        inputDFA = eval(file.read())
        print("Input:")
        pprint.pprint(inputDFA)
        print("-" * 80)

    minimalDFA = minimize(inputDFA)

    oldStates: int = len(inputDFA[0])
    newStates: int = len(minimalDFA[0])

    if oldStates != newStates:
        print(f"Reduced number of states from {oldStates} to {newStates}.")
    else:
        print("Input DFA already minimal.")

    with open("min.py", "w") as file:
        print("Output:")
        pprint.pprint(minimalDFA)
        pprint.pprint(minimalDFA, file)
        print("-" * 80)


if __name__ == "__main__":
    main()
