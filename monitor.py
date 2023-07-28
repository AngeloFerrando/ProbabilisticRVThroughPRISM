class Monitor:
    def __init__(self, file_states, file_transitions, file_properties):
        self.__state_vars = []
        self.__states = {}
        self.__transitions = {}
        self.__file_properties = file_properties
        self.__initial_state = '0'
        with open(file_states, 'r') as file:
            first_line = file.readline()
            self.__state_vars = first_line.replace('(', '').replace(')', '').replace('\n', '').split(',')
            # ev_indexes = [False]*len(self.__state_vars)
            # i = 0
            # for col in self.__state_vars:
            #     if 'event_' in col:
            #         ev_indexes[i] = True
            #     i += 1
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
                self.__transitions[line[0]][','.join([e + '=' + v for (e,v) in self.__states[line[1]]])] = (line[1], float(line[2]))

        # for tr in self.__transitions:
        #     for ev in self.__transitions[tr]:
        #         (st, pr) = self.__transitions[tr][ev]
        #         print(tr, '-', pr, '->', st)

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
                    file.write(tr + ' ' + self.__transitions[tr][ev][0] + ' ' + str(self.__transitions[tr][ev][1]) + '\n')
    def next(self, event):
        # event = set(['event_' + e for e in event])
        print('EVENT:', event)
        # print(self.__transitions[self.__initial_state])
        for ev in self.__transitions[self.__initial_state]:
            print('EV:', set([e for e in ev.split(',') if '=0' not in e]))
            if event == set([e for e in ev.split(',') if '=0' not in e]):
                (next_state, _) = self.__transitions[self.__initial_state][ev]
                self.__transitions[self.__initial_state][ev] = (next_state, 1.0)
            else:
                (aux, _) = self.__transitions[self.__initial_state][ev]
                self.__transitions[self.__initial_state][ev] = (aux, 0.0)
        self.__initial_state = next_state


                

