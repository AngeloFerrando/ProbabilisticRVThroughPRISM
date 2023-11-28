import sys
import random

def main():
    size = int(sys.argv[1])
    min_j = 0
    trans = ''
    for i in range(0, size-1):
        min_choice = min(size-1-min_j, 4)
        if min_choice == 0:
            break
        choices = random.randint(1, min_choice)
        if choices == 3:
            choices = 2
        trans += f'\t[l{i}] state={i} -> '
        prob = (1.0 / choices)
        trans_aux = []
        for j in range(1, choices+1):
            trans_aux.append(f'{prob} : (state\'={min_j+j})')
        trans += '+'.join(trans_aux) + ';\n'
        min_j += choices
    labels = '\n'.join([f'label "label_{l}" = (state={l});' for l in range(0, size)])
    with open('meta_model.csl', 'w') as file:
        file.write(f'P=? [F "label_{size-1}"];')
    with open('meta_model.prism', 'w') as file:
        file.write(f'''
dtmc

module meta
	state : [0..{size-1}] init 0;
    // transitions
{trans}
endmodule

// Labels for states
{labels}
''')

if __name__ == "__main__":
    main()