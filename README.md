# Solidity-obfuscator
**Developed as part of CSIT 5730 Group 4 Project**

## Author
- **LI Chenhao** - [Ujikintoki](https://github.com/Ujikintoki): Design main code structures, develop ast parser util, develop control flow obfuscator, and write readme file.

## Intro

Solidity-obfuscator aims to protect smart contracts by making their code harder to reverse-engineer, analyze, or exploit. By applying various obfuscation strategies, it helps safeguard sensitive logic and business rules embedded in the contracts.


## Features

- **Control Flow Obfuscation**: transform the sequential code function blocks into a fakse conditions or loops.
- **Dataflow Obfuscation**:
- **Layout Obfuscation**:
- **Dead Code Insertion**:

## Usage

Obfuscation Tool

First run the parser to generate ast json of the input solidity code before onfuscating.
```bash
python main.py test/test1.sol --parse
```
or (Determine based on your system version and different python versions)

```bash
python3 main.py test/test1.sol --parse
```

Run the obfuscation tool from the command line with the following syntax:
```bash
python main.py test/test1.sol --all
```
or (Determine based on your system version and different python versions)

```bash
python3 main.py test/test1.sol --all
```

Apply specific obfuscators (see Options below):
```bash
python main.py test/test1.sol --controlflow
```
or (Determine based on your system version and different python versions)

```bash
python3 main.py test/test1.sol --controlflow
```

## Options

`--controlflow` : Apply control flow obfuscation.

`--dataflow` : Apply dataflow obfuscation.

`--layout` : Apply layout obfuscation.

`--deadcode` : Apply dead code insertion.

`--all` or leave blank : Apply all obfuscation techniques.

## Contact

For questions or assistance, please contact the authors:
- Chenhao LI (clifh@connect.ust.hk)