from textwrap import dedent

def format_assembly_string(func):
    def inner(*args, **kwargs):
        assembly_string, labels = func(*args, **kwargs)
        assembly = dedent(assembly_string)
        return assembly.format(**labels)
    return inner