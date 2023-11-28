import sys
import os
from monitor import Monitor
from preprocessing import preprocessing

def main():
    storm = True if sys.argv[2] == 'storm' else False
    if sys.argv[1].endswith('.big'):
        big = True
    else:
        big = False
    # preprocessing the input file to explicit the actions (i.e., events) in the PRISM model
    if not big:
        with open(sys.argv[1], 'r') as file:
            new_model = preprocessing(file.read())
        with open(sys.argv[1].replace('.prism', '_instr.prism'), 'w') as file:
            file.write(new_model)
        os.system('prism ' + sys.argv[1].replace('.prism', '_instr.prism') + ' -exportstates ' + sys.argv[1].replace('.prism', '_instr.sta') + ' -exporttrans ' + sys.argv[1].replace('.prism', '_instr.tra') + ' -exportlabels ' + sys.argv[1].replace('.prism', '_instr.lab'))
        monitor = Monitor(sys.argv[1].replace('.prism', '_instr.sta'), sys.argv[1].replace('.prism', '_instr.tra'), sys.argv[1].replace('.prism', '_instr.lab'), sys.argv[1].replace('.prism', '.csl'), storm)  
    else:
        os.system('../bigrapher/bigrapher full -p ' + sys.argv[1].replace('.big', '.tra') + ' -l ' + sys.argv[1].replace('.big', '.csl') + ' --solver=MCARD -M 5000 ' + sys.argv[1])
        with open(sys.argv[2], 'r') as file:
            prop = file.read()
        with open(sys.argv[1].replace('.big', '.csl'), 'a') as file:
            file.write(prop)
        monitor = Monitor(None, sys.argv[1].replace('.big', '.tra'), None, sys.argv[1].replace('.big', '.csl'), storm)  
        # monitor.to_files(sys.argv[1].replace('.big', '_mon.sta'), sys.argv[1].replace('.big', '_mon.tra'))
        print(monitor.next(set(['select_product_1=1'])))
        # monitor.to_files(sys.argv[1].replace('.big', '_mon.sta'), sys.argv[1].replace('.big', '_mon.tra'))
        print(monitor.next(set(['select_lowqualitybag_product_1=1'])))
        # monitor.to_files(sys.argv[1].replace('.big', '_mon.sta'), sys.argv[1].replace('.big', '_mon.tra'))
        print(monitor.next(set(['select_product_2=1', 'select_lowqualitybag_product_1=1'])))
        # monitor.to_files(sys.argv[1].replace('.big', '_mon.sta'), sys.argv[1].replace('.big', '_mon.tra')) 
        print(monitor.next(set(['select_highqualitybag_product_2=1', 'select_lowqualitybag_product_1=1'])))
        # monitor.to_files(sys.argv[1].replace('.big', '_mon.sta'), sys.argv[1].replace('.big', '_mon.tra'))

if __name__ == "__main__":
    main()
