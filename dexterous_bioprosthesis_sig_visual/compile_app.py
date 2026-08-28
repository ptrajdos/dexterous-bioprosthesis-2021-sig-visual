"""Module for compiling the visualization application into a standalone executable.

Uses PyInstaller to package the application as a single-file executable.
"""

import sys

import platform
import os
import shutil
import PyInstaller.__main__


def get_platform_string():
    """Return the current platform identification string."""
    return platform.platform()


def get_root_dir():
    """Return the absolute path to the package root directory."""
    return os.path.dirname(os.path.normpath(__file__))


def get_compile_dir():
    """Return the path to the base compilation output directory."""
    return os.path.join(get_root_dir(), "../", "compiled_app")


def get_compile_dir_system():
    """Return the platform-specific compilation output directory."""
    return os.path.join(get_compile_dir(), get_platform_string())


def get_build_dir():
    """Return the path to the PyInstaller build directory."""
    return os.path.join(get_compile_dir_system(), "build")


def get_dist_dir():
    """Return the path to the PyInstaller distribution directory."""
    return os.path.join(get_compile_dir_system(), "dist")


def get_script_file():
    """Return the path to the main application script to compile."""
    return os.path.join(get_root_dir(), "vis_app.py")


def clean_compile_dir():
    """Remove the platform-specific compilation output directory."""
    dir_to_remove = get_compile_dir_system()
    if os.path.exists(dir_to_remove):
        shutil.rmtree(dir_to_remove)
        print("Directory ", dir_to_remove, " has been deleted.")
    else:
        print("Nothing to clean!")


def get_base_option_list():
    """Return the base list of PyInstaller command-line options."""
    opt_list = [
        "--collect-submodules",
        "sklearn",
        "--hidden-import",
        "PIL._tkinter_finder",
        "--distpath",
        get_dist_dir(),
        "--workpath",
        get_build_dir(),
        "-y",
        "--clean",
        "--onefile",
        "--console",
    ]
    return opt_list


def build():
    """Build the application as a standalone executable."""
    opt_list = get_base_option_list()
    opt_list += [get_script_file()]

    print("Compiling ", get_script_file())

    PyInstaller.__main__.run(opt_list)


def build_debug():
    """Build the application with debug logging and diagnostics enabled."""
    opt_list = get_base_option_list()
    opt_list += ["--log-level", "DEBUG", "--debug", "all"]
    opt_list += [get_script_file()]

    print("Compiling with debugging enabled", get_script_file())

    PyInstaller.__main__.run(opt_list)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        build()
        sys.exit()

    if len(sys.argv) > 1 and sys.argv[1] == "build_debug" or len(sys.argv) == 1:
        build_debug()
        sys.exit()

    if len(sys.argv) > 1 and sys.argv[1] == "clean":
        clean_compile_dir()
        sys.exit()

    print("Pass an option to the script: build, build_debug or clean")
