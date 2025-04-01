run:
	./script.sh
	rm r.out
	rm br.out

png:
	xdg-open build_requires.png
	xdg-open runtime_requires.png

graph:
	xdg-open build_requires
	xdg-open runtime_requires

clean:
	rm build_requires
	rm runtime_requires
	rm *.png
	rm *.out

cleanout: 
	rm *.out

cleanpng:
	rm *.png

cleangraph:
	rm build_requires
	rm runtime_requires
