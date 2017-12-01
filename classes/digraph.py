'''
DiGraph
'''

from . import Graph


class DiGraph(Graph):
    """
    Representa un grafo dirigido, donde las aristas no son necesariamente bidireccionales.
    """

    def add_edge(self, node1, node2, attr_dict=None):
        """
        Añade la arista que va de node1 a node2 al grafo. Si alguno de los nodos no existe,
        se crea implícitamente.
        'attr_dict' especifica un atributo para la arista, si ya contenía un atributo,
        se añade al diccionario de atributos.
        """
        if attr_dict is None:
            edge_dict = {}
        else:
            # Tenemos que crear una copia del diccionario, porque si no utilitzamos el método add_edges_from, estaremos
            # asignando un mismo diccionario de atributos a múltiples aristas (y si modificamos los atributos de una arista,
            # modificaremos también las demás aristas).
            edge_dict = attr_dict.copy()

        # Comprovamos si los dos nodos existe, si no existe alguno, lo creamos y después creamos la arista.
        if node1 not in self.nodes():
            self.add_node(node1)
        if node2 not in self.nodes():
            self.add_node(node2)

        # Añadimos únicamente la arista que va de node1 a node2, ya que el grafo es dirigido
        if self._edges[node1] != {}:
            if node2 in self._edges[node1] and edge_dict:
                self._edges[node1][node2].update(edge_dict)
            else:
                self._edges[node1][node2] = edge_dict
        else:
            self._edges[node1].update({node2: edge_dict})
