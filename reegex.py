from queue import LifoQueue
from bag import Bag


class Digraph():
    def __init__(self, V: int):
        self._V = V
        self._E = 0
        self._adj = Bag()
        for v in range(V):
            self._adj.add(Bag())

    @property
    def V(self):
        return self._V

    @property
    def E(self):
        return self._E

    def addEdge(self, v: int, w: int):
        self._adj[v].add(w)
        self._E += 1
        return self

    def adj(self, v) -> iter:
        return self._adj[v]

    def reverse(self):
        R = Digraph(self._V)
        for v in range(self._V):
            for w in self._adj:
                R.addEdge(w, v)
        return R


class DirectedDFS:
    def __init__(self, G: Digraph, sources: iter):
        self._marked = [False] * G.V
        [self.dfs(G, s) for s in sources if not self._marked[s]]
        # for s in sources:
        #     if not self._marked[s]:
        #         self.dfs(G, s)

    def dfs(self, G: Digraph, v: int):
        self._marked[v] = True
        #list(map(lambda x: self.dfs(G, x) if not self._marked[x] else None, G.adj(v)))
        [self.dfs(G, w) for w in G.adj(v) if not self._marked[w]]
        # for w in G.adj(v):
        #     if not self._marked[w]:
        #         self.dfs(G, w)

    def marked(self, v) -> bool:
        return self._marked[v]


class NFA:
    def __init__(self, regexp: str):
        ops = []
        self._re = regexp
        self._M = len(self._re)
        self._G = Digraph(self._M + 1)

        for i in range(self._M):
            lp = i
            if self._re[i] == '(' or self._re[i] == '|':
                ops.append(i)
            elif self._re[i] == ')':
                _or = ops.pop()
                if _or == '|':
                    lp = ops.pop()
                    self._G.addEdge(lp, i + 1).addEdge(_or, i)
                    # self._G.addEdge(_or, i)
                else:
                    lp = _or

            if i < self._M - 1 and self._re[i + 1] == '*':
                self._G.addEdge(lp, i + 1)
                self._G.addEdge(i + 1, lp)
            if self._re[i] in "(*)":
                self._G.addEdge(i, i + 1)

    def recognizes(self, txt: str) -> bool:

        dfs = DirectedDFS(self._G, [0])
        pc = Bag([v for v in range(self._G.V) if dfs.marked(v)])
        for i in range(len(txt)):
            match = Bag([v + 1 for v in pc if v < self._M and self._re[v] in '.' + txt[i]])
            print(match._items, "match")
            dfs = DirectedDFS(self._G, match)
            print(dfs._marked)
            pc = Bag([v for v in range(self._G.V) if dfs.marked(v)])
            print(pc._items)
        return self._M in pc


if __name__ == '__main__':
    regex = 'ab*c'
    nfa = NFA(regex)
    txts = ["c"]
    for txt in txts:
        if nfa.recognizes(txt):
            print(txt)
