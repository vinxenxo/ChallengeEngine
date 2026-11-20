# Root cause — dataclasses import namespace

The V4 helper used `importlib.util.module_from_spec()` and immediately called `spec.loader.exec_module(module)`. It did not first place `module` in `sys.modules[spec.name]`.

The pinned QImage compositor imports `dataclass` and uses postponed annotations. During dataclass field processing, Python resolves annotation identifiers against the module namespace in `sys.modules`. Because the module entry was absent, dataclasses dereferenced `None.__dict__`, producing the exact V4 exception.

V5 registers the module before `exec_module`; it removes the entry if module execution raises. A regression fixture proves both the original failing sequence and the corrected sequence.
