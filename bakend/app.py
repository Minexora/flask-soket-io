from flask import Flask, render_template, request
from flask_socketio import SocketIO, Namespace, send, emit
from flask_cors import CORS

app = Flask(__name__, static_folder="../frontend/static",
            template_folder="../frontend/templates")
app.config['SECRET_KEY'] = 'secret!'

sio = SocketIO(app, logger=True, engineio_logger=True)
CORS(app)


@app.route('/')
def index():
    return render_template('index.html')


class SocketServer:
    def __init__(self) -> None:
        sio.on_event("connect", self.on_connect, namespace='/')
        sio.on_event("on_error", self.error_handler, namespace='/')
        sio.on_event("deneme", self.deneme, namespace='/')
        sio.on_event("disconnect", self.test_disconnect, namespace='/')

    def on_connect(self):
        emit('new_user', {'data': f'{request.sid} Connected.'})

    def error_handler(self, e):
        print(f'ERROR: {str(e)}')

    def deneme(self, data):
        print(f'deneme- {data}')

    def test_disconnect(self):
        print('Client disconnected')


if __name__ == '__main__':
    SocketServer()
    sio.run(app, host="0.0.0.0", port=8080)
