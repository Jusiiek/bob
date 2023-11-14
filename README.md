# Bob bot

-------------------------------------------------------------------------
## Setup

### 1. Create virtual environment for python

##### use python version 3.10.+ Execute the command below to create a virtual environment
```
python -m venv venv
```
-------------------------------------------------------------------------
### 2. Active virtual environment
##### Unix
```
source venv/bin/activate
```
##### windows
```
source venv/Scripts/activate
```
-------------------------------------------------------------------------
### 3. Install requirements

##### use makefile
```
make dev_install_requirements
```
##### or classic way
```
pip install -r requirements
```
-------------------------------------------------------------------------
### 4. Run project

##### use makefile
```
make dev_run
```
##### or classic way
```
python main.py
```