import numpy as np
import copy

def objective_f(state, S, T):
    # Create the subset B from S based on the state
    B = S[[idx for idx in range(len(S)) if state[idx] == 1]]
    
    # Compute the objective value f(B)
    f_B = abs(T - sum(B))
    return f_B

def get_neighbor(state):
    n_state = copy.deepcopy(state)
    n_state = list(n_state)  # Convert tuple to list for modification

    on_indices = [i for i, bit in enumerate(n_state) if bit == 1]
    off_indices = [i for i, bit in enumerate(n_state) if bit == 0]

    if sum(n_state) == len(n_state):  # All bits are on
        # Remove a random item
        if on_indices:  # Check needed to ensure there are items to remove
            remove_index = np.random.choice(on_indices)
            n_state[remove_index] = 0
    elif sum(n_state) == 0:  # All bits are off
        # Add a random item
        if off_indices:  # Check needed to ensure there are items to add
            add_index = np.random.choice(off_indices)
            n_state[add_index] = 1
    else:  # Both on and off bits exist
        u = np.random.uniform()
        if u < 0.5 and on_indices:  # Check needed for on_indices
            # Remove an element
            remove_index = np.random.choice(on_indices)
            n_state[remove_index] = 0
        elif off_indices:  # Check needed for off_indices
            # Add an element
            add_index = np.random.choice(off_indices)
            n_state[add_index] = 1

    return tuple(n_state)  # Convert back to tuple before returning
