# article-image-generator
Project for generating images from and for articles

- Requirements: 
    - [Python 3.9.2](https://www.python.org/downloads/)
    - [NodeJS](https://nodejs.org/en)

## Installation:

1. Create Python virtual enviroment (optional, but will prevent some unexpected errors)
    - when you restart your workspace you will need to activate it again, just run the second line

```cmd
~\AppData\Local\Programs\Python\Python39\python -m venv venv # create venv
venv\Scripts\activate           # activate venv
pip install -r requirements.txt # install needed packages
```

2. Get all svelte packages

```cmd
cd ./frontend
npm install
cd ../
```

3. Build svelte and run fastapi

```cmd
cd ./frontend
npm run build; cd ../
python main.py
```

4. When first build is done, just run the python file
    - don't forget to be in virtual enviroment

```cmd
python main.py # Add argument "--dev" for hot reload
```