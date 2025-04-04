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

## Guide to use the program
**Step 0:** For using the program you will need `python3`, `python3-graphviz`, `make` to use it directly through your system and `docker` in addition to these if you wish to use containers. You should decide the way you will use, considering package's architecture dependencies. If you have multiple spec files in your package, bring them into one directory.  
**Step 1:** Copy needed directory (Container/Direct) to your system. Each of them has scripts, Makefiles, other files to make the process quick and convenient. The next steps will depend on the module you are going to use. Now we are working in the directory.  

### Direct usage
**Step 2:** Write `make` to start the Makefile. You will be asked to choose between a directory of specfiles and a single file. After choosing that, write a path to the directory/file. If everything is okay, the spec file(s) will be parsed into temporary file *pkg.out*.  
**Step 3:** Write a name for your parsed package. It will be used in graphs later. Then the *pkg.out* temporary file will be queried to create the graphs.  
The graphs will be output in your directory in DOT language as `build_requires` and `runtime_requires`, in PNG format as `build_requires.png` and `runtime_requires.png`. You may use `make png` to open both pngs.  
**Note:** If you wish to clean the results, just do `make clean`. There are other options to clean pngs: `make cleanpng`; .out: `make cleanout`; DOT: `make cleangraph`. To open graphs quickly, do `make graph`.  
You may read about the graph format lower.  

### Container usage
The difference between the direct and the container modules is in creating Docker container and running the program directly inside it. **Everything from the directory will be copied into the container - keep that in mind.** To use the module, you should have access to ROOT user (sudo/being root will do), since Docker needs root privileges to be used.  

**Step 2:** To launch a container, you must have **distributive image** that is needed for package and you must change **Dockerfile, run.sh, copy.sh**.  
Change the `FROM: image` in Dockerfile to your distributive image. Then change the container name that is going to be used in container creation and launching later. To do that, change `container_name` in run.sh and copy.sh to another name that will not correlate with others. `docker container ps -a` will help. Name `fedora` and image `fedora:latest` are set by default.  
**Step 3:** When step 2 is done, do `make dockrun`. You will be asked if you want to build {container_name}.img - that's container image. Do that, if you haven't built it yet or if you have changed something in directory. If everything is okay, you will get a terminal that provides access to the running container.  
**Step 4:** Do the steps 2-3 from Direct usage. That's right the same thing, you just do it in isolated system.  
**Step 5:** After these you may exit your container terminal or close it. Do `make dockcp` inside your native Container directory to copy the output of the program that is in container into your Container directory. After that you may use `make png` to see the graphs.  
**Note:** If you wish to clean the results, just do `make clean`. There are other options to clean pngs: `make cleanpng`; .out: `make cleanout`; DOT: `make cleangraph`. To open graphs quickly, do `make graph`.  
You may read about the graph format just there.  

### Graph format
After running the program, you will receive graphs in DOT and png formats.  
**Main node:** The main node (root node) has blue color and the name of the package that you have written before. The edges from it go to the subpackages of the spec file(s). If it has a label `main package:{index}`, it means, that it is main package (not described by %package) in the ({index}+1) spec file.  
**Subpackages and main package:** The nodes after the root node have red color and the names that are described in spec file(s). If the node describes main package, it will have the name of the package with index: `{package_name}`. They have edges that lead to their dependencies. If the node describes
subpackage and does not have any edges, it is meant that the subpackage has **the same dependencies as its main package**.  
**Dependencies:** The nodes after the packages nodes describe packages' dependencies. These nodes have box shape and green color. The edges leading to them may have labels that describe conditions of the dependency (such as version; mode, where the dependency is needed).  

## Problems with packages
If you still have problems with the package spec file (errors from rpmspec in particular), you should learn the distributive the package is meant for and use it in the container. The images for Docker containers are written on `https://hub.docker.com/`.  
If the distributive is the same as you are using right now, but you still have errors, you should try installing a package (the package itself, libs, macros definitions or etc), respective to the package you are trying to query. For example, to query python3.13 package, you should have **python3** or **python-rpm-macros** installed.  
