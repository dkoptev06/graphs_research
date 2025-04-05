# Свойства дискретно-треугольных графов

Основная часть исследования проводилась в _Jupyter Notebook_, доступном по [ссылке](https://colab.research.google.com/drive/1PNQFd-zG_b4c0KlOYnMoeCpPHLoo9KCF).

В этом репозитории содержатся программы, использованные для задач, которые было удобнее выполнять локально. Здесь имеются следующие файлы:

+ [dtg.cpp](https://github.com/dkoptev06/graphs_research/blob/master/dtg.cpp) &mdash; программа, в которой реализована проверка графов на дискретно-треугольность. В ней имеются два наследника общего класса `DtgCheckerInterface`: `SimpleDtgChecker`, осуществляющий проверку на дискретно-треугольность по определению, и `FastDtgChecker`, осуществляющий проверку на дискретно-треугольность, оптимизированную для графов диаметра $2$. Сравнение скорости их работы приведено в программе [compare_checkers.cpp](https://github.com/dkoptev06/graphs_research/blob/master/compare_checkers.cpp). 
+ [filter_graphs.cpp](https://github.com/dkoptev06/graphs_research/blob/master/filter_graphs.cpp) &mdash; программа, принимающая на стандартный ввод список графов,  и выводящая на стандартный вывод только дискретно-треугольные среди них.
+ [check_random_graphs.cpp](https://github.com/dkoptev06/graphs_research/blob/master/check_random_graphs.cpp) &mdash; программа, осуществляющая многопоточный подсчет количества дискретно-треугольных графов среди случайных в модели $G\left(n, \frac{1}{2}\right)$.
+ [collections.py](https://github.com/dkoptev06/graphs_research/blob/master/collections.py) &mdash; программа, обрабатывающая онлайн-коллекцию графов. Производит скачивание наборов графов из онлайн-коллекции, и сохраняет на диск найденные дискретно-треугольные графы.
+ [extend_graph.cpp](https://github.com/dkoptev06/graphs_research/blob/master/extend_graph.cpp) &mdash; программа, осуществляющая многопоточный перебор способов добавить в дискретно-треугольный граф одну вершину так, чтобы он остался дискретно-треугольным.
+ [link_extractor.py](https://github.com/dkoptev06/graphs_research/blob/master/link_extractor.py) &mdash; вспомогательная программа, которая выводит список ссылок на все файлы из онлайн-коллекции графов.
