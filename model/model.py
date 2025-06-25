import copy

import networkx as nx
from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.DiGraph()
        self._nodes = []
        self._idMap = {}
        self._bestPath = []
        self._bestScore = 0

    def trovaCammino(self, store_id):
        self._bestPath = []
        self._bestScore = 0

        source = self._idMap[int(store_id)]
        self._ricorsione([source])
        return self._bestPath, self._bestScore

    def _ricorsione(self, parziale):
        successori = list(self._grafo.successors(parziale[-1]))

        if self._score(parziale) > self._bestScore:
            self._bestPath = copy.deepcopy(parziale)
            self._bestScore = self._score(parziale)
        else:
            for n in successori:
                if len(parziale) ==1:
                    parziale.append(n)
                    self._ricorsione(parziale)
                    parziale.pop()
                else:
                    if n not in parziale and self._grafo[parziale[-1]][n]['weight'] < self._grafo[parziale[-2]][parziale[-1]]['weight']:
                        parziale.append(n)
                        self._ricorsione(parziale)
                        parziale.pop()

    def _score(self, parziale):
        score = 0
        for i in range(len(parziale) -1):
            score += self._grafo[parziale[i]][parziale[i+1]]['weight']
        return score


    def builtGraph(self, store_id, k):
        self._nodes = DAO.getVertici(store_id)
        self._grafo.add_nodes_from(self._nodes)
        for nodo in self._nodes:
            self._idMap[nodo.order_id] = nodo

        archi = DAO.getArchi(store_id, k, self._idMap)
        for arco in archi:
            self._grafo.add_edge(arco[0], arco[1], weight=arco[2])

    def getBFSNodesFromTree(self, source):
        tree = nx.bfs_tree(self._grafo, self._idMap[int(source)])
        archi = list(tree.edges())
        nodi = list(tree.nodes())
        return nodi[1:]

    def getDFSNodesFromTree(self, source):
        tree = nx.dfs_tree(self._grafo, source)
        nodi = list(tree.nodes())
        return nodi[1:]

    def getCammino(self, sourceStr):
        source = self._idMap[int(sourceStr)]
        lp = []
        # for source in self._graph.nodes:
        tree = nx.dfs_tree(self._grafo, source)
        nodi = list(tree.nodes())

        # Per ogni nodo raggiunto dal DFS...
        for node in nodi:
            tmp = [node] #Ricostruisce il cammino dal nodo source a node risalendo l’albero.
            while tmp[0] != source:
                pred = nx.predecessor(tree, source, tmp[0])  #Usa nx.predecessor() per ottenere il padre di un nodo (cioè da dove è arrivato nella DFS).
                tmp.insert(0, pred[0])  #tmp diventa un cammino completo da source a node.
                # tree: è il grafo orientato (in questo caso un albero DFS) da usare come riferimento per trovare il predecessore.
                # source: è il nodo di partenza da cui è cominciata la DFS. tmp[0]: è il nodo attuale da cui vogliamo risalire all’indietro, verso la sorgente
                # tmp.insert(0, pred[0]) inserisci B all’inizio di tmp, che diventa [B, C]
            if len(tmp) > len(lp):  #Se tmp è più lungo del miglior cammino trovato finora (lp), allora lo aggiorna.
                lp = copy.deepcopy(tmp)
        return lp


    def numArchi(self):
        return self._grafo.number_of_edges()

    def getStores(self):
        return DAO.getStores()