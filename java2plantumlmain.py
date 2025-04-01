import os
from javaanalyzer import JavaAnalyzer

if __name__ == "__main__":
    analyzer = JavaAnalyzer() # get an analyzer for one project
    # then get all java files, analyze them by "analyzer.analyze_file"
    for root, dirs, files in os.walk("javaCodeTest3"):
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

