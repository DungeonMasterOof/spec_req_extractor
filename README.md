## Spec data extractor
The program has multiple modules. The main goal is to extract requirements and build requirements fields from a spec file or a set of spec files (in one directory). There is a Makefile to make working with modules simpler. For now, there are:
`Makefile, script.sh, task.py`  
Their work is described below.

### Makefile
Makefile has options to start the program and to clean everything after its work.
`run` - just starts the script
`cleanout` - removes .out files that are products of script.sh
`cleangraph` - removes build_requires and requires files that are realizations of Graphviz graphs in DOT language
`cleanpng` - removes .png files (supposed to be build_requires.png and requires.png)  

### script.sh
A bash script to collect requires and build requires data from spec files. It uses
`rpmspec -q --buildrequires >> br.out` for requires during build and
`rpmspec -q --requires >> r.out` for requires during runtime.  
After that the script launches **task.py**

### task.py
A python module to take the data from the script and to use Graphviz Python API for  creating graphs that the user will receive. It has a function named **proc** for processing the graph creation:
`proc(graph, packet_name, filename, verflag)`
It receives *graph* - Graphviz API class that is used for graph declaration  
*packet_name* - string that contains packet name. It is written by the user, and is used in graph's root. **Note**: For example, python-3 or LibreOffice packets use multiple spec files. That's why it is important to receive name from the user, because it may be unclear what spec has the right name for the packet.  
*filename* - name of the file that had been made by the script. Should be synced with graph's purpose (br.out for build requirements, r.out for runtime requirements)
*verflag* - flag for labeling the edges with the versions of required packets instead of leaving it in the nodes. For example, *cmake-data = 3.28.3-7* with verflag = True will be transformed into **"cmake-data" node** and **"= 3.28.3-7" label** on the edge.  
Also, if there is a condition for having a requirement, for example, *(cmake-rpm-macros = 3.28.3-7 if rpm-build)*, then the parentheses are removed, and future result depends on verflag, mentioned before.
