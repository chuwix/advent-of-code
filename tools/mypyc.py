import inspect
import subprocess
from os import path
from pathlib import Path


def ensure_built():
    caller_dir = Path(path.dirname(path.abspath((inspect.stack()[1])[1])))
    # so_here = any(p.suffix in {".so", ".pyd"} for p in caller_dir.glob("main.*"))
    # if so_here:
    #     return
    # DEV-ONLY: rebuild in-place
    subprocess.check_call(["python", "setup.py", "build_ext", "--inplace"], cwd=str(caller_dir))
