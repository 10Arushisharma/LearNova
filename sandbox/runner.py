"""Isolated sandbox entrypoint executed inside a constrained Docker container or isolated subprocess."""
import ast
import io
import json
import sys
import time
import traceback
from contextlib import redirect_stdout, redirect_stderr

MAX_OUTPUT_CHARS = 16000
BLOCKED_MODULES = {
    "os",
    "subprocess",
    "socket",
    "shutil",
    "ctypes",
    "multiprocessing",
    "threading",
    "http",
    "urllib",
    "requests",
    "httpx",
    "ftplib",
    "smtplib",
    "telnetlib",
    "pathlib",
    "importlib",
    "sys",
    "pty",
    "fcntl",
    "resource",
    "signal",
    "webbrowser",
}

BLOCKED_BUILTINS = {"eval", "exec", "compile", "__import__", "open", "breakpoint", "input"}


def validate_ast(source: str) -> str | None:
    try:
        tree = ast.parse(source, mode="exec")
    except SyntaxError as exc:
        return f"SyntaxError: {exc.msg} (line {exc.lineno})"

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                root = alias.name.split(".")[0]
                if root in BLOCKED_MODULES:
                    return f"SecurityError: Import of '{root}' is restricted in the Learnova sandbox."
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                root = node.module.split(".")[0]
                if root in BLOCKED_MODULES:
                    return f"SecurityError: Import from '{root}' is restricted in the Learnova sandbox."
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id in BLOCKED_BUILTINS and node.func.id != "input":
                return f"SecurityError: Built-in '{node.func.id}' is restricted in the sandbox."
        elif isinstance(node, ast.Attribute) and node.attr.startswith("__"):
            if node.attr not in {"__init__", "__str__", "__repr__", "__len__", "__getitem__", "__iter__", "__next__", "__name__"}:
                return f"SecurityError: Access to dunder attribute '{node.attr}' is restricted."
    return None


def safe_import(name, globals=None, locals=None, fromlist=(), level=0):
    root = name.split(".")[0]
    if root in BLOCKED_MODULES:
        raise ImportError(f"Module '{root}' is restricted in the Learnova sandbox.")
    return __import__(name, globals, locals, fromlist, level)


def main() -> None:
    raw = sys.stdin.read()
    try:
        payload = json.loads(raw)
    except Exception:
        print(json.dumps({"success": False, "stdout": "", "stderr": "Invalid sandbox payload", "execution_time_ms": 0}))
        return

    code = payload.get("code", "")
    stdin_text = payload.get("stdin", "") or ""
    stdin_lines = stdin_text.splitlines()
    stdin_idx = 0

    err = validate_ast(code)
    if err:
        print(json.dumps({"success": False, "stdout": "", "stderr": err, "execution_time_ms": 0}))
        return

    def safe_input(prompt: str = "") -> str:
        nonlocal stdin_idx
        if prompt:
            sys.stdout.write(str(prompt))
        if stdin_idx < len(stdin_lines):
            val = stdin_lines[stdin_idx]
            stdin_idx += 1
            return val
        return ""

    safe_builtins = {
        "abs": abs,
        "all": all,
        "any": any,
        "bin": bin,
        "bool": bool,
        "chr": chr,
        "dict": dict,
        "divmod": divmod,
        "enumerate": enumerate,
        "filter": filter,
        "float": float,
        "format": format,
        "frozenset": frozenset,
        "getattr": getattr,
        "hasattr": hasattr,
        "hash": hash,
        "hex": hex,
        "id": id,
        "input": safe_input,
        "int": int,
        "isinstance": isinstance,
        "issubclass": issubclass,
        "iter": iter,
        "len": len,
        "list": list,
        "map": map,
        "max": max,
        "min": min,
        "next": next,
        "object": object,
        "oct": oct,
        "ord": ord,
        "pow": pow,
        "print": print,
        "range": range,
        "repr": repr,
        "reversed": reversed,
        "round": round,
        "set": set,
        "slice": slice,
        "sorted": sorted,
        "str": str,
        "sum": sum,
        "tuple": tuple,
        "type": type,
        "zip": zip,
        "Exception": Exception,
        "ValueError": ValueError,
        "TypeError": TypeError,
        "KeyError": KeyError,
        "IndexError": IndexError,
        "ZeroDivisionError": ZeroDivisionError,
        "AssertionError": AssertionError,
        "StopIteration": StopIteration,
        "__build_class__": __build_class__,
        "__import__": safe_import,
    }

    namespace = {"__builtins__": safe_builtins, "__name__": "__main__"}
    stdout_buf = io.StringIO()
    stderr_buf = io.StringIO()

    start = time.perf_counter()
    success = True
    try:
        compiled = compile(code, "<learnova_playground>", "exec")
        with redirect_stdout(stdout_buf), redirect_stderr(stderr_buf):
            exec(compiled, namespace, namespace)
    except Exception:
        success = False
        tb_lines = traceback.format_exc().splitlines()
        cleaned = [line for line in tb_lines if "/opt/runner.py" not in line and "runner.py" not in line]
        stderr_buf.write("\n".join(cleaned) if cleaned else traceback.format_exc())
    elapsed_ms = round((time.perf_counter() - start) * 1000, 2)

    out_str = stdout_buf.getvalue()[:MAX_OUTPUT_CHARS]
    err_str = stderr_buf.getvalue()[:MAX_OUTPUT_CHARS]
    print(
        json.dumps(
            {
                "success": success and not err_str,
                "stdout": out_str,
                "stderr": err_str,
                "execution_time_ms": elapsed_ms,
            }
        )
    )


if __name__ == "__main__":
    main()
