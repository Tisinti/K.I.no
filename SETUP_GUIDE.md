This guide is for starting `K.I.no` app.

> You may also use Dockerfile to run the app.

1. Clone the repository

```bash
git clone https://github.com/HardMax71/K.I.no
```

2. Move into the repository

```bash
cd K.I.no
```

3. Create a virtual environment

```bash
python -m venv venv  # if using python
source venv/bin/activate  # if using bash
```

4. Install the required packages

```bash
pip install -r requirements.lock # if user
pip install -r requirements-dev.lock # if developer
```

5. Start the app

```bash
python app.py 
```
