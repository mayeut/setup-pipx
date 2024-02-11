# setup-pipx

[pipx]: https://github.com/pypa/pipx

This action installs [pipx].

While most runners come with [pipx] pre-installed, this is not always the case:
- GitHub-hosted macos-14 runners
- Self-hosted runners

Optional features:
- python version used to install pipx (default: non EOL [pipx] supported Python versions)
- add `pipx` to `PATH` (default: true)
- add `PIPX_BIN_DIR` to `PATH` (default: true)

Limitations:
- `PIPX_HOME`, `PIPX_BIN_DIR` & `PIPX_MAN_DIR` are always overriden in this implementation

When used multiple times, the action does not re-install [pipx] if:
- the action reference is the same (e.g. `@v1`)
- the resolved python version is the same.

## Basic usage

```yaml
steps:
- uses: mayeut/setup-pipx@v1
- run: pipx run pycowsay moooo!
```

## Advanced usage

In composite actions, it might be desirable not to mess-up with the `PATH` variable.

You can do so:

```yaml
steps:
- uses: mayeut/setup-pipx@v1
  id: pipx
  with:
    python-version: "3.10 - 3.12"
    add-pipx-to-path: false
    add-pipx-bin-dir-to-path: false
- run: |
    "${{ steps.pipx.outputs.python-path }}" -V  # you can get the path to the python executable
    "${{ steps.pipx.outputs.pipx-path }}" run pycowsay  # run directly using pipx full-path
```
