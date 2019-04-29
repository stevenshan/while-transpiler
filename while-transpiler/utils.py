import os

class FileLikeDescriptor:
    """
    file-like object with read method to make os file descriptor act like file
    """

    def __init__(self, fd):
        self.fd = fd

    def write(self, string):
        os.write(self.fd, string.encode("ascii"))
