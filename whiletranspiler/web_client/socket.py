import socketio
import os
from whiletranspiler import transpiler
from . import socket_utils
import io
import subprocess

sio = socketio.Server(async_mode='threading')
socket_action = socket_utils.socket_decorator(sio)

class triggers:
    ast = []

@socket_action('connect')
def connect(emit, environ):
    print("connected")

@socket_action('disconnect')
def disconnect(emit):
    print("disconnected")

@socket_action("filelisting")
def filelisting(emit, data=None):
    files = [f for f in os.listdir(".")
            if os.path.isfile(f) and not f.startswith(".")]
    emit("filelisting", files)

@socket_action("loadfile")
def loadfile(emit, filename=None):
    found = False
    if filename is not None:
        try:
            text = open(str(filename), "r").read()
            found = True
        except FileNotFoundError:
            emit("filedata", {
                "filename": filename,
                "reason": "notfound",
                "error": True,
            })
        except (UnicodeDecodeError, PermissionError):
            emit("filedata", {
                "filename": filename,
                "reason": "unopenable",
                "error": True,
            })
        else:
            emit("filedata", {
                "filename": filename,
                "text": text,
                "error": False,
            })
            return

@socket_action("save")
def save(emit, data=None):
    def error():
        emit("savestatus", True);

    def success():
        emit("savestatus", False);

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

@socket_action("build")
def build(emit, data=None):
    _error_data = {"error": True}

    remaining_actions = set([
        "transpiler_c_code",
        "transpiler_ast",
        "transpiler_tokens",
    ])

    def error():
        for action in remaining_actions:
            emit(action, _error_data)

        for trigger_action in triggers.ast:
            trigger_action(emit, None)

    def success(action, new_data):
        assert action in remaining_actions
        remaining_actions.remove(action)

        _data = dict(data)
        _data.update(new_data)
        _data["error"] = False
        emit(action, _data)

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
                    emit("parsestatus", {
                        "line": err.args[0],
                        "error": True,
                    })
                return
            else:
                emit("parsestatus", {
                    "error": False,
                })

            ast = parse_result.ast
            ast_string = ast.print(return_str=True)
            success("transpiler_ast", {"text": ast_string})

            for trigger_action in triggers.ast:
                trigger_action(emit, ast)

            c_source_buffer = io.StringIO()
            transpiler.transpile_c.transpile_parsed(
                    parse_result, c_source_buffer)
            success("transpiler_c_code", {"text": c_source_buffer.getvalue()})

            if "execute" in data and data["execute"]:
                def emit_execution(new_data):
                    _data = dict(data)
                    _data.update(new_data)
                    _data["error"] = False
                    emit("execution", _data)

                emit_execution({"signal": "start"})
                emit_execution({"message": "Compiling..."})

                output_file = "a.out"
                status, stdout = transpiler.utils.c_compile(
                        parse_result, output_file, capture_output=True)
                emit_execution({"message": f"{stdout}"})

                if status == 0:
                    try:
                        emit_execution({"message": "Running..."})
                        output = transpiler.utils.exec_file(
                            f"./{output_file}",
                            timeout=3,
                            capture_output=True
                        )
                    except subprocess.TimeoutExpired:
                        emit_execution(
                                {"message": "Error: execution timed out."})
                    else:
                        emit_execution({"message": f"{output}"})

                emit_execution({"signal": "end"})

    except Exception as e:
        print(e)
        error()
        return

