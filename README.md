# Signal Visualizer

A desktop application for visualizing raw EMG signals collected as part of the Dexterous Bioprosthesis project. Built with Tkinter and Matplotlib.

## Requirements

- Python 3.9+
- Tkinter (included with most Python distributions)

## Installation

### Using a virtual environment (recommended)

```bash
make create_env
```

This will:
1. Create a Python virtual environment in `venv/`.
2. Install all dependencies (including dev tools).
3. Unpack example data from `data/AW_18_06_2024_EMG.zip`.

### Using Conda

```bash
make create_conda
```

### Manual installation

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -e .[dev]
```

## Usage

### Running the application

```bash
make run
```

Or manually:

```bash
source venv/bin/activate   # On Windows: venv\Scripts\activate
python dexterous_bioprosthesis_sig_visual/vis_app.py
```

### Loading data

1. Launch the application.
2. Go to **File → Open Directory** and select a directory containing raw signal data files.
3. Select a signal from the list on the left to display it.
4. Use the channel list to switch between individual channels.

### Keyboard shortcuts

The application supports keyboard navigation for browsing signals and channels. Use the built-in **Help** menu for details.

## Building a standalone executable

The application can be compiled into a standalone executable using PyInstaller:

```bash
make build
```

Or manually:

```bash
python dexterous_bioprosthesis_sig_visual/compile_app.py build
```

The compiled executable will be placed in `compiled_app/<platform>/dist/`.

### Running the compiled application

After building, run the standalone executable directly — no Python installation required:

```bash
# macOS / Linux
./compiled_app/<platform>/dist/vis_app

# Windows
compiled_app\<platform>\dist\vis_app.exe
```

Replace `<platform>` with the platform string of the system used for building (e.g., `macOS-15.5-arm64-arm-64bit`).

Other compile options:

```bash
# Build with debug logging
python dexterous_bioprosthesis_sig_visual/compile_app.py build_debug

# Clean compiled artifacts
python dexterous_bioprosthesis_sig_visual/compile_app.py clean
```


## Cleaning up

```bash
make clean
```

This removes build artifacts, virtual environments, and compiled executables.
