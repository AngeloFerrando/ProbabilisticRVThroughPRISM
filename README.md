# ProbabilisticRVThroughPRISM

TBD

## To run

The following is to synthesise the monitor (just a test for now)

```bash
python3 main.py ./examples/manufacturing/manufacturing.prism
```

```bash
prism -importtrans ./examples/manufacturing/manufacturing_instr1.tra -importstates ./examples/manufacturing/manufacturing_instr.sta -importlabels ./examples/manufacturing/manufacturing_instr.lab ./examples/manufacturing/manufacturing.csl -dtmc
```