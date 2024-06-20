ROOTDIR=$(realpath $(dir $(firstword $(MAKEFILE_LIST))))
DATADIR=${ROOTDIR}/data
EXAMPLE_DATAFILE=${DATADIR}/AW_18_06_2024_EMG.zip
VENV_SUBDIR=${ROOTDIR}/venv
CVENV_SUBDIR=${ROOTDIR}/cvenv
CODE_DIR=${ROOTDIR}/dexterous_bioprosthesis_sig_visual
APP_FILE=${CODE_DIR}/vis_app.py
COMPILE_FILE=${CODE_DIR}/compile_app.py
REQ_FILE=${ROOTDIR}/requirements_dev.txt

PYTHON=python
PIP=pip
UNZIP=unzip

.PHONY: all clean build

create_env: create_venv unpack_data

clean:
	rm -rf ${VENV_SUBDIR}

create_venv:
	${PYTHON} -m venv ${VENV_SUBDIR}
	. ${VENV_SUBDIR}/bin/activate; ${PIP} install -e ${ROOTDIR}; ${PIP} install -r ${REQ_FILE}

create_conda:
	conda create --prefix ${CVENV_SUBDIR} python==3.9.7 -y
	conda activate ${CVENV_SUBDIR}; conda install tk -y; ${PIP} install -e ${ROOTDIR}

unpack_data:
	${UNZIP} ${EXAMPLE_DATAFILE} -d ${DATADIR}

run:
	${PYTHON} ${APP_FILE}

build:
	${PYTHON} ${COMPILE_FILE} build