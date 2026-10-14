# Installation Guide

This document provides instructions for setting up the
**Toy Car Detection** development environment.

## 1. Prerequisites

Before installing the project, ensure that you have the following:

- Git
- Python 3.12 (managed by uv)
- uv (Python package and project manager)
- A USB webcam or built-in camera
- (Optional) RC toy car

### Supported Operating Systems

- macOS
- Windows 10
- Linux (tested on Debian 13)

## 2. Install uv

This project uses [uv](https://docs.astral.sh/uv/) for Python
version management, dependency management, and virtual environments.

### macOS and Linux

Install uv using the
[official installation script](https://docs.astral.sh/uv/getting-started/installation/):

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Alternatively, macOS users can install uv using Homebrew:

```bash
brew install uv
```

### Windows

Open PowerShell and run:

```powershell
irm https://astral.sh/uv/install.ps1 | iex
```

### Verify Installation

Verify that uv is installed successfully:

```bash
uv --version
```

## 3. Clone the Repository

Clone the project from GitHub:

```bash
git clone https://github.com/thanaphoj-h/toycar-detection.git
```

Navigate to the project directory:

```bash
cd toycar-detection
```

## 4. Install Python

This project uses Python 3.12.

Install the required Python version using uv:

```bash
uv python install 3.12
```

Verify the Python installation:

```bash
uv python list
```

The project's Python version is specified in `.python-version`.

## 5. Install Dependencies

Synchronize the project environment:

```bash
uv sync
```

This command automatically:

1. Creates a virtual environment (`.venv`) if necessary.
2. Resolves the required Python version.
3. Installs the project dependencies.
4. Synchronizes dependencies using `uv.lock`.

The project dependencies are defined in `pyproject.toml`.

## 6. Run the Application

Start the application:

```bash
uv run python main.py
```

Ensure that the webcam is connected and accessible.

## References

- [uv Documentation](https://docs.astral.sh/uv/)
- [uv Installation Guide](https://docs.astral.sh/uv/getting-started/installation/)
- [Python Documentation](https://docs.python.org/3.12/)
- [OpenCV Documentation](https://docs.opencv.org/)
- [Matplotlib Documentation](https://matplotlib.org/stable/)
