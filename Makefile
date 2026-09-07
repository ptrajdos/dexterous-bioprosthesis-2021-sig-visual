ROOTDIR=$(realpath $(dir $(firstword $(MAKEFILE_LIST))))
DATADIR=${ROOTDIR}/data
SRCDIR=${ROOTDIR}/dexterous_bioprosthesis_sig_visual
EXAMPLE_DATAFILE=${DATADIR}/AW_18_06_2024_EMG.zip
VENV_SUBDIR=${ROOTDIR}/venv
CVENV_SUBDIR=${ROOTDIR}/cvenv
CODE_DIR=${ROOTDIR}/dexterous_bioprosthesis_sig_visual
APP_FILE=${CODE_DIR}/vis_app.py
COMPILE_FILE=${CODE_DIR}/compile_app.py
COMPILED_DIR=${ROOTDIR}/compiled_app
INSTALL_LOG_FILE=${ROOTDIR}/install.log
DOCS_DIR=${ROOTDIR}/docs
UML_DIR=${ROOTDIR}/docs/uml
DOCZIP=${ROOTDIR}/dexterous_bioprosthesis_sig_visual_docs.zip
SPHINX_DIR=${ROOTDIR}/docs/sphinx
SPHINX_BUILD_DIR=${SPHINX_DIR}/_build
DOCPDF=${ROOTDIR}/dexterous_bioprosthesis_sig_visual_docs.pdf

VENV_OPTIONS=

PYTHON=python
SYSPYTHON=python
PIP=pip
UNZIP=unzip
PDOC=pdoc3
PYLINT= pylint
DOT=dot
PYREVERSE=pyreverse
SPHINX_APIDOC=sphinx-apidoc
SPHINX_BUILD=sphinx-build

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

docs: pypackages uml
	${ACTIVATE}; $(PDOC) --force --html ${SRCDIR} --output-dir ${DOCS_DIR}

uml: pypackages
	@echo "Generating UML diagrams..."
	@rm -rf "$(UML_DIR)"
	@mkdir -p "$(UML_DIR)"

	@${ACTIVATE}; find "$(SRCDIR)" -type f -name '__init__.py' | \
	while read -r init; do \
		pkg="$$(dirname "$$init")"; \
		rel="$${pkg#$(SRCDIR)}"; \
		rel="$${rel#/}"; \
		name="$$(basename "$$pkg")"; \
		outdir="$(UML_DIR)/$$rel"; \
		tmpdir="$$(mktemp -d)"; \
		mkdir -p "$$outdir"; \
		echo "  $$pkg"; \
		\
		$(PYREVERSE) \
			-o dot \
			-p "$$name" \
			-d "$$tmpdir" \
			"$$pkg"; \
		\
		if [ -f "$$tmpdir/classes_$$name.dot" ]; then \
			$(DOT) \
				-Tsvg \
				$(DOT_OPTS) \
				"$$tmpdir/classes_$$name.dot" \
				-o "$$outdir/classes.svg"; \
		fi; \
		\
		if [ -f "$$tmpdir/packages_$$name.dot" ]; then \
			$(DOT) \
				-Tsvg \
				$(DOT_OPTS) \
				"$$tmpdir/packages_$$name.dot" \
				-o "$$outdir/packages.svg"; \
		fi; \
		\
		rm -rf "$$tmpdir"; \
	done


docs-pdf: pypackages uml
	@echo "Generating Sphinx PDF documentation..."
	@rm -rf "$(SPHINX_DIR)"
	@mkdir -p "$(SPHINX_DIR)"
	${ACTIVATE}; $(SPHINX_APIDOC) -f -o "$(SPHINX_DIR)" "$(SRCDIR)"
	@printf '%s\n' \
		'dexterous_bioprosthesis_sig_visual' \
		'======================================' \
		'' \
		'.. toctree::' \
		'   :maxdepth: 4' \
		'' \
		'   modules' \
		'   uml_diagrams' \
		> "$(SPHINX_DIR)/index.rst"
	@printf '%s\n' \
		'UML Diagrams' \
		'============' \
		'' \
		> "$(SPHINX_DIR)/uml_diagrams.rst"
	@mkdir -p "$(SPHINX_DIR)/_uml_images"
	@if [ -d "$(UML_DIR)" ]; then \
		find "$(UML_DIR)" -name '*.svg' | sort | while read -r svg; do \
			base="$$(basename $$svg .svg)"; \
			dir="$$(basename $$(dirname $$svg))"; \
			svgname="$${dir}_$${base}.svg"; \
			cp "$$svg" "$(SPHINX_DIR)/_uml_images/$$svgname"; \
			printf '%s\n' "$$dir / $$base" '--------------------------------------' '' ".. image:: _uml_images/$$svgname" '' >> "$(SPHINX_DIR)/uml_diagrams.rst"; \
		done; \
	fi
	@echo 'import os, sys' > "$(SPHINX_DIR)/conf.py"
	@echo 'sys.path.insert(0, os.path.abspath("$(ROOTDIR)"))' >> "$(SPHINX_DIR)/conf.py"
	@echo 'project = "dexterous_bioprosthesis_sig_visual"' >> "$(SPHINX_DIR)/conf.py"
	@echo 'author = "Paweł Trajdos"' >> "$(SPHINX_DIR)/conf.py"
	@echo 'extensions = ["sphinx.ext.autodoc", "sphinx.ext.napoleon", "sphinx.ext.imgconverter"]' >> "$(SPHINX_DIR)/conf.py"
	@echo 'master_doc = "index"' >> "$(SPHINX_DIR)/conf.py"
	@echo 'latex_engine = "pdflatex"' >> "$(SPHINX_DIR)/conf.py"
	${ACTIVATE}; $(SPHINX_BUILD) -b latex "$(SPHINX_DIR)" "$(SPHINX_BUILD_DIR)/latex"
	$(MAKE) -C "$(SPHINX_BUILD_DIR)/latex" all-pdf
	@cp "$(SPHINX_BUILD_DIR)/latex/dexterous_bioprosthesis_sig_visual.pdf" "$(DOCPDF)"
	@echo "PDF documentation generated: $(DOCPDF)"

docs-zip: docs
	@echo "Creating documentation zip file..."
	@rm -f "$(DOCZIP)"
	@cd "$(DOCS_DIR)" && zip -r "$(DOCZIP)" ./*