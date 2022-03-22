# Streamix

A playlist aggregator that allows users to migrate playlists from major streaming platforms.

## Getting Started

There are a few steps you'll need to follow to get the application running on your machine. In order to fully run the application, you will need to run both the client and server simultaneously.

### Running the client

First, navigate to the client directory:

```bash
cd client
```

Next, install all necessary packages required by the client:

```bash
yarn install
```

Finally, run the client application:

```bash
yarn dev
```

Voila! The client should be running on `http://localhost:3000`

---

### Running the server

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
python manage.py runserver
```

The server will now be running on `http://localhost:8000/api/`
