import sys
import os
from monitor import Monitor
from preprocessing import preprocessing
import argparse

def main():
    parser = argparse.ArgumentParser(description='Probabilistic Runtime Verification through Probabilistic Model Checking.')
    parser.add_argument('model', metavar='model', type=str,
                    help='The file containing the probabilistic model to use')
    parser.add_argument('pctl', metavar='pctl', type=str,
                    help='The file containing the PCTL property to verify')
    parser.add_argument('trace', metavar='trace', type=str,
                    help='The file containing the trace of events to verify')
    parser.add_argument('--storm',
        help='To use STORM model checker instead of PRISM',
        action='store_true')

    args = parser.parse_args()
    storm = args.storm #True if len(sys.argv) >= 4 and sys.argv[3] == 'storm' else False
    model_file = args.model
    pctl_file = args.pctl
    trace_file = args.trace
    if model_file.endswith('.big'):
        big = True
    else:
        big = False
    # preprocessing the input file to explicit the actions (i.e., events) in the PRISM model
    if not big:
        with open(model_file, 'r') as file:
            new_model = preprocessing(file.read())
        with open(model_file.replace('.prism', '_instr.prism'), 'w') as file:
            file.write(new_model)
        os.system('prism ' +  model_file.replace('.prism', '_instr.prism') + ' -exportstates ' +  model_file.replace('.prism', '_instr.sta') + ' -exporttrans ' +  model_file.replace('.prism', '_instr.tra') + ' -exportlabels ' +  model_file.replace('.prism', '_instr.lab') + ' > /dev/null')
        monitor = Monitor( model_file.replace('.prism', '_instr.sta'),  model_file.replace('.prism', '_instr.tra'),  model_file.replace('.prism', '_instr.lab'),  pctl_file, storm)  
    else:
        os.system('bigrapher/bigrapher full -p ' +  model_file.replace('.big', '.tra') + ' -l ' +  model_file.replace('.big', '.csl') + ' --solver=MCARD -M 5000 ' +  model_file + ' > /dev/null')
        with open(pctl_file, 'r') as file:
            prop = file.read()
        with open( model_file.replace('.big', '.csl'), 'a') as file:
            file.write(prop)
        monitor = Monitor(None,  model_file.replace('.big', '.tra'), None,  model_file.replace('.big', '.csl'), storm)
    
    with open(trace_file, 'r') as file:
        for line in file.readlines():
            line = line.replace('\n', '')
            print('EVENT:', line)
            print('PROBABILITY:', monitor.next(set(line.split(','))))

if __name__ == "__main__":
    main()
