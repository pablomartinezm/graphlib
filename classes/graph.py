# -*- coding: utf-8 -*-
__author__ = """\n""".join(['Sergio Montoya de Paco <sergio.mp1710@gmail.com>',
                            'Daniel Monzonís Laparra <dani.monzonis@gmail.com>'])

class Graph:
    """
Clase Graph, que representa un grafo (conjunto de vértices y aristas). La clase representa un grafo no dirigido, por lo tanto, 
las aristas que unen dos vértices son bidireccionales.
Métodos:
    -def __init__(self): Constructor de la clase, donde se crea el conjunto vacío de nodos y aristas.
    -def node(self)(@property): Atributo que es un conjunto de nodos en un diccionario, donde la key es el nodo y el value son
     los atributos del nodo.
    -def edge(self)(@property): Atributo que es un conjunto de aristas en un diccionario, donde la key es un nodo y los value
     son diccionarios, donde la key es el nodo al que va la arista y el value los atributos de dicha arista.
    -def nodes(self): Devuelve una lista con todos los nodos.
    -def edges(self): Devuelve una lista con tuplas que representan las aristas (nodo1,nodo2)
    -def add_node(self, node, attr_dict=None): Añade el nodo al diccionario de nodos, si el elemento ya existía, en caso de que
     se especifique un nuevo atributo, se añadirá al diccionario de atributos. 'attr_dict' = dictionary
    -def add_edge(self, node1, node2, attr_dict=None): Añade una arista al diccionario de aristas, si uno de los nodos
     especificados no existe, se creará el nodo de forma implícita. 'attr_dict' especifica un atributo para la arista, si ya
     contenía un atributo, se añade al diccionario de atributos.
    -def add_nodes_from(self, node_list, attr_dict=None): Añade todos los nodos especificados en la lista 'node_list', a todos
     les añade los atributos especificados en 'attr_dict'.
    -def add_edges_from(self, edge_list, attr_dict=None): Añade todas las aristas especificadas en la lista 'edge_list', a 
     todas les añade los atributos especificados en 'attr_dict'.
    -def degree(self,node): Devuelve el grado del nodo 'node', si el nodo no existe, lanza una excepción.
    -def __getitem__(self, node): Devuelve los nodos a los cuales está conectado el nodo 'node', con los respectivos atributos
     de cada arista, en forma de diccionario. {node1:{attributes},node2:{attributes}}.
    -def __len__(self): Devuelve el número de nodos que hay en el grafo.
    -def neighbors(self, node): Devuelve una lista con los nodos incidentes en el nodo 'node'.
    -def remove_node(self, node1): Elimina el nodo 'node1' del grafo y todas sus aristas incidentes.
    -def remove_edge(self, node1, node2): Elimina la arista (node1,node2) del grafo. Ímplicitamente se elimina también la
     arista (node2,node1).
    -def remove_nodes_from(self, node_list): Elimina todos los nodos especificados en la lista de nodos 'node_list'. De igual
     forma que en la función remove_node, se elimina el nodo y todas sus aristas incidentes.
    -def remove_edges_from(self, edge_list): Elimina todas las aristas especificadas en la lista de aristas 'edge_list'. De 
     igual forma que en la función remove_edge, se elimina la arista birideccional (se elimina tanto (node1,node2) como 
     (node2,node1)).
    """
    def __init__(self):
        """Constructor de la clase, donde se crea el conjunto vacío de nodos y aristas."""
        self._nodes = {}
        self._edges = {}

    @property
    def node(self):
        """(Atributo) Conjunto de nodos en un diccionario, donde la key es el nodo y el value son los atributos del nodo."""
        return self._nodes

    @property
    def edge(self):
        """
        (Atributo) Conjunto de aristas en un diccionario, donde la key es un nodo y los value son diccionarios, 
        donde la key es el nodo al que va la arista y el value los atributos de dicha arista.
        """
        return self._edges

    def nodes(self):
        """Devuelve una lista con todos los nodos."""
        return list(self._nodes.keys())

    def edges(self):
        """Devuelve una lista con tuplas que representan las aristas (nodo1,nodo2)"""
        edges_list = []
        for n1 in self._edges.keys():
            for n2 in self._edges[n1].keys():
                if not (n2, n1) in edges_list:
                    edges_list.append((n1, n2))
        return edges_list

    def add_node(self, node, attr_dict=None):
        """
        Añade el nodo al diccionario de nodos, si el elemento ya existía, en caso de que se especifique un nuevo atributo,
        se añadirá al diccionario de atributos. 'attr_dict' = dictionary
        """
        if attr_dict is None:
            node_dict = {}
        else:
            # Tenemos que crear una copia del diccionario, porque si no utilitzamos el método add_nodes_from, estaremos
            # asignando un mismo diccionario de atributos a múltiples nodos (y si modificamos los atributos de un nodo,
            # modificaremos también los demás nodos).
            node_dict = attr_dict.copy()

        if node in self._nodes:
            if attr_dict:
                self._nodes[node].update(node_dict)
        else:
            self._nodes[node] = node_dict
            # Añadimos el nodo al diccionario de aristas, aunque su grado sea 0, así podremos
            # utilizar métodos como degree(node) o neighbors(node).
            self._edges[node] = {}

    def add_edge(self, node1, node2, attr_dict=None):
        """
        Añade una arista al diccionario de aristas, si uno de los nodos especificados no existe, se creará el nodo de forma implícita. 
        'attr_dict' especifica un atributo para la arista, si ya contenía un atributo, se añade al diccionario de atributos.
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

        # Añadimos para una arista que va del nodo A al B, la arista que va de A a B y la arista que va de B a A.
        for n1, n2 in [(node1, node2), (node2, node1)]:

            if self._edges[n1] != {}:
                if n2 in self._edges[n1] and edge_dict:
                    self._edges[n1][n2].update(edge_dict)
                else:
                    self._edges[n1][n2] = edge_dict
            else:
                self._edges[n1].update({n2: edge_dict})

    def add_nodes_from(self, node_list, attr_dict=None):
        """Añade todos los nodos especificados en la lista 'node_list' [nodo1,nodo2,...], a todos les añade los atributos especificados en 'attr_dict'."""
        for new_node in node_list:
            self.add_node(new_node, attr_dict)

    def add_edges_from(self, edge_list, attr_dict=None):
        """
        Añade todas las aristas especificadas en la lista 'edge_list' [(nodo1,nodo2),(nodo2,nodo3),...], a todas les añade 
        los atributos especificados en 'attr_dict'.
        """
        for new_edge in edge_list:
            self.add_edge(new_edge[0], new_edge[1], attr_dict)

    def degree(self, node):
        """Devuelve el grado del nodo 'node', si el nodo no existe, lanza una excepción."""
        if node in self._edges:
            return len(self._edges[node])
        else:
            raise ValueError("El nodo " + str(node) + " no existe")

    def __getitem__(self, node):
        """
        Devuelve los nodos a los cuales está conectado el nodo 'node', con los respectivos atributos
        de cada arista, en forma de diccionario. {node1:{attributes},node2:{attributes}}.
        """
        if node in self._edges:
            return self._edges[node]
        else:
            raise ValueError("El nodo " + str(node) + " no existe")

    def __len__(self):
        """Devuelve el número de nodos que hay en el grafo."""
        return len(self._nodes)

    def neighbors(self, node):
        """Devuelve una lista con los nodos incidentes en el nodo 'node'."""
        if node in self._edges:
            return list(self._edges[node].keys())
        else:
            raise ValueError("El nodo " + str(node) + " no existe")

    def remove_node(self, node1):
        """Elimina el nodo 'node1' del grafo y todas sus aristas incidentes."""
        if node1 not in self._nodes:
            raise ValueError("El nodo " + str(node1) + " no existe")

        # Primero eliminamos el nodo del conjunto de nodos
        del self._nodes[node1]

        # Y ahora eliminamos todas sus aristas incidentes
        if node1 in self._edges:
            edges_list_to_remove = [node2 for node2 in self._edges[node1].keys()]
            del self._edges[node1]
            for node in edges_list_to_remove:
                del self._edges[node][node1]

    def remove_edge(self, node1, node2):
        """Elimina la arista (node1,node2) del grafo. Ímplicitamente se elimina también la arista (node2,node1)."""
        if node1 not in self._edges:
            raise ValueError("El nodo " + str(node1) + " no existe")
        if node2 not in self._edges:
            raise ValueError("El nodo " + str(node2) + " no existe")
        if node2 not in self._edges[node1]:
            raise ValueError("El nodo " + str(node1) + " no está conectado con el nodo " + str(node2))

        # Eliminamos tanto la arista (node1,node2) como la arista (node2,node1)
        for n1, n2 in [(node1, node2), (node2, node1)]:
            del self._edges[n1][n2]

    def remove_nodes_from(self, node_list):
        """
        Elimina todos los nodos especificados en la lista de nodos 'node_list' [nodo1,nodo2,...]. De igual forma que en la 
        función remove_node, se elimina el nodo y todas sus aristas incidentes.
        """
        for node in node_list:
            self.remove_node(node)

    def remove_edges_from(self, edge_list):
        """
        Elimina todas las aristas especificadas en la lista de aristas 'edge_list' [(nodo1,nodo2),(nodo2,nodo3),...]. De igual forma
        que en la función remove_edge, se elimina la arista birideccional (se elimina tanto (node1,node2) como (node2,node1)).
        """
        for edge in edge_list:
            self.remove_edge(edge[0], edge[1])
