from graphviz import Digraph, escape


def proc(graph, packet_name, filename, verflag): # Обработка графа graph с корнем packet_name и узлами из файла filename
    # verflag - флаг, говорящий о том, пишем ли мы версии зависимостей на рёбрах графа или просто ничего не трогаем
    graph.node('packet', packet_name, shape='egg', color='blue')

    file = open(filename, 'r')
    graph.attr('node', shape='box', color='green')
    i = 0
    for line in file.readlines():
        # line = escape('"' + line + '"')
        if verflag: # Хотим указывать версии на рёбрах
            ind = line.find('=') # Версии зависимостей указывают после знака =
            if ind != -1: # Указана версия
                version = line[(ind+1):] # Запоминаем версию
                line = line[:ind] # Забываем обо всём до = (включительно)
                if line[-1] == ' ':
                    line = line[:-1]
                graph.node(str(i), line)
                graph.edge('packet', str(i), version) # Делаем пометку на ребре о версии
            else: # Версия не указана
                graph.node(str(i), line)
                graph.edge('packet', str(i))

        else:
            graph.node(str(i), line)
            graph.edge('packet', str(i))

        i += 1

    graph.attr(rankdir='TB')

    # Выводим граф в файл и на экран
    output_path = graph.render(filename=graph.name, view=True)  # Создаём в качестве файла наш граф
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
proc(brgraph, packet_name, 'br.out', True)
proc(rgraph, packet_name, 'r.out', True)