import copy
import os
import sys

class Monitor:
    
    def __init__(self, file_states, file_transitions, file_labels, file_properties, storm):
        self.__state_vars = []
        self.__states = {}
        self.__transitions = {}
        self.__file_labels = file_labels
        self.__file_properties = file_properties
        self.__initial_states = set(['0'])
        self.__storm = storm
        if file_states: # PRISM
            self.__kind = 'prism'
            # extract the atomic propositions that hold in states from the STA file
            with open(file_states, 'r') as file:
                first_line = file.readline()
                self.__state_vars = first_line.replace('(', '').replace(')', '').replace('\n', '').split(',')
                for line in file.readlines():
                    self.__states[line.split(':')[0]] = set()
                    i = 0
                    for el in line.split(':')[1].replace('(', '').replace(')', '').replace('\n', '').split(','):
                        self.__states[line.split(':')[0]].add((self.__state_vars[i], el))
                        i += 1
            # extract the transitions from the TRA file
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
            self.__kind = 'bigrapher'
            # extract the atomic propositions that hold in states from the CSL file
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
            # extract the transitions from the TRA file
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
                    # the non-determinism is only for the empty event (the events of our interest are deterministic w.r.t. the next state where they move to)
                    self.__transitions[line[0]][','.join([e + '=' + v for (e,v) in self.__states[line[1]]])].add((line[1], float(line[2])))
            print(self.__transitions['0'])
    # generate state and transition files from the monitor (the state file is only generated in case of PRISM)
    def to_files(self, file_states, file_transitions):
        if self.__kind == 'prism':
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
    def next(self, event, simulated=False):
        # print('EVENT:', event)
        new_initial_states = set(self.__initial_states)
        for initial_state in self.__initial_states:
            # print('Move from state ', initial_state, ' where the atoms { ', ','.join([str(e[0]) for e in self.__states[initial_state]]),' } hold')
            for ev in self.__transitions[initial_state]:
                # print('EV:', set([e for e in ev.split(',') if '=0' not in e]))
                if simulated or event == set([e for e in ev.split(',')]):
                    simulated = False
                    new_initial_states.remove(initial_state)
                    next_states = copy.deepcopy(self.__transitions[initial_state][ev])
                    # print(next_states)
                    for (next_state, prob) in next_states:
                        # print('To the state ', next_state, ' where the atoms { ', ','.join([str(e[0]) for e in self.__states[next_state]]),' } hold')
                        self.__transitions[initial_state][ev].remove((next_state, prob))

                        self.__transitions[initial_state][ev].add((next_state, 1.0))
                        new_initial_states.add(next_state)
                else:
                    next_states = self.__transitions[initial_state][ev]
                    for (aux, prob) in next_states:
                        self.__transitions[initial_state][ev].remove((aux, prob))
                        self.__transitions[initial_state][ev].add((aux, 0.0))
        self.__initial_states = new_initial_states
        return self.check()
    def check(self):
        self.to_files('tmp.sta', 'tmp.tra')
        if self.__kind == 'prism':
            if self.__storm:
                os.system('./prismlab_to_stormlab.sh {file_labels} {file_labels_storm}'.format(file_labels=self.__file_labels, file_labels_storm=self.__file_labels.replace('.lab', '_storm.lab')) + ' > /dev/null')
                os.system('./prismtra_to_stormtra.sh tmp.tra tmp_storm.tra' + ' > /dev/null')
                result = self.call_quiet(os.popen, 'storm --explicit tmp_storm.tra {file_labels} --prop {csl}'.format(file_labels=self.__file_labels.replace('.lab', '_storm.lab'), csl=self.__file_properties)).read()
            else:
                result = self.call_quiet(os.popen, 'prism -importtrans tmp.tra -importstates tmp.sta -importlabels {file_labels} {csl} -dtmc'.format(file_labels=self.__file_labels, csl=self.__file_properties)).read()
        else:
            result = self.call_quiet(os.popen, 'prism -importtrans tmp.tra {csl} -dtmc'.format(csl=self.__file_properties)).read()
        # print(result)
        if self.__storm and self.__kind == 'prism':
            res = result[result.index('Result (for initial states)')+28:result.index('Time for model checking')].replace('\n', '').strip()
            if res == 'true' or res == 'false':
                return bool(res)
            else:
                return float(res)
            
        else:
            if '(exact floating point)' in result:
                return float(result[result.index('Result:')+8:result.index('(exact floating point)')])
            else:
                return True if 'Result: true' in result else False
    def simulated_next(self, trace_length):
        for i in range(0, trace_length):
            self.next('None', simulated=True)
    def call_quiet(self, func, *args, **kwargs):
        with open(os.devnull, 'w') as devnull:
            sys.stdout, sys.stderr = devnull, devnull
            try:
                return func(*args, **kwargs)
            finally:
                sys.stdout, sys.stderr = sys.__stdout__, sys.__stderr__


                

