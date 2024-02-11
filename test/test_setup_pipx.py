import os
import subprocess

import pytest

from setup_pipx import main, setup_pipx


@pytest.fixture()
def github_output(tmp_path, monkeypatch):
    result = tmp_path / "GITHUB_OUTPUT"
    monkeypatch.setenv("GITHUB_OUTPUT", str(result))
    yield result


@pytest.fixture()
def github_path(tmp_path, monkeypatch):
    result = tmp_path / "GITHUB_PATH"
    monkeypatch.setenv("GITHUB_PATH", str(result))
    yield result


def test_missing_args(github_output, github_path):
    with pytest.raises(AssertionError, match='invalid number of arguments'):
        setup_pipx([])


@pytest.mark.parametrize("add_pipx_to_path", ["true", "false"])
@pytest.mark.parametrize("add_pipx_bin_dir_to_path", ["true", "false"])
def test_valid(tmp_path, github_output, github_path, add_pipx_to_path, add_pipx_bin_dir_to_path, monkeypatch):
    path = tmp_path.joinpath("pipx").resolve()
    setup_pipx([add_pipx_bin_dir_to_path, add_pipx_to_path, path])

    pipx = next(path.glob("pipx/pipx*"))
    output = subprocess.run([pipx, "--version"], check=True, capture_output=True, text=True).stdout
    assert output.strip() == "1.4.3"

    assert github_output.exists()
    output_lines = github_output.read_text().splitlines()
    assert len(output_lines) == 2, output_lines
    assert any(line.startswith("pipx-path=") for line in output_lines), output_lines
    assert any(line.startswith("pipx-bin-dir=") for line in output_lines), output_lines

    path_lines = [] if not github_path.exists() else github_path.read_text().splitlines()
    expected_path_count = sum(1 if value == "true" else 0 for value in (add_pipx_to_path, add_pipx_bin_dir_to_path))
    assert len(path_lines) == expected_path_count, path_lines
    if add_pipx_to_path == "true":
        assert any(line.startswith(str(path / "pipx")) for line in path_lines), path_lines
    if add_pipx_bin_dir_to_path == "true":
        assert any(line.startswith(str(path / "bin")) for line in path_lines), path_lines


def test_invalid_bool1(tmp_path, github_output, github_path):
    with pytest.raises(KeyError):
        setup_pipx(["fals", "false", tmp_path / "pipx"])


def test_invalid_bool2(tmp_path, github_output, github_path):
    with pytest.raises(KeyError):
        setup_pipx(["false", "fals", tmp_path / "pipx"])


def test_invalid_path(tmp_path, github_output, github_path):
    with pytest.raises(AssertionError):
        setup_pipx(["false", "false", tmp_path / "pipx" / "pipx"])
