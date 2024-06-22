ROOTDIR=$(realpath $(dir $(firstword $(MAKEFILE_LIST))))
DATADIR=${ROOTDIR}/data
EXAMPLE_DATAFILE=${DATADIR}/AW_18_06_2024_EMG.zip
VENV_SUBDIR=${ROOTDIR}/venv
CVENV_SUBDIR=${ROOTDIR}/cvenv
CODE_DIR=${ROOTDIR}/dexterous_bioprosthesis_sig_visual
APP_FILE=${CODE_DIR}/vis_app.py
COMPILE_FILE=${CODE_DIR}/compile_app.py
REQ_FILE=${ROOTDIR}/requirements_dev.txt
COMPILED_DIR=${ROOTDIR}/compiled_app

PYTHON=python
PIP=pip
UNZIP=unzip

ifeq ($(OS),Windows_NT)
	ACTIVATE:=. ${VENV_SUBDIR}/Scripts/activate
else
	ACTIVATE:=. ${VENV_SUBDIR}/bin/activate
endif

.PHONY: all clean build

create_env: venv unpack_data

clean:
	rm -rf ${VENV_SUBDIR} ${COMPILED_DIR}

venv:
	${PYTHON} -m venv ${VENV_SUBDIR}
	${ACTIVATE}; ${PIP} install -e ${ROOTDIR}; ${PIP} install -r ${REQ_FILE}

create_conda:
	conda create --prefix ${CVENV_SUBDIR} python==3.9.7 -y
	conda activate ${CVENV_SUBDIR}; conda install tk -y; ${PIP} install -e ${ROOTDIR}

unpack_data:
	${UNZIP} ${EXAMPLE_DATAFILE} -d ${DATADIR}

run:
	${ACTIVATE}; ${PYTHON} ${APP_FILE}

build:
	${ACTIVATE}; ${PYTHON} ${COMPILE_FILE} build