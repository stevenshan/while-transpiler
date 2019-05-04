import os
import sys

class StdoutCapture:
    def __init__(self):
        self.out = ""

    def __enter__(self):
        self.rfd, self.wfd = os.pipe()
        self.orig_stdout = os.dup(sys.stdout.fileno())
        os.dup2(self.wfd, sys.stdout.fileno())

    def __exit__(self, type, value, traceback):
        sys.stdout.flush()
        os.dup2(self.orig_stdout, sys.stdout.fileno())

        os.close(self.wfd)
        r = os.fdopen(self.rfd)
        self.out = r.read()
        r.close()


