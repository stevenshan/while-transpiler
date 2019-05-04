from .flask_app import app
from .socket import sio
import socketio

app.wsgi_app = socketio.Middleware(sio, app.wsgi_app)

