# Create Python Virtual Environment

Here is how you could create a Python 3.10 [`venv` virtual environment](https://docs.python.org/3.10/library/venv.html) under Windows:

```bash
# Create virtual environment with Python 3.10
py -3.10 -m venv .venv
# Activate virtual environment
.venv\Scripts\activate.bat
# Upgrade pip
python -m pip install --upgrade pip
```

For Linux, you need to specify exact python runtime:

```bash
# Create virtual environment with Python 3.10
python3 -m venv .venv
# Activate virtual environment
.venv\Scripts\activate.bat
# Upgrade pip
python -m pip install --upgrade pip
```
