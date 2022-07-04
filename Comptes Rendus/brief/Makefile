#Makefile compte rendu brief

CR.pdf: CR.dvi
	dvipdf CR.dvi

CR.dvi:
	latex CR.tex

pdf : CR.tex
	pdflatex $^
	
clean : 
	rm -f *.log *.aux *.dvi *.pdf 
