import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any
from app.core.config import settings

SANDBOX_RUNNER_PATH = Path(__file__).resolve().parents[3] / "sandbox" / "runner.py"


def execute_python_sandbox(code: str, stdin: str = "") -> dict[str, Any]:
    """
    Execute Python code in an isolated sandbox.
    - Never uses eval/exec inside the FastAPI process.
    - When SANDBOX_MODE == "docker", launches an ephemeral non-root container with --network=none,
      --read-only, memory/CPU/PID limits.
    - When SANDBOX_MODE == "subprocess" (local dev without Docker daemon), spawns an isolated Python
      subprocess running sandbox/runner.py with a stripped environment and strict wall-clock timeout.
    """
    payload = json.dumps({"code": code, "stdin": stdin})
    timeout = max(1, min(15, settings.SANDBOX_TIMEOUT_SECONDS))

    if settings.SANDBOX_MODE == "docker":
        cmd = [
            "docker",
            "run",
            "--rm",
            "-i",
            "--network=none",
            "--read-only",
            "--pids-limit=64",
            f"--memory={settings.SANDBOX_MEMORY_LIMIT}",
            f"--cpus={settings.SANDBOX_CPU_LIMIT}",
            "--security-opt=no-new-privileges",
            "--cap-drop=ALL",
            settings.SANDBOX_IMAGE,
        ]
        try:
            proc = subprocess.run(
                cmd,
                input=payload,
                capture_output=True,
                text=True,
                timeout=timeout + 2,
            )
            return _parse_runner_output(proc, "docker")
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "stdout": "",
                "stderr": f"TimeoutError: Execution exceeded the {timeout}s container limit.",
                "execution_time_ms": timeout * 1000.0,
                "sandbox_mode": "docker",
            }
        except FileNotFoundError:
            return {
                "success": False,
                "stdout": "",
                "stderr": "SandboxError: Docker binary is unavailable on host.",
                "execution_time_ms": 0.0,
                "sandbox_mode": "docker",
            }

    # Subprocess isolated fallback (separate Python process, stripped env, temp cwd)
    runner_path = str(SANDBOX_RUNNER_PATH)
    if not os.path.exists(runner_path):
        return {
            "success": False,
            "stdout": "",
            "stderr": "SandboxError: Isolated runner script not found.",
            "execution_time_ms": 0.0,
            "sandbox_mode": "subprocess",
        }

    minimal_env = {
        "PATH": os.environ.get("PATH", ""),
        "SYSTEMROOT": os.environ.get("SYSTEMROOT", ""),
        "PYTHONIOENCODING": "utf-8",
        "PYTHONDONTWRITEBYTECODE": "1",
    }
    try:
        with tempfile.TemporaryDirectory(prefix="learnova_sb_") as tmpdir:
            proc = subprocess.run(
                [sys.executable, "-I", runner_path],
                input=payload,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=tmpdir,
                env=minimal_env,
            )
            return _parse_runner_output(proc, "subprocess")
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "stdout": "",
            "stderr": f"TimeoutError: Execution exceeded the {timeout}s limit.",
            "execution_time_ms": timeout * 1000.0,
            "sandbox_mode": "subprocess",
        }


def _parse_runner_output(proc: subprocess.CompletedProcess[str], mode: str) -> dict[str, Any]:
    raw_out = (proc.stdout or "").strip()
    if raw_out:
        try:
            data = json.loads(raw_out.splitlines()[-1])
            data["sandbox_mode"] = mode
            return data
        except json.JSONDecodeError:
            pass
    return {
        "success": False,
        "stdout": raw_out[:4000],
        "stderr": (proc.stderr or "Sandbox execution failed without structured output.")[:4000],
        "execution_time_ms": 0.0,
        "sandbox_mode": mode,
    }


def evaluate_challenge_submission(
    user_code: str, test_cases: list[dict[str, Any]], expected_output: str = ""
) -> dict[str, Any]:
    """Run user code against hidden/visible test cases inside the sandbox."""
    if not test_cases:
        res = execute_python_sandbox(user_code)
        exp = (expected_output or "").strip()
        got = (res.get("stdout") or "").strip()
        passed = bool(res["success"] and (not exp or got == exp))
        return {
            "passed": passed,
            "passed_tests": 1 if passed else 0,
            "total_tests": 1,
            "execution_time_ms": res.get("execution_time_ms", 0.0),
            "details": [
                {
                    "name": "Output verification",
                    "passed": passed,
                    "expected": exp or "(clean exit)",
                    "actual": got or res.get("stderr", ""),
                }
            ],
        }

    # Build a single sandboxed test harness executing user_code + assertions
    harness_lines = [user_code, "", "_learnova_results = []"]
    for idx, tc in enumerate(test_cases):
        assertion = tc.get("assert_expr", "True")
        name = tc.get("name", f"Test {idx + 1}")
        harness_lines.append("try:")
        harness_lines.append(f"    assert {assertion}")
        harness_lines.append(f"    _learnova_results.append({{'name': {name!r}, 'passed': True, 'error': ''}})")
        harness_lines.append("except Exception as _e:")
        harness_lines.append(f"    _learnova_results.append({{'name': {name!r}, 'passed': False, 'error': str(_e) or type(_e).__name__}})")
    harness_lines.append("import json as _lj")
    harness_lines.append("print('__LEARNOVA_TESTS__' + _lj.dumps(_learnova_results))")

    # Note: we allow json internally inside the harness only by importing json before or avoiding import in AST?
    # Wait: sandbox/runner.py allows `import json` (not in BLOCKED_MODULES)! Let's verify: json is safe and allowed.
    res = execute_python_sandbox("\n".join(harness_lines))
    stdout = res.get("stdout", "")
    marker = "__LEARNOVA_TESTS__"
    details = []
    if marker in stdout:
        json_part = stdout.split(marker, 1)[1].strip().splitlines()[0]
        try:
            details = json.loads(json_part)
        except Exception:
            details = []

    if not details:
        details = [
            {
                "name": tc.get("name", f"Test {i+1}"),
                "passed": False,
                "error": res.get("stderr") or "Runtime error before tests completed",
            }
            for i, tc in enumerate(test_cases)
        ]

    passed_count = sum(1 for d in details if d.get("passed"))
    return {
        "passed": passed_count == len(test_cases) and len(test_cases) > 0,
        "passed_tests": passed_count,
        "total_tests": len(test_cases),
        "execution_time_ms": res.get("execution_time_ms", 0.0),
        "stdout": stdout.split(marker)[0].strip(),
        "stderr": res.get("stderr", ""),
        "details": details,
    }
