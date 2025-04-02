# Spec data extractor
The main goal of the program is to extract requirements and build requirements fields from a spec file or a set of spec files (located in one directory). They will be described as two graphs as the result of the program. Graphs will be directed and will show main package and subpackages dependencies. **IMPORTANT: If a subpackage does not have any edges, it is meant that it has the same dependencies as the main package (RPM standard). See task.py for more info.** Finally, there is a Makefile to make everything simpler and more convenient.  
You may notice two directives: Direct and Container. Direct is the lighter version of the program but is less unified. It just uses your system, your system's macro definitions in particular. Container directive is more sophisticated and uses Docker containers with set image.  
**Note: If you want to change the image (depends on your rpm packets), you should change ${container_name} in *run.sh* and *copy.sh* and change image in *Dockerfile*. You should have respective image installed.**  
The description of each file is below.  

## Direct
The basic instructions and modules for Direct usage (and for program usage inside the container).  

### Makefile
Makefile has options to start the program and to clean everything after its work.
`run` - just starts the script  
`png` - xdg-open build\_requires**.png** and runtime\_requires**.png**  
`graph` - xdg-open build\_requires and runtime\_requires (graphs described in DOT)  
`cleanout` - removes .out files that are products of script.sh  
`cleangraph` - removes build_requires and requires files that are realizations of Graphviz graphs in DOT language  
`cleanpng` - removes .png files (supposed to be build_requires.png and requires.png)  
`clean` - cleanpng, cleangraph and cleanout respectively  

### script.sh
A bash script to collect packages, their requires and build requires data from spec files. It uses
`rpmspec -P gcc.spec | grep -e %package -e BuildRequires -e Requires >> pkg.out` (or >) for grabbing everything we may use into pkg.out file.  
**Note:** If you choose querying a directive, then the script will add an information about the next spec file into the pkg.out through `echo "%mainpackage" >> pkg.out`. That is an agreement that doesn't correlate with other sections and descriptions. After that the script launches **task.py**.  
**Note: rpmspec may write warnings, but it is okay, if they are not related to macros, requires and buildrequires. Otherwise the information *may be* inaccurate, try changing the system distributive / container image. The 2nd way is described lower.**  

### task.py
A python module to take the data from the script and to use Graphviz Python API for creating graphs that the user will receive. Graphs are directed and have different colors and shapes for root node, subpackages and dependencies. If a subpackage has no edges, it is meant that it has dependencies equal to main package (see **Note 2**). Otherwise it has only the dependencies that it has edges with. 
Main function for querying the data is **pkgquery**:
`pkgquery(graph, packet_name, pkgfile, verflag)`
It receives *graph* - Graphviz API class that is used for graph declaration  
*packet_name* - string that contains packet name. It is written by the user, and is used in graph's root. **Note**: For example, python-3 or LibreOffice packets use multiple spec files. That's why it is important to receive name from the user, because it may be unclear what spec has the right name for the packet.  
*pkgfile* - name of the file that had been made by the script. Has everything needed for querying: BuildRequires, Requires, %package.
*verflag* - flag for labeling the edges with the versions of required packets instead of leaving it in the nodes. For example, *cmake-data = 3.28.3-7* with verflag = True will be transformed into **"cmake-data" node** and **"= 3.28.3-7" label** on the edge.  
**Note 1** If there is a condition for having a requirement, for example, *(cmake-rpm-macros = 3.28.3-7 if rpm-build)*, then the parentheses are removed, and future result depends on verflag, mentioned before.  
**Note 2** You may turn on the option to make edges from subpackages to main package dependencies just by removing ''' (commentary), but it is not recommended at all. Graphs of huge applications will be awful and non-informative.  

## Containers
The container has OS of the distributive written in $container_name. The container has everything from the Container directive and it should be launched in that directive. Besides setting up the container, everything is the same as for Direct usage, you just work inside the container's distributive. Everything for working with the container is described below.  
**Note: If you want to change the image (depends on your rpm packets), you should change ${container_name} in *run.sh* and *copy.sh* and change image in *Dockerfile*. You should have respective image installed.**  

### Dockerfile
File with instructions for Docker. Used for building the container's image. Needed packages are installed on build, and everything from the Container directive is copied into /app of container. If you want to change anything, rely on Dockerfile's docs.  

### run.sh
A bash script to build the container from Dockerfile and to run it. **IT MUST BE RAN FROM ROOT USER.** If the container hasn't been built yet, it's image will have id **${container\_name}_img**. The container will be run in interactive terminal with a name **${container\_name}_name**, and if there is another container with that name, the older one will be deleted.  
Used commands: 
`docker build -t "${container_name}_img" .` - building the container from Docker file  
`docker run --name "${container_name}_name" -it "${container_name}_img"` - launching the container with the respective image id and name. It is run in interactive terminal (-it)  
`docker rm "${container_name}_name"` - removing the old container with the same name  

### copy.sh
A bash script to copy the resulting data (DOT graphs and png) from the container with name **${container\_name}_name**. **IT MUST BE RAN FROM ROOT USER.** The script copies the data into */tmp/snap-private-tmp/snap.docker/tmp* and then fixes the permissions and moves the data into the current directory.  
Used commands: 
`docker cp ${container_name}_name:/app/... /tmp` - copy the ... from the container with name **${container\_name}_name** into */tmp/snap-private-tmp/snap.docker/tmp*  
`chmod 666 /tmp/snap-private-tmp/snap.docker/tmp/*` - fixing the permissions of the data. Needed because of root privileges of the container user.  
`mv /tmp/snap-private-tmp/snap.docker/tmp/... ./` - moving the ... from the /tmp of Docker into the current directory  

## Problems with packages
If you still have problems with the package spec file (errors from rpmspec in particular), you should learn the distributive the package is meant for and use it in the container. The images for Docker containers are written on `https://hub.docker.com/`.  
If the distributive is the same as you are using right now, but you still have errors, you should try installing a package (the package itself, libs, macros definitions or etc), respective to the package you are trying to query. For example, to query python3.13 package, you should have **python3** or **python-rpm-macros** installed.  
