import os
import sys
from javaanalyzer import JavaAnalyzer

if __name__ == "__main__":
    analyzer = JavaAnalyzer() # get an analyzer for one project
    # then get all java files, analyze them by "analyzer.analyze_file"
    # 获取命令行参数
    if len(sys.argv) != 2:
        print("Usage: java2plantumlmain.py <path_to_java_files>")
        exit()
    path_to_java_files = sys.argv[1]
    for root, dirs, files in os.walk(path_to_java_files):
        for file in files:
            if file.endswith(".java"):
                analyzer.analyze_file(os.path.join(root, file))

    # analyze dependence and association
    analyzer.analyze_relations()

    #final print
    print('@startuml')
    analyzer.print_packages()
    analyzer.print_relations()
    print('@enduml')

