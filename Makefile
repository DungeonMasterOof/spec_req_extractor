run:
	./script.sh

clean:
	rm *.out
	rm build_requires
	rm runtime_requires
	rm *.png

cleanout: 
	rm *.out

cleanpng:
	rm *.png

cleangraph:
	rm build_requires
	rm runtime_requires
