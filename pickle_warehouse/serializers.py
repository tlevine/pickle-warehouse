import io
import base64 as _base64

class base64:
    'Dump and load base64-encoded stuff.'
    @staticmethod
    def dump(obj, fp):
        input_fp = io.BytesIO(obj)
        base64.encode(input_fp, fp)
    @staticmethod
    def load(fp):
        output_fp = io.BytesIO()
        base64.decode(fp, output_fp)
        return output_fp.read()

class identity:
    'Dump and load things that are already serialized.'
    @staticmethod
    def dump(obj, fp):
        fp.write(obj)
    @staticmethod
    def load(fp):
        return fp.read()

class meta_xml:
    def __init__(self, lxml_module):
        self.module = lxml_module
    @staticmethod
    def dump(obj, fp):
        fp.write(self.module.tostring(obj))
    @staticmethod
    def load(fp):
        return self.module.fromstring(fp.read())
