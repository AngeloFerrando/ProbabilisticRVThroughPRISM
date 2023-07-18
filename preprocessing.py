import sys

def preprocessing(model):
    new_prism_model = 'dtmc' + '\n\n'
    already_added_events = set()
    start_module = model.find('module')
    end_module = model.find('endmodule')
    while start_module != -1 and end_module != -1:
        events = set()
        index = start_module
        start = model.find('[', index)
        end_state_variables = 0
        new_transitions = []
        while start != -1 and start < end_module:
            end = model.find(']', index)
            if end == -1:
                raise Exception('PRISM model with syntax errors')
            event = model[start+1:end]
            if '..' not in event:
                if event not in already_added_events:
                    events.add(event)
            else:
                end_state_variables = model.find(';', end)
            index = end + 1
            start = model.find('[', index)
        for event in events:
            index = model.find('[' + event + ']') + len(event) + 2
            body = model[model.find('->', index)+2 : model.find(';', index)]
            new_body = None
            for choice in body.split('+'):
                if ':' in choice:
                    perc = choice.split(':')[0] + ':'
                    choice = choice.split(':')[1].strip()
                else:
                    perc = ''
                    choice = choice.strip()
                for event1 in events:
                    if event1 == event:
                        choice += ' & (' + event1 + '\'=1)'
                    else:
                        choice += ' & (' + event1 + '\'=0)'
                if new_body:
                    new_body += ' + ' + perc + choice
                else:
                    new_body = perc + choice
            new_transition = model[model.find('[' + event + ']'):model.find('->', index)].strip() + ' -> ' + new_body + ';'
            new_transitions.append(new_transition)
        new_prism_model += model[start_module:end_state_variables+1] + '\n'
        for event in events:
            new_prism_model += '\t' + event + ': [0..1] init 0;\n'
        new_prism_model += '\n'
        for transition in new_transitions:
            new_prism_model += '\t' + transition + '\n\n'
        new_prism_model += 'endmodule' + '\n\n'
        already_added_events.union(events)
        start_module = model.find('module', end_module+4)
        prev_end_module = end_module
        end_module = model.find('endmodule', end_module+4)
    new_prism_model += model[prev_end_module+9:]
    return new_prism_model


def main():
    with open(sys.argv[1], 'r') as file:
        new_model = preprocessing(file.read())
    with open(sys.argv[1].replace('.prism', '_instr.prism'), 'w') as file:
        file.write(new_model)
                  

if __name__ == "__main__":
    main()