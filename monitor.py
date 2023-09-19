class Monitor:
    def __init__(self, file_states, file_transitions, file_properties):
        self.__state_vars = []
        self.__states = {}
        self.__transitions = {}
        self.__file_properties = file_properties
        self.__initial_states = set(['0'])
        if self.__states: # PRISM
            with open(file_states, 'r') as file:
                first_line = file.readline()
                self.__state_vars = first_line.replace('(', '').replace(')', '').replace('\n', '').split(',')
                for line in file.readlines():
                    self.__states[line.split(':')[0]] = set()
                    i = 0
                    for el in line.split(':')[1].replace('(', '').replace(')', '').replace('\n', '').split(','):
                        self.__states[line.split(':')[0]].add((self.__state_vars[i], el))
                        i += 1
            with open(file_transitions, 'r') as file:
                file.readline() # discard first line
                for line in file.readlines():
                    line = line.replace('\n', '').split(' ')
                    if line[0] not in self.__transitions:
                        self.__transitions[line[0]] = {}
                    if ','.join([e + '=' + v for (e,v) in self.__states[line[1]]]) not in self.__transitions[line[0]]:
                        self.__transitions[line[0]][','.join([e + '=' + v for (e,v) in self.__states[line[1]]])] = set()
                    self.__transitions[line[0]][','.join([e + '=' + v for (e,v) in self.__states[line[1]]])].add((line[1], float(line[2])))
        else: # BIGRAPHER
            with open(file_properties, 'r') as file:
                for line in file.readlines():
                    line = (line[:line.index('=')], line[line.index('=')+1:])
                    event = line[0].replace('label', '').replace('"', '').strip()
                    if '=' not in line[1]:
                        continue
                    for state in line[1].split('|'):
                        state = state.split('=')[1].replace(';', '').strip()
                        if state not in self.__states:
                            self.__states[state] = set()
                        self.__states[state].add((event, '1'))
            with open(file_transitions, 'r') as file:
                file.readline() # discard first line
                for line in file.readlines():
                    line = line.replace('\n', '').split(' ')
                    if line[0] not in self.__states:
                        self.__states[line[0]] = set()
                    if line[1] not in self.__states:
                        self.__states[line[1]] = set()
                    if line[0] not in self.__transitions:
                        self.__transitions[line[0]] = {}
                    if ','.join([e + '=' + v for (e,v) in self.__states[line[1]]]) not in self.__transitions[line[0]]:
                        self.__transitions[line[0]][','.join([e + '=' + v for (e,v) in self.__states[line[1]]])] = set()
                    self.__transitions[line[0]][','.join([e + '=' + v for (e,v) in self.__states[line[1]]])].add((line[1], float(line[2])))
            pippo=''

    def to_files(self, file_states, file_transitions):
        with open(file_states, 'w') as file:
            file.write('(' + ','.join(self.__state_vars) + ')\n')
            for state in self.__states:
                file.write(state + ':' + '(')
                l = []
                for var in self.__state_vars:
                    for (el, v) in self.__states[state]:
                        if var == el:
                            l.append(v)
                file.write(','.join(l) + ')\n')
        with open(file_transitions, 'w') as file:
            n_trans = 0
            for tr in self.__transitions:
                n_trans += len(self.__transitions[tr])
            file.write(str(len(self.__states)) + ' ' + str(n_trans) + '\n')
            for tr in self.__transitions:
                for ev in self.__transitions[tr]:
                    for tp in self.__transitions[tr][ev]:
                        file.write(tr + ' ' + tp[0] + ' ' + str(tp[1]) + '\n')
    def next(self, event):
        # event = set(['event_' + e for e in event])
        print('EVENT:', event)
        # print(self.__transitions[self.__initial_state])
        new_initial_states = set(self.__initial_states)
        for initial_state in self.__initial_states:
            for ev in self.__transitions[initial_state]:
                print('EV:', set([e for e in ev.split(',') if '=0' not in e]))
                if event == set([e for e in ev.split(',') if '=0' not in e]):
                    new_initial_states.remove(initial_state)
                    next_states = self.__transitions[initial_state][ev]
                    for (next_state, _) in next_states:
                        self.__transitions[initial_state][ev].remove((next_state, _))
                        self.__transitions[initial_state][ev].add((next_state, 1.0))
                        new_initial_states.add(next_state)
                else:
                    next_states = self.__transitions[initial_state][ev]
                    for (aux, _) in next_states:
                        self.__transitions[initial_state][ev].remove((aux, _))
                        self.__transitions[initial_state][ev].add((aux, 0.0))
        self.__initial_states = new_initial_states


                

