from java2plantumltool import Java2PlantUMLTool, UMLRelationship
from javavariable import JavaFormalParameter, JavaType
from javalang.tree import MethodDeclaration, ConstructorDeclaration, ReferenceType
from javacontext import JavaClassContext

class JavaMethod:
    # 'throws' for future
    attrs = ['name', 'return_type', 'modifiers', 'parameters', 'throws', 'body', 'dependencies']
    def __init__(self, declaration: MethodDeclaration, context: JavaClassContext|None = None):
        self.name = declaration.name #type: ignore
        self.return_type = JavaType.resolve_type(declaration.return_type) #type: ignore
        self.modifiers = declaration.modifiers #type: ignore
        self.parameters = [JavaFormalParameter(p) for p in declaration.parameters] #type: ignore
        self.body = declaration.body #type: ignore
        self.throws = declaration.throws #type: ignore
        self.dependencies = []
        # self.context = context
    
    def __str__(self):
        return f"{Java2PlantUMLTool.print_modifiers(self.modifiers)}{self.return_type} {self.name}({', '.join([str(p) for p in self.parameters])})"

    def parse_dependencies(self, context: JavaClassContext, ignore: set[str] | None = None):
        if context is None:
            return
        types_set:set[str] = set()
        if ignore is None or self.return_type not in ignore:
            types_set.add(self.return_type)
        
        for parameter in self.parameters:
            if ignore is None or parameter.type not in ignore:
                types_set.add(parameter.type)
        
        if self.body:
            for statement in self.body:
                for _, node in statement.filter(ReferenceType):
                    if ignore is None or node.name not in ignore:
                        types_set.add(node.name)
        
        for t in types_set:
            class_path = context.get_full_class_path(t)
            if class_path is not None:
                self.dependencies.append(class_path)


    @property
    def dependencies_list(self):
        return [f"{self.name} {UMLRelationship.DEPEND} {d}" for d in self.dependencies]


class JavaConstructor:
    attrs = ['name', 'modifiers', 'parameters', 'throw', 'body', 'dependencies']
    def __init__(self, declaration: ConstructorDeclaration, context: JavaClassContext | None = None):
        self.name = declaration.name #type: ignore
        self.modifiers = declaration.modifiers #type: ignore
        self.parameters = [JavaFormalParameter(p) for p in declaration.parameters] #type: ignore
        self.body = declaration.body #type: ignore
        self.throws = declaration.throws #type: ignore
        # self.context = context
        self.dependencies = []

    def __str__(self):
        return f"{Java2PlantUMLTool.print_modifiers(self.modifiers)}{self.name}({', '.join([str(p) for p in self.parameters])})"
    def parse_dependencies(self, context: JavaClassContext, ignore: set[str] | None = None):
        if context is None:
            return
        types_set:set[str] = set()
        for parameter in self.parameters:
            if ignore is None or parameter.type not in ignore:
                types_set.add(parameter.type)
        if self.body:
            for statement in self.body:
                for _, node in statement.filter(ReferenceType):
                    if ignore is None or node.name not in ignore:
                        types_set.add(node.name)
        for t in types_set:
            class_path = context.get_full_class_path(t)
            if class_path is not None:
                self.dependencies.append(class_path)
    
    @property
    def dependencies_list(self):
        return [f"{self.name} {UMLRelationship.DEPEND} {d}" for d in self.dependencies]
