# java code to plantuml

## how to use

env: python 3.11

1. install java lang

   ```cmd
   pip install javalang
   ```
2. modify java2plantumlmain.py

   ```python
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

   ```
3. run java2plantumlmain.py

## feature

1. support multi-files
2. support simple package, class, interface, enum, method, field

## future

1. inner class support

## structure

```puml
@startuml

' 基本类结构
class BaseJavaClass {
    # name: str
    # modifiers: set[str]
    # fields: list[JavaField]
    # constructors: list[JavaConstructor]
    # methods: list[JavaMethod]
    # extends: str | list[str]
    # implements: list[str]
    # relations: list[str]
    + __init__(declaration: ClassDeclaration, context: JavaClassContext)
    + _parse_fields()
    + _parse_constructors()
    + _parse_methods()
    + parse_relationships()
}

class JavaClass {
    + __str__()
}
JavaClass --|> BaseJavaClass

class JavaInterface {
    + __str__()
}
JavaInterface --|> BaseJavaClass

class JavaEnum {
    - constants: list[str]
    + __str__()
}
JavaEnum --|> BaseJavaClass

' 辅助工具类
class Java2PlantUMLTool {
    {static} _VISIT_MODIFIERS_SYMBOL: dict
    {static} _OTHER_MODIFIERS_SYMBOL: dict
    {static} print_modifiers(modifiers: set[str] | str)
}

enum UMLRelationship {
    INNER = "-+"
    DEPEND = ".>"
    ASSOCIATE = "->"
    IMPLEMENT = ".|>"
    EXTEND = "-|>"
}

' 字段和方法相关
class JavaField {
    - name: str
    - type: str
    - modifiers: set[str]
    - documentation: str
    + __str__()
    {static} resolve_fields(declaration: FieldDeclaration)
}

class JavaFormalParameter {
    - name: str
    - type: str
    - varargs: bool
    + __str__()
}

class JavaMethod {
    - name: str
    - return_type: str
    - parameters: list[JavaFormalParameter]
    + parse_dependencies()
    + __str__()
}

class JavaConstructor {
    - name: str
    - parameters: list[JavaFormalParameter]
    + parse_dependencies()
    + __str__()
}

' 包和上下文管理
class JavaPackage {
    - name: str
    - classes: dict[str, JavaClass | JavaInterface | JavaEnum]
    + parse(declarations: list)
    + parse_relations()
}

class JavaClassContext {
    - class_package_dict: dict[str, str]
    + get_full_class_path(class_name: str)
}

' 核心分析器
class JavaAnalyzer {
    - __packages: dict[str, JavaPackage]
    + analyze_file(filepath: str)
    + analyze_relations()
    + print_packages()
}

' 类型处理
class JavaType {
    {static} resolve_type(type_node)
}

' 依赖关系
JavaAnalyzer -> JavaPackage
JavaPackage "1" *--> "0..*" JavaClass
JavaPackage "1" *--> "0..*" JavaInterface
JavaPackage "1" *--> "0..*" JavaEnum

BaseJavaClass o--> JavaField
BaseJavaClass o--> JavaMethod
BaseJavaClass o--> JavaConstructor
BaseJavaClass o--> JavaClassContext

JavaMethod o--> JavaFormalParameter
JavaConstructor o--> JavaFormalParameter

JavaMethod ..> JavaType : uses
JavaField ..> JavaType : uses
JavaFormalParameter .left.> JavaType : uses

BaseJavaClass .left.> Java2PlantUMLTool : uses
JavaMethod .up.> Java2PlantUMLTool : uses
JavaConstructor .up.> Java2PlantUMLTool : uses
JavaField .up.> Java2PlantUMLTool : uses
JavaFormalParameter .up.> Java2PlantUMLTool : uses

BaseJavaClass .left.> UMLRelationship : uses
JavaMethod .> UMLRelationship : uses
JavaConstructor .> UMLRelationship : uses

@enduml
```
