ROOTDIR=$(realpath $(dir $(firstword $(MAKEFILE_LIST))))
DATADIR=${ROOTDIR}/data
EXAMPLE_DATAFILE=${DATADIR}/AW_18_06_2024_EMG.zip
VENV_SUBDIR=${ROOTDIR}/venv
CODE_DIR=${ROOTDIR}/dexterous_bioprosthesis_sig_visual

PYTHON=python
PIP=pip
UNZIP=unzip

.PHONY: all clean

create_env: create_venv unpack_data

clean:
	rm -rf ${VENV_SUBDIR}

create_venv:
	${PYTHON} -m venv ${VENV_SUBDIR}
	. ${VENV_SUBDIR}/bin/activate; ${PIP} install -e .

unpack_data:
	${UNZIP} ${EXAMPLE_DATAFILE} -d ${DATADIR}

