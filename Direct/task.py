from graphviz import Digraph, unflatten
from pathlib import Path


def pkgquery(graph, packet_name, pkgfile, verflag): # Обработка графа graph с корнем packet_name и узлами из файла filename
    # verflag - флаг, говорящий о том, пишем ли мы версии зависимостей на рёбрах графа или просто ничего не трогаем
    graph.node('packet', packet_name, shape='egg', color='blue')

    file = open(pkgfile, 'r')
    graph.attr('node', shape='box', color='green')

    graphname = graph.name
    i = 0

    br = "BuildRequires"
    rr = "Requires"
    pm = "%package"
    newspec = "%mainpackage" # Наша договорённость о том, как отмечаются в pkg.out новые spec файлы
    speccount = 0 # Количество обработанных spec файлов. Имеет роль для директив с 2 и более spec файлами, иначе не влияет

    parsed = file.readlines()

    pkg = packet_name
    graph.node('p0', pkg, shape='egg', color='red')
    graph.edge('packet', 'p0', "main package")
    pkgid = 0 # Сначала идёт += 1 => первый айди в проге далее будет 1
    pkgnode = 'p0'


    '''
    # ВНИМАНИЕ! ТО, ЧТО В АПОСТРОФАХ, - ОСОБЫЙ ФУНКЦИОНАЛ
    # По стандарту RPM spec файлов, если у нас есть подпакет, и у него какое-либо описание ПУСТОЕ (в частности, нам нужные
    # BuildRequires и Requires), то это описание у него ТАКОЕ ЖЕ, как у главного пакета
    # Эта опция реализует это в графе, но предупреждение: это делает граф визуально убийственным. Если хотите - уберите
    # апострофы, где они есть.
    # Обычно же, без этой опции, подразумевается, что "пустой" подпакет <=> все зависимости из главного пакета
    mainlst = []
    mainpkgnode = 'p1'
    reqcount = 0
    '''

    for line in parsed:
        if (line.startswith(br)) and graphname == "build_requires":
            line = line[len(br):] # Избавляемся от строки br
            if line.startswith('('):  # Получаем комментарий (метка на ребре)
                ind = line.find(')')
                comment = line[1:ind]
                line = line[ind + 1:]
            else:
                comment = str()

            line = line[1:]  # Избавляемся от :

            line = line.strip()
            if (line.startswith("(")) and (line.endswith(")")): # Удаляем некрасивые скобки при условиях
                line = line[1:-1]

            if verflag:  # Хотим указывать версии на рёбрах
                ind = line.find(' ')  # Версии зависимостей указывают после пробела
                if ind != -1:  # Указана версия
                    version = line[(ind + 1):]  # Запоминаем версию
                    line = line[:ind]  # Забываем обо всём до пробела (включительно)
                    graph.node(str(i), line)
                    comment += '\n' + version  # Делаем пометку на ребре о версии
                else:  # Версия не указана
                    graph.node(str(i), line)

                graph.edge(pkgnode, str(i), comment)
            else:
                graph.node(str(i), line)
                graph.edge(pkgnode, str(i), comment)
            '''
            if pkgnode == mainpkgnode:  # Main package
                mainlst.append([str(i), comment])

            reqcount += 1
            '''
            i += 1

        elif (line.startswith(rr)) and graphname == "runtime_requires":
            line = line[len(rr):] # Избавляемся от строки rr
            if line.startswith('('):  # Получаем комментарий (метка на ребре)
                ind = line.find(')')
                comment = line[1:ind]
                line = line[ind + 1:]
            else:
                comment = str()

            line = line[1:]  # Избавляемся от :

            line = line.strip()
            if (line.startswith("(")) and (line.endswith(")")): # Удаляем некрасивые скобки при условиях
                line = line[1:-1]

            if verflag:  # Хотим указывать версии на рёбрах
                ind = line.find(' ')  # Версии зависимостей указывают после пробела
                if ind != -1:  # Указана версия
                    version = line[(ind + 1):]  # Запоминаем версию
                    line = line[:ind]  # Забываем обо всём до пробела (включительно)
                    graph.node(str(i), line)
                    comment += '\n' + version  # Делаем пометку на ребре о версии
                else:  # Версия не указана
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
            if reqcount == 0: # Предыдущий пакет не добавил ни одной зависимости, значит всё как у main
                for elem in mainlst:
                    graph.edge(pkgnode, elem[0], elem[1])

            reqcount = 0
            '''

            line = line[len(pm):] # Избавляемся от строки pm
            line = line.lstrip()
            ind = line.find('-n')
            if ind != -1:
                line = line[ind+2:]
                line = line.rstrip()
                pkg = line
            else:
                line = line.rstrip()
                pkg = f'{packet_name}-{line}'

            pkgid += 1
            pkgnode = f'p{pkgid}'
            graph.node(pkgnode, pkg, shape='egg', color='red')
            graph.edge('packet', pkgnode)

        elif line.startswith(newspec):
            if speccount != 0:
                pkgid += 1
                pkg = f'{packet_name}:{speccount}'
                pkgnode = f'p{pkgid}'
                graph.node(pkgnode, pkg, shape='egg', color='red')
                graph.edge('packet', pkgnode, f"main package:{speccount}")

                '''
                mainpkgnode = pkgnode
                mainlst.clear()
                '''

            speccount += 1
        else:
            continue


    graph.attr(rankdir='LR')
    # numrow = round(i / 10)# Количество рядов в отображении
    out = graph.unflatten()

    # Выводим граф в файл и на экран
    output_path = out.render(filename=f'{graph.name}', view=True)  # Создаём в качестве файла наш граф

    print("Был создан граф:", output_path)



brgraph = Digraph(
        name='build_requires',  # Название графа
        comment='Отражение необходимостей для сборки пакета',
        format='png',  # Формат на выходе
        engine='dot'  # Движок для визуализации
)

rgraph = Digraph(
        name='runtime_requires',  # Название графа
        comment='Отражение необходимостей для работы пакета',
        format='png',  # Формат на выходе
        engine='dot'  # Движок для визуализации
)


print("Введите название пакета: ")
packet_name = input()
pkgfile = Path("./pkg.out")

pkgquery(brgraph, packet_name, pkgfile, True)
pkgquery(rgraph, packet_name, pkgfile, True)