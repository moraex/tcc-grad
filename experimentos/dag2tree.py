import networkx as nx
import sys
import utils


class Graph:
    T = None
    DAG = None
    leaves = None

    def __init__(self, edges) -> None:
        self.DAG = nx.DiGraph()
        self.DAG.add_edges_from(edges)
        # construo uma arvore a partir de um DAG
        self.T = nx.dfs_tree(self.DAG, source="root")
        self.leaves = [v for v, d in self.T.out_degree() if d == 0]

    def antecessors(self, node):
        """retorna um vetor com todos os antecessores
        do nó node até a raiz da arvore T"""
        q = [node]
        paths = []
        while q:
            node = q.pop(0)
            paths.append(node)
            if not self.T.pred[node]:
                break
            q.append(list(self.T.pred[node])[0])
        return paths

    def antecessors2str(self, antecessors):
        """ recebe um vetor de antecessores e 
        retorna no formato 'root/class_0/class_1/.../class_n'"""
        return '/'.join(antecessors.__reversed__())

    def treeSpace2Str(self):
        """retorna todas as combinações de caminhos possiveis de uma árvore"""
        paths = nx.all_simple_paths(self.T, source="root", target=self.leaves)
        output_tree_space = []
        for path in list(paths):
            p = path
            while p:
                output_tree_space.append('/'.join(p))
                p.pop(-1)
        return ",".join(set(output_tree_space))

    def parseManyClasses2Tree(self, string):
        """recebe uma string de DAG classes e retorna a correspondencia em Tree"""
        target_sample_space = []
        sample_classes = list(string.split("@"))
        target_sample_space = [self.antecessors2str(
            self.antecessors(c)) for c in sample_classes]
        return '@'.join(target_sample_space)


class ParseArff:
    file_attr_space = []
    class_attr_space = []
    data_indicator_line = []
    data_space = []
    _Graph = None
    _OSPath = None

    def __init__(self, file_arff) -> None:
        self._OSPath = utils.OSPath(file_arff)
        file = utils.ReadFile().read(self._OSPath.full)
        self.runFile(file)
        self.initEdges(self.class_attr_space[0].split(" ")[-1])
        self.reshapeClassSpace()
        self.reshapeSampleClassSpace()
        self.generateTreeFile(
            f"{self._OSPath.path}/{self._OSPath.file_name}.trainvalid.fake.arff")

    def runFile(self, file):
        curr_sample_idx = 0
        relation = False
        class_idx_line = 0

        for line in file:
            curr_sample_idx += 1
            if (not relation) and line.count("@RELATION"):
                self.file_attr_space.append(line)
                self.file_attr_space.append("\n")
                relation = True

            if line.count("@DATA"):
                self.data_indicator_line.append("\n")
                self.data_indicator_line.append(line)
                break

            if line.count("@ATTRIBUTE class "):
                self.class_attr_space.append(line)
                class_idx_line = curr_sample_idx
            elif line.count("@ATTRIBUTE "):
                self.file_attr_space.append(line)

        for line in file[curr_sample_idx:]:
            if line.replace("\n", "") != "":
                self.data_space.append(line)

    def initEdges(self, dag_string_space):
        dag_string = dag_string_space.replace("\n", "")
        edges = [tuple(v.split("/")) for v in dag_string.split(",")]
        self._Graph = Graph(edges)

    def reshapeClassSpace(self):
        new_class_attr_space = self.class_attr_space[0].split(" ")
        new_class_attr_space[-1] = self._Graph.treeSpace2Str() + "\n"
        self.class_attr_space = [" ".join(new_class_attr_space)]

    def reshapeSampleClassSpace(self):
        new_data_space = []
        for line in self.data_space:
            arr_line = line.replace("\n", "").split(",")
            arr_line[-1] = self._Graph.parseManyClasses2Tree(arr_line[-1])
            new_line = ','.join(arr_line) + '\n'
            new_data_space.append(new_line)
        self.data_space = new_data_space

    def generateTreeFile(self, file_name):
        output = self.file_attr_space + self.class_attr_space + \
            self.data_indicator_line + self.data_space
        utils.WriteFile().write(file_name, output)


if __name__ == '__main__':
    dataset = sys.argv[1]
    ParseArff(dataset)
