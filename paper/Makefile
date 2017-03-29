LATEX=pdflatex
MAIN=tsd2017
SOURCES=$(MAIN).tex
FIGURES=
SUBDIRS=tables
BIBTEX=bibtex

.PHONY: subdirs all

all: $(MAIN).pdf

subdirs: 
	for dir in $(SUBDIRS); do  $(MAKE) -j 2 -C $$dir;  done

default:
	python ../results/create_db.py
	python ../results/create_tables.py

$(MAIN).pdf: $(SOURCES) $(FIGURES)
	$(LATEX) $(MAIN)
	test -f $(MAIN).makefile && make -j 2 -f $(MAIN).makefile || echo no $(MAIN).makefile
	$(BIBTEX) $(MAIN)
	$(LATEX) $(MAIN)
	$(LATEX) $(MAIN)

$(MAIN).aux:
	$(LATEX) $(MAIN)

view:
	evince $(MAIN).pdf >/dev/null 2>&1 &

clean:
	rm -f *~ $(MAIN).aux $(MAIN).bbl $(MAIN).blg $(MAIN).log\
		$(MAIN).pdf $(MAIN).snm $(MAIN).toc $(MAIN).nav $(MAIN).out\
		$(MAIN).fdb_latexmk
