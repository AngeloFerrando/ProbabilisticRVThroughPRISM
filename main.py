import sys
import os
from monitor import Monitor
from preprocessing import preprocessing

def main():
    # preprocessing the input file to explicit the actions (i.e., events) in the PRISM model
    with open(sys.argv[1], 'r') as file:
        new_model = preprocessing(file.read())
    with open(sys.argv[1].replace('.prism', '_instr.prism'), 'w') as file:
        file.write(new_model)
    os.system('prism ' + sys.argv[1].replace('.prism', '_instr.prism') + ' -exportstates ' + sys.argv[1].replace('.prism', '_instr.sta') + ' -exporttrans ' + sys.argv[1].replace('.prism', '_instr.tra'))
    monitor = Monitor(sys.argv[1].replace('.prism', '_instr.sta'), sys.argv[1].replace('.prism', '_instr.tra'), sys.argv[1].replace('.prism', '.csl'))  
    monitor.to_files(sys.argv[1].replace('.prism', '_instr1.sta'), sys.argv[1].replace('.prism', '_instr1.tra')) 
    monitor.next(set(['choose_between_product1_and_product2=1', 'status_product_2=1']))
    monitor.to_files(sys.argv[1].replace('.prism', '_instr1.sta'), sys.argv[1].replace('.prism', '_instr1.tra')) 

if __name__ == "__main__":
    main()