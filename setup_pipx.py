import sys

if sys.version_info[:2] < (3, 8):
    print("::error file=setup-pipx.py,line=4::Python>=3.8 is required, please check 'python-version' input")
    exit(1)

import os
import subprocess
import tempfile

from pathlib import Path


def python(*args, **kwargs):
    kwargs.setdefault("check", True)
    kwargs.setdefault("stderr", subprocess.STDOUT)
    subprocess.run([sys.executable, "-sSE", *args], **kwargs)


def shim(pipx_home, pipx_bin_dir, pipx_man_dir, pipx_path):
    return f"""#!python -sSE

import os
import sys


env = os.environ.copy()
env["PIPX_HOME"] = r"{pipx_home}"
env["PIPX_MAN_DIR"] = r"{pipx_man_dir}"
env["PIPX_BIN_DIR"] = r"{pipx_bin_dir}"
args = [sys.executable, "-sSE", r"{pipx_path}", *sys.argv[1:]]
if sys.platform != "win32":
    os.execve(sys.executable, args, env)
else:
    import subprocess
    process = subprocess.run(args, env=env)
    sys.exit(process.returncode)
"""


def setup_pipx(args):
    assert len(args) == 3, "invalid number of arguments"
    add_pipx_bin_dir_to_path = {"true": True, "false": False}[args[0]]
    add_pipx_to_path = {"true": True, "false": False}[args[1]]
    here = Path(__file__).parent.resolve(strict=True)
    temp_path = Path(args[2]).resolve()
    assert temp_path.parent.is_dir()
    pipx_bin = temp_path / "pipx"
    pipx_bin_dir = temp_path / "bin"
    if not temp_path.is_dir():
        print("::group::Install pipx wrapper")
        temp_path.mkdir()
        pipx_path = here / "pipx.pyz"
        env = os.environ.copy()
        pipx_home = temp_path / "home"
        pipx_man_dir = temp_path / "man"
        env["PIPX_HOME"] = str(pipx_home)
        env["PIPX_BIN_DIR"] = str(pipx_bin)
        env["PIPX_MAN_DIR"] = str(pipx_man_dir)
        env["PIPX_DEFAULT_PYTHON"] = sys.executable
        with tempfile.TemporaryDirectory() as temp_script_dir:
            script_path = Path(temp_script_dir).joinpath("pipx")
            script_path.write_text(
                shim(pipx_home, pipx_bin_dir, pipx_man_dir, pipx_path)
            )
            python(pipx_path, "run", "--path", here / "install_pipx_wrapper.py", temp_script_dir, pipx_bin, sys.executable, env=env)
        print("::endgroup::")
    pipx_path = [file for file in pipx_bin.glob("pipx*") if file.stem == "pipx"]
    assert len(pipx_path) == 1
    print(f"pipx wrapper installed at: '{pipx_path[0]}'")
    with Path(os.environ["GITHUB_OUTPUT"]).open("at") as output:
        output.write(f"pipx-path={pipx_path[0]}\n")
        output.write(f"pipx-bin-dir={pipx_bin_dir}\n")
    if add_pipx_to_path or add_pipx_bin_dir_to_path:
        with Path(os.environ["GITHUB_PATH"]).open("at") as path:
            if add_pipx_to_path:
                print(f"Adding '{pipx_bin}' to PATH")
                path.write(f"{pipx_bin}\n")
            if add_pipx_bin_dir_to_path:
                print(f"Adding '{pipx_bin_dir}' to PATH")
                path.write(f"{pipx_bin_dir}\n")


def main():
    try:
        setup_pipx(sys.argv[1:])
    except Exception as e:
        print(f"::error file=setup-pipx.py::{e}")
        exit(1)


if __name__ == "__main__":
    main()
