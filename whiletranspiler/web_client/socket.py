import socketio
import os
from whiletranspiler import transpiler
from .utils import StdoutCapture
import sys

sio = socketio.Server(async_mode='threading')

@sio.on('connect')
def connect(sid, environ):
    print('connect ', sid)

@sio.on('disconnect')
def disconnect(sid):
    print('disconnect ', sid)

@sio.on("filelisting")
def filelisting(sid, data=None):
    files = [f for f in os.listdir(".")
            if os.path.isfile(f) and not f.startswith(".")]
    sio.emit("filelisting", files)

@sio.on("loadfile")
def loadfile(sid, filename=None):
    found = False
    if filename is not None:
        try:
            text = open(str(filename), "r").read()
            found = True
        except FileNotFoundError:
            sio.emit("filedata", {
                "filename": filename,
                "reason": "notfound",
                "error": True,
            })
        except (UnicodeDecodeError, PermissionError):
            sio.emit("filedata", {
                "filename": filename,
                "reason": "unopenable",
                "error": True,
            })
        else:
            sio.emit("filedata", {
                "filename": filename,
                "text": text,
                "error": False,
            })
            return

@sio.on("save")
def save(sid, data=None):
    def error():
        sio.emit("savestatus", True);

    def success():
        sio.emit("savestatus", False);

    if data is None or "text" not in data or "filename" not in data:
        error()
        return

    try:
        file_obj = open(str(data["filename"]), "w")
        file_obj.write(str(data["text"]))
    except:
        error()
    else:
        success()

@sio.on("run")
def run(sid, data=None):
    _error_data = {"error": True}

    remaining_actions = set([
        "transpiler_c_code",
        "transpiler_ast",
        "transpiler_tokens",
    ])

    def error():
        for action in remaining_actions:
            sio.emit(action, _error_data)

    def success(action, new_data):
        assert action in remaining_actions
        remaining_actions.remove(action)

        _data = dict(data)
        _data.update(new_data)
        _data["error"] = False
        sio.emit(action, _data)

    if isinstance(data, dict):
        _error_data.update(data)
    else:
        error()
        return

    try:
        with open(data["filename"], "r") as file_obj:
            token_stream = transpiler.lexer.get_token_stream(file_obj)

            tokens = []
            try:
                while True:
                    tokens.append(next(token_stream))
            except StopIteration:
                pass

            token_string = "\n".join(
                    ("Line %-4d: %s" % (tk.line_range[0], tk)
                    for tk in tokens))
            success("transpiler_tokens", {"text": token_string})

            try:
                parse_result = transpiler.parser.parse((x for x in tokens))
            except transpiler.parser.ParseError as err:
                error()
                if len(err.args) > 0:
                    sio.emit("parsestatus", {
                        "line": err.args[0],
                        "error": True,
                    })
            else:
                sio.emit("parsestatus", {
                    "error": False,
                })

            capture = StdoutCapture()
            with capture as capturer:
                parse_result.ast.print()
            success("transpiler_ast", {"text": capture.out})

            capture = StdoutCapture()
            with capture as capturer:
                transpiler.transpile_c.transpile_parsed(
                        parse_result, sys.stdout)
            success("transpiler_c_code", {"text": capture.out})

    except Exception as e:
        print(e)
        error()

