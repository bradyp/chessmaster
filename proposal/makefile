PAPER = proposal

default:
	cp $(PAPER).tex $(PAPER).tex.backup #Create backup just in case...
	latex $(PAPER)
	latex $(PAPER)
	dvips -t letter $(PAPER)
	ps2pdf $(PAPER).ps

clean:
	rm -f *.pdf *.log *.blg *.bbl *.aux *.dvi *.toc *.ps *~
