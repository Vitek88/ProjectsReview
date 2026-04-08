import sys

# Patch to prevent CustomTkinter from crashing when sys.stderr is None (PyInstaller case)
if sys.stderr is None:
    class _Dummy:
        def write(self, *args, **kwargs):
            pass
        def flush(self):
            pass

    sys.stderr = _Dummy()
