run:
	./script.sh
	rm r.out
	rm br.out

clean:
	# rm *.out
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
