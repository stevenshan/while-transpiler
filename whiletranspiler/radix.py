"""
Implementation of radix trie and some wrappers for it
"""

def _common_prefix(s1, s2):
    buff = []
    for c1, c2 in zip(s1, s2):
        if c1 == c2:
            buff.append(c1)
        else:
            break
    return "".join(buff)

class RadixTrie:
    def __init__(self, value = "", terminal = True):
        self.value = value
        self.children = []
        self.terminal = terminal
        self.prefix = ""

    @classmethod
    def from_list(cls, L):
        root = RadixTrie()
        for l in L:
            root.insert(l)
        return root

    @property
    def string(self):
        assert self.terminal
        return self.prefix + self.value

    def __repr__(self):
        if self.terminal:
            return f"<RadixTrie '{self.value}'>"
        else:
            return f"<RadixTrie --'{self.value}'-->"

    def insert(self, string):
        assert isinstance(string, str)
        if len(string) == 0:
            return

        for i, child in enumerate(self.children):
            assert child.value is not None
            if string.startswith(child.value):
                # if string is prefixed by child
                remainder = string[len(child.value):]
                if remainder == "":
                    child.terminal = True
                else:
                    child.insert(remainder)
                return

            if child.value.startswith(string):
                # split child
                shared = RadixTrie(string, True)
                shared.prefix = child.prefix
                child.value = child.value[len(string):]
                child.prefix += string
                shared.children.append(child)
                self.children[i] = shared
                return

            common_prefix = _common_prefix(child.value, string)
            if common_prefix != "":
                shared = RadixTrie(common_prefix, False)
                shared.prefix = child.prefix
                child.value = child.value[len(common_prefix):]
                child.prefix += common_prefix
                string = string[len(common_prefix):]
                new_node = RadixTrie(string, True)
                new_node.prefix = shared.prefix + common_prefix
                shared.children = [child, new_node]
                self.children[i] = shared
                return

        new_node = RadixTrie(string, True)
        self.children.append(new_node)
        new_node.prefix = self.prefix + self.value

class RadixReader:
    """
    takes characters one by one to check if the radix tree contains a prefix
    of it
    """

    def __init__(self, radix_trie):
        self.original = radix_trie
        self.reset()

    def reset(self):
        self.root = self.original
        self.last_match = self.original
        self.buff = ""
        self.unmatched = []

    @classmethod
    def from_list(cls, L):
        return cls(RadixTrie.from_list(L))

    def add(self, string):
        assert isinstance(string, str)
        success = True
        for c in string:
            success &= self._add(c)
        return success

    def _add(self, c):
        if self.buff == self.root.value:
            for child in self.root.children:
                if child.value.startswith(c):
                    self.root = child
                    self.buff = c
                    self.unmatched.append(c)

                    if self.buff == self.root.value and self.root.terminal:
                        self.unmatched = []
                        self.last_match = self.root

                    return True

            return False

        self.buff += c
        self.unmatched.append(c)
        if not self.root.value.startswith(self.buff):
            return False

        if self.buff == self.root.value and self.root.terminal:
            self.unmatched = []
            self.last_match = self.root

        return True

    @property
    def last_string(self):
        return self.last_match.string

