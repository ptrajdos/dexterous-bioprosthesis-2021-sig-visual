ROOTDIR=$(realpath $(dir $(firstword $(MAKEFILE_LIST))))
DATADIR=${ROOTDIR}/data
EXAMPLE_DATAFILE=${DATADIR}/AW_18_06_2024_EMG.zip
VENV_SUBDIR=${ROOTDIR}/venv
CVENV_SUBDIR=${ROOTDIR}/cvenv
CODE_DIR=${ROOTDIR}/dexterous_bioprosthesis_sig_visual
APP_FILE=${CODE_DIR}/vis_app.py
COMPILE_FILE=${CODE_DIR}/compile_app.py
COMPILED_DIR=${ROOTDIR}/compiled_app
INSTALL_LOG_FILE=${ROOTDIR}/install.log

VENV_OPTIONS=

PYTHON=python
SYSPYTHON=python
PIP=pip
UNZIP=unzip

PYTHON_VERSION=3.9.7

ifeq ($(OS),Windows_NT)
	ACTIVATE:=. ${VENV_SUBDIR}/Scripts/activate
else
	ACTIVATE:=. ${VENV_SUBDIR}/bin/activate
endif

.PHONY: all clean build

create_env: pypackages unpack_data

clean: clean_pypackages clean_venv clean_compiled clean_conda
	@echo "Cleaning up build artifacts, virtual environments, and test logs..."

clean_pypackages:
	rm -rf pypackages

clean_venv:
	rm -rf ${VENV_SUBDIR}

clean_compiled:
	rm -rf ${COMPILED_DIR}

clean_conda:
	rm -rf ${CVENV_SUBDIR}

venv:
	${SYSPYTHON} -m venv --upgrade-deps ${VENV_OPTIONS} ${VENV_SUBDIR}
	${ACTIVATE}; ${PYTHON} -m ${PIP} install wheel setuptools pypackages

pypackages: venv
	${ACTIVATE}; ${PYTHON} -m ${PIP} install -e ${ROOTDIR}[dev] --prefer-binary --log ${INSTALL_LOG_FILE}
	touch $@

create_conda:
	conda create --prefix ${CVENV_SUBDIR} python==${PYTHON_VERSION} -y
	conda activate ${CVENV_SUBDIR}; conda install tk -y; ${PIP} install -e ${ROOTDIR}

unpack_data:
	${UNZIP} ${EXAMPLE_DATAFILE} -d ${DATADIR}

run: pypackages
	${ACTIVATE}; ${PYTHON} ${APP_FILE}

build: pypackages
	${ACTIVATE}; ${PYTHON} ${COMPILE_FILE} build