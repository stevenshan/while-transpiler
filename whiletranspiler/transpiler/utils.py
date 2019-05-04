import os
import sys
import subprocess
from .transpile_c import transpile_parsed

def decode_str_bytes(raw_bytes):
    return "".join((chr(x) for x in raw_bytes))

def c_compile(parse_result, output_file, capture_output=False):
    """
    Compiles transpiled C source code using gcc.
    """

    rfd, wfd = os.pipe()
    file_obj = os.fdopen(wfd, "w")
    transpile_parsed(parse_result, file_obj)
    file_obj.close()
    gcc_args = ["gcc", "-x", "c", "-o", output_file, "-"]

    options = {"stdin": rfd}

    if capture_output:
        options.update({
            "stdout": subprocess.PIPE,
            "stderr": subprocess.STDOUT,
        })

    process = subprocess.run(gcc_args, **options)

    stdout = ""
    if process.stdout is not None:
        stdout = decode_str_bytes(process.stdout)

    return process.returncode, stdout

def exec_file(filename, capture_output=False, timeout=None):
    options = {}
    if timeout is not None:
        options["timeout"] = timeout

    if capture_output :
        options.update({"stdout": subprocess.PIPE})
        process = subprocess.run([filename], **options)
        return decode_str_bytes(process.stdout)
    else:
        subprocess.run([filename], **options)

