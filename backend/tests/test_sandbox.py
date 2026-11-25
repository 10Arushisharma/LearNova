"""Sandbox security and execution tests."""
import json
from app.services.sandbox import execute_python_sandbox, evaluate_challenge_submission


def test_basic_execution():
    result = execute_python_sandbox("print('hello')")
    assert result["stdout"].strip() == "hello"
    assert result["success"] is True


def test_blocked_import_os():
    result = execute_python_sandbox("import os\nos.system('echo hacked')")
    assert result["success"] is False
    assert "SecurityError" in result["stderr"] or "restricted" in result["stderr"].lower()


def test_blocked_import_subprocess():
    result = execute_python_sandbox("import subprocess; subprocess.run(['ls'])")
    assert result["success"] is False


def test_blocked_socket():
    result = execute_python_sandbox("import socket")
    assert result["success"] is False


def test_blocked_eval():
    result = execute_python_sandbox("eval('__import__(\"os\")')")
    assert result["success"] is False or "restricted" in result.get("stderr", "").lower()


def test_math_works():
    result = execute_python_sandbox("print(2 ** 10)")
    assert result["stdout"].strip() == "1024"


def test_numpy_allowed():
    result = execute_python_sandbox("import numpy as np\nprint(np.array([1,2,3]).sum())")
    assert result["stdout"].strip() == "6"


def test_syntax_error():
    result = execute_python_sandbox("def broken(\nprint('oops')")
    assert result["success"] is False
    assert "SyntaxError" in result["stderr"]


def test_runtime_error():
    result = execute_python_sandbox("x = 1 / 0")
    assert result["success"] is False
    assert "ZeroDivisionError" in result["stderr"]


def test_challenge_evaluation_pass():
    res = evaluate_challenge_submission(
        "def add(a, b): return a + b",
        [{"name": "add test", "assert_expr": "add(2, 3) == 5"}],
    )
    assert res["passed"] is True
    assert res["passed_tests"] == 1


def test_challenge_evaluation_fail():
    res = evaluate_challenge_submission(
        "def add(a, b): return a - b",
        [{"name": "add test", "assert_expr": "add(2, 3) == 5"}],
    )
    assert res["passed"] is False


def test_no_network_access():
    result = execute_python_sandbox("import urllib.request; urllib.request.urlopen('http://google.com')")
    assert result["success"] is False
