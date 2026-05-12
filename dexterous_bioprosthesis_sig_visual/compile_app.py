import sys

import platform
import os
import sys
import shutil
import PyInstaller.__main__

"""
	Compiles the feedback application code into standalone app. 
"""


def get_platform_string():
    return platform.platform()


def get_root_dir():
    return os.path.dirname(os.path.normpath(__file__))


def get_compile_dir():
    return os.path.join(get_root_dir(), "../", "compiled_app")


def get_compile_dir_system():
    return os.path.join(get_compile_dir(), get_platform_string())


def get_build_dir():
    return os.path.join(get_compile_dir_system(), "build")


def get_dist_dir():
    return os.path.join(get_compile_dir_system(), "dist")


def get_script_file():
    return os.path.join(get_root_dir(), "vis_app.py")


def clean_compile_dir():
    dir_to_remove = get_compile_dir_system()
    if os.path.exists(dir_to_remove):
        shutil.rmtree(dir_to_remove)
        print("Directory ", dir_to_remove, " has been deleted.")
    else:
        print("Nothing to clean!")


def get_base_option_list():
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

    opt_list = get_base_option_list()
    opt_list += [get_script_file()]

    print("Compiling ", get_script_file())

    PyInstaller.__main__.run(opt_list)


def build_debug():

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
