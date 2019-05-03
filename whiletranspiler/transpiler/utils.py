import os
import sys
import subprocess
from .transpile_c import transpile_parsed

def c_compile(parse_result, output_file):
    """
    Compiles transpiled C source code using gcc.
    """

    rfd, wfd = os.pipe()
    file_obj = os.fdopen(wfd, "w")
    transpile_parsed(parse_result, file_obj)
    file_obj.close()
    gcc_args = ["gcc", "-x", "c", "-o", output_file, "-"]
    process = subprocess.run(gcc_args, stdout=subprocess.PIPE, stdin=rfd)
    return process.returncode


def exec_file(filename, capture_output=False, timeout=None):
    if capture_output :
        options = {"stdout": subprocess.PIPE}
        if timeout is not None:
            options["timeout"] = timeout
        process = subprocess.run([filename], **options)
        return process.stdout.decode("ascii")
    else:
        subprocess.run([filename])

