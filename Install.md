# Install the Python code

## System requirements

    sudo apt install cpufrequtils

## Install uv

[uv](https://docs.astral.sh/uv/) is used for Python package and project management.

Install uv:

    curl -LsSf https://astral.sh/uv/install.sh | sh

Or on macOS with Homebrew:

    brew install uv

## Install Python dependencies

uv will automatically create a virtual environment in `.venv` and install all dependencies defined in `pyproject.toml`.

    uv sync

This installs all dependencies including [RGBMatrixEmulator](https://github.com/ty-porter/RGBMatrixEmulator) for laptop/emulator mode.

### Running commands with uv

Use `uv run` to execute commands within the virtual environment:

    uv run matrix              # Run the matrix CLI
    uv run python -m Matrix.driver.executor -l   # List commands

Or activate the virtual environment manually:

    source .venv/bin/activate
    matrix                     # Run the matrix CLI
    python -m Matrix.driver.executor -l

### Development tools

Install dev tools like ruff for linting:

    uv tool install ruff

Run linting:

    ruff check --fix Matrix/
    ruff format Matrix

### Installing rpi-rgb-led-matrix on the target system (Raspberry Pi)

On the target system, you want to run the code against the real [rpi-rgb-led-matrix](https://github.com/hzeller/rpi-rgb-led-matrix) lib.

See https://github.com/hzeller/rpi-rgb-led-matrix to install on the target system.

You can either install `rgbmatrix` in the `.venv` or globally to the system.

If `rgbmatrix` is installed in the "global python" you still need to make it available inside the `.venv`.

One approach is:

    cp -R /usr/local/lib/python3.12/dist-packages/rgbmatrix-0.0.1-py3.12-linux-aarch64.egg/rgbmatrix .venv/lib/python3.12/site-packages/.

#### snd_bcm2835

As explained in the documentation, the `rgbmatrix` will not be able to access the hardware if the `snd_bcm2835` module is loaded.

Depending on the underlying distro, editing the `/boot/config.txt` or `/boot/firmware/config.txt` and adding `dtparam=audio=off` may not work as expected.

Better safe than sorry:

    echo "blacklist snd_bcm2835" > /tmp/snd2-blacklist.conf 
    
    sudo cp /tmp/snd2-blacklist.conf /etc/modprobe.d/.

# React App

Be sure npm is installed.

    cd pixel-pulse-neo-client

    npm install

    npm run build

# Add startup scripts

See [system/ReadMe.md](system/ReadMe.md)
