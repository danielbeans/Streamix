# Running the server

First, make sure you are in the root directory of the project and create a python virtual environment:

```bash
virtualenv env
```

Next, activate the virtual environment:

```bash
source env/bin/activate
```

Then install the required packages:

```bash
pip install -r requirements.txt
```

To start the server, make sure the `venv` is running, go into the `server/` directory, and start the server:

```bash
cd server
python manage.py runserver
```

The server will now be running on `http://localhost:8000/api/`
