

halted = False


def rewritten(Cy):
    Cy != Cy.last


def rewrite_in(pos, Cy1):
    return pos > 0 and no_rewrite(Cy1)


def one_step(Cy):
    pass


def simulate(Cy1, Cy2):
    if pos <= k:
        Cy1 = one_step(Cy1)
        buffer += 1
    if pos > k:
        Cy2 = one_step(Cy2)
        buffer = 0


def monotone():
    while not rewritten(Cy1) or not rewritten(Cy2) or not halted:
        simulate(Cy1, Cy2)

    if halted:  # tail found
        return False

    if rewritten(Cy2):  # Cy2 rewritten before Cy1 but still can be tail
        while not restarted:
            simulate(Cy1, Cy2)

        if Cy1.restarted and Cy2.restarted:
            return True
        else:
            return False

    # Cy1 rewritten, marks position and check if Cy2 rewrites before if not it reject
    # if it rewrite before the position then it check if it is not tail and then reject or accept based on that
    # tail -> reject, cycle -> accepts
    if rewritten(Cy1):
        Am.rewrite(Cy1)
        Am.last_rewritten = Cy1.position
        while Am.last_rewritten <= k:
            simulate(Cy1, Cy2)
        if not rewritten(Cy2):
            return False
        else:
            while not restarted:
                simulate(Cy1, Cy2)
            if Cy1.restarted and Cy2.restarted:
                return True
            else:
                return False


def can_restart(state):
    s = [state]
    visited = []
    while s:
        cur_state = s.pop()
        visited.append(cur_state)
        possible_states = [i for i in automaton.instructions[cur_state]]
