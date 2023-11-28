import random
import sys

label = 0

def divide_interval(num_parts):
    """Divide [0, 1] into num_parts ensuring all probabilities are non-zero and their sum is 1."""
    probs = []
    remaining = 1.0
    
    for i in range(num_parts - 1):
        min_val = 0.01  # this ensures that the probability is non-zero
        max_val = remaining - (num_parts - i - 1) * min_val
        p = random.uniform(min_val, max_val)
        probs.append(round(p, 2))  # round to 2 decimal places
        remaining = round(remaining - p, 2)  # to ensure no floating point inaccuracies
    
    probs.append(remaining)  # assign the remaining value to the last element, ensuring the total is 1
    return probs


def is_cyclic(src, dest, transitions, reachables):
    """Check if adding transition from src to dest creates a cycle."""
    if src == dest:  # Self-loop
        return True
    if src in transitions.get(dest, []):  # Bidirectional loop
        return True
    return src in reachables.get(dest, set())

def update_reachables(src, dest, reachables, transitions):
    """Update the set of reachable states after adding a new transition."""
    updated = reachables[src].copy()
    updated.add(dest)
    updated |= reachables[dest]
    for state in updated:
        reachables[src] |= reachables[state]
    for prev_state, dests in transitions.items():
        if src in dests:
            reachables[prev_state] |= updated

def generate_prism_model(num_states, num_transitions, num_labels, file_name="meta_model.prism"):
    global label
    labels = [f"label_{i}" for i in range(num_labels)]

    init_state = random.randint(0, num_states-1)
    
    transitions = {}
    reachables = {i: set() for i in range(num_states)}
    
    # Create a list of all possible transitions
    all_transitions = [(i, j) for i in range(num_states) for j in range(i+1, num_states)]
    random.shuffle(all_transitions)

    added_transitions = 0
    while added_transitions < num_transitions and all_transitions:
        src, dest = all_transitions.pop()

        if not is_cyclic(src, dest, transitions, reachables):
            if src not in transitions:
                transitions[src] = []
            if dest not in transitions[src]:
                transitions[src].append(dest)
                update_reachables(src, dest, reachables, transitions)
                added_transitions += 1

    with open(file_name, 'w') as f:
        f.write("dtmc\n\n")
        f.write("module meta\n")
        f.write(f"\tstate : [0..{num_states-1}] init {random.randint(0, num_states-1)};\n\n")

        for src, dests in transitions.items():
            probs = divide_interval(len(dests))
            transition_strs = [f"{probs[i]:.2f} : (state'={dests[i]})" for i in range(len(dests))]
            combined_transition_str = " + ".join(transition_strs)
            f.write(f"\t[l{label}] state={src} -> {combined_transition_str};\n")
            label += 1

        f.write("endmodule\n\n")

        # Properly place labels
        f.write("// Labels for states\n")
        for i, label in enumerate(labels):
            f.write(f"label \"{label}\" = (state={i});\n")
    
    return labels


def generate_csl_file(labels, file_name="meta_model.csl"):
    with open(file_name, 'w') as f:
        for label in labels:
            f.write(f"P=? [F \"{label}\"];\n")
            return

if __name__ == "__main__":
    num_states = int(sys.argv[1])
    
    # Calculating maximum and minimum transitions
    max_transitions = int((num_states * (num_states - 1)) / 2)
    min_transitions = num_states

    print(f"Maximum allowed transitions: {max_transitions}")
    print(f"Minimum required transitions: {min_transitions}")

    num_transitions = int(sys.argv[2])
    
    # Checking user-inputted transitions against bounds
    if num_transitions > max_transitions:
        print(f"Error: Number of transitions exceeds the allowed maximum of {max_transitions}.")
        exit()
    elif num_transitions < min_transitions:
        print(f"Error: Number of transitions is below the required minimum of {min_transitions}.")
        exit()
    
    # Adding checks for the number of labels
    print(f"Maximum allowed labels: {num_states}")
    print(f"Minimum required labels: 1")

    num_labels = int(sys.argv[3])

    if num_labels < 1 or num_labels > num_states:
        print(f"Error: Number of labels should be between 1 and {num_states}.")
        exit()

    labels = generate_prism_model(num_states, num_transitions, num_labels)
    generate_csl_file(labels)
    
    print("Files meta_model.prism and meta_model.csl have been generated.")
