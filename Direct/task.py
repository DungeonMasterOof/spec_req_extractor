from graphviz import Digraph, unflatten
from pathlib import Path


def pkgquery(graph, app_name, pkgfile, verflag): # Querying graph "graph" with "app_name" root node and edges from "filename" file
    # verflag is a flag that tells us if we are writing versions and conditions above the edges of the graph or leave them in nodes
    graph.node('packet', app_name, shape='egg', color='blue')

    file = open(pkgfile, 'r')
    graph.attr('node', shape='box', color='green')

    graphname = graph.name
    i = 0

    br = "BuildRequires"
    rr = "Requires"
    pm = "%package"
    newspec = "%mainpackage" # Our agreement about the new spec file start labeling in filename
    newname = "Name"
    package_name = app_name # May be changed (if met "Name:")
    speccount = 0 # Number of queried spec files. Makes sense for directories with 2 and more specs

    parsed = file.readlines()

    # Getting first name
    firstline = parsed[0]
    if firstline.startswith(newname):
        firstline = firstline[len(newname) + 1:]  # Getting rid of newname string and :
        firstline = firstline.strip()
        package_name = firstline

    pkg = package_name
    graph.node('p0', pkg, shape='egg', color='red')
    graph.edge('packet', 'p0', "main package")
    pkgid = 0 # Id for the first main package
    pkgnode = 'p0'

    '''
    # EVERYTHING THAT IS IN TRIPLE ' IS SPECIAL
    # According to RPM spec files standard, if you have a subpackage, and if any of its fields is EMPTY (particularly 
    # BuildRequires & Requires) then that field will be THE SAME AS THE MAIN PACKAGE'S ONE 
    # That option is turned off there, because it makes graph inconvenient as hell. If you wish to turn it on, delete
    # the triple ' everywhere you see them
    # Otherwise it is meant that subpackage without dependency edges has the same dependencies as the main package
    mainlst = []
    mainpkgnode = 'p1'
    reqcount = 0
    '''

    for line in parsed:
        if (line.startswith(br)) and graphname == "build_requires":
            line = line[len(br):] # Getting rid of br string
            if line.startswith('('):  # Getting the conditions
                ind = line.find(')')
                comment = line[1:ind]
                line = line[ind + 1:]
            else:
                comment = str()

            line = line[1:]  # Getting rid of :

            line = line.strip()
            if (line.startswith("(")) and (line.endswith(")")): # Deleting excessive parentheses
                line = line[1:-1]

            if verflag:  # If we want to put conditions on edges
                ind = line.find(' ')  # Versions of conditions are written after whitespace
                if ind != -1:  # Found condition
                    version = line[(ind + 1):]  # Remember it
                    line = line[:ind]  # Save everything until the whitespace
                    graph.node(str(i), line)
                    comment += '\n' + version  # Making label on the edge
                else:  # No condition found
                    graph.node(str(i), line)

                graph.edge(pkgnode, str(i), comment)
            else: # Conditions inside the node
                graph.node(str(i), line)
                graph.edge(pkgnode, str(i), comment)
            '''
            if pkgnode == mainpkgnode:  # Main package
                mainlst.append([str(i), comment])

            reqcount += 1
            '''
            i += 1

        elif (line.startswith(rr)) and graphname == "runtime_requires":
            line = line[len(rr):] # Getting rid of rr string
            if line.startswith('('):  # Getting the conditions
                ind = line.find(')')
                comment = line[1:ind]
                line = line[ind + 1:]
            else:
                comment = str()

            line = line[1:]  # Getting rid of :

            line = line.strip()
            if (line.startswith("(")) and (line.endswith(")")): # Deleting excessive parentheses
                line = line[1:-1]

            if verflag:  # If we want to put conditions on edges
                ind = line.find(' ')  # Versions of conditions are written after whitespace
                if ind != -1:  # Found condition
                    version = line[(ind + 1):]  # Remember it
                    line = line[:ind]  # Save everything until the whitespace
                    graph.node(str(i), line)
                    comment += '\n' + version  # Making label on the edge
                else:  # No condition found
                    graph.node(str(i), line)

                graph.edge(pkgnode, str(i), comment)
            else:
                graph.node(str(i), line)
                graph.edge(pkgnode, str(i), comment)

            '''
            if pkgnode == mainpkgnode:  # Main package
                mainlst.append([str(i), comment]) # Adding to a list

            reqcount += 1
            '''
            i += 1

        elif line.startswith(pm):
            '''
            if reqcount == 0: # Previous package had no dependency described <=> everything from mainpackage
                for elem in mainlst:
                    graph.edge(pkgnode, elem[0], elem[1])

            reqcount = 0
            '''

            line = line[len(pm):] # Getting rid of pm string
            line = line.lstrip()
            ind = line.find('-n')
            if ind != -1:
                line = line[ind+2:]
                line = line.rstrip()
                pkg = line
            else:
                line = line.rstrip()
                pkg = f'{package_name}-{line}'

            pkgid += 1
            pkgnode = f'p{pkgid}'
            graph.node(pkgnode, pkg, shape='egg', color='red')
            graph.edge('packet', pkgnode)

        elif line.startswith(newspec):
            if speccount != 0:
                pkgid += 1
                pkg = f'{package_name}'
                pkgnode = f'p{pkgid}'
                graph.node(pkgnode, pkg, shape='egg', color='red')
                graph.edge('packet', pkgnode, f"main package:{speccount}")

                '''
                mainpkgnode = pkgnode
                mainlst.clear()
                '''

            speccount += 1

        elif line.startswith(newname):
            line = line[len(newname)+1:] # Getting rid of newname string and :
            line = line.strip()
            package_name = line

        else:
            continue


    graph.attr(rankdir='LR')
    # numrow = round(i / 10) # Number of words in dependencies, if you wish to change unflatten scatter parameter
    out = graph.unflatten()

    # Outputting the graph and showing it
    output_path = out.render(filename=f'{graph.name}', view=True)  # Grapviz graph -> 2 files (DOT and png)
    print("The graph was created. Its path:", output_path)



brgraph = Digraph(
        name='build_requires',  # Graph name
        comment='Отражение необходимостей для сборки пакета',
        format='png',  # Format of output
        engine='dot'  # Visualization engine
)

rgraph = Digraph(
        name='runtime_requires',  # Graph name
        comment='Отражение необходимостей для работы пакета',
        format='png',  # Format of output
        engine='dot'  # Visualization engine
)


print("Write the name of the app: ")
app_name = input()
pkgfile = Path("./pkg.out")

pkgquery(brgraph, app_name, pkgfile, True)
pkgquery(rgraph, app_name, pkgfile, True)