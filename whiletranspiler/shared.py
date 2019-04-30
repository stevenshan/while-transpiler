"""
Shared classes used between different steps in lexer and parser
"""

class TokenMetadata:
    """
    Holds meta data for each token such as line number and character number
    """

    line_range = None
    char_range = None

    @staticmethod
    def initialized(obj):
        return obj.line_range is not None and obj.char_range is not None

    def set_metadata(self, objects):
        """
        Sets the metadata to merge of metadata of all objects in `objects`
        """

        objects = list(filter(self.initialized, objects))

        if len(objects) == 0:
            return

        line_min = min(objects, key=lambda x: x.line_range[0]).line_range[0]
        line_max = max(objects, key=lambda x: x.line_range[1]).line_range[1]
        self.line_range = (line_min, line_max)

        char_min = min(objects, key=lambda x: x.char_range[0]).char_range[0]
        char_max = max(objects, key=lambda x: x.char_range[1]).char_range[1]
        self.char_range = (char_min, char_max)

    def merge_metadata(self, objects):
        objects = list(objects)
        if not self.initialized(self):
            self.set_metadata(objects)
        else:
            self.set_metadata((
                (objects[i] if i < len(objects) else self)
                for i in range(len(objects) + 1)))
