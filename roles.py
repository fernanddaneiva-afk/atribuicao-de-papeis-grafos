"""Atribuição de papéis (role assignment) em grafos e em alguns produtos de grafos.

Implementação didática e independente, com verificação computacional em grafos
pequenos, dos conceitos e resultados da tese:
  MESQUITA NEIVA, F. Atribuição de papéis em alguns produtos de grafos.
  Tese (Doutorado em Ciência da Computação), Instituto de Informática, UFG, 2022.

Definição (Cap. 3): p : V(G) -> {0..r-1} sobrejetora é uma r-atribuição de papéis se,
para quaisquer u, v com p(u) = p(v), vale p(N(u)) = p(N(v)) (Lema 3.3).
Grafos são dicionários {vértice: conjunto de vizinhos}, simples e sem laços.
"""
from itertools import product


# ----------------------------------------------------------------- construção de grafos
def graph_from_edges(n, edges):
    adj = {v: set() for v in range(n)}
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    return adj


def complement(adj):
    vs = set(adj)
    return {v: vs - adj[v] - {v} for v in adj}


def cartesian_product(g, h):
    """G □ H: (u,v) ~ (u',v') se (u=u' e vv' em H) ou (v=v' e uu' em G)."""
    adj = {(u, v): set() for u in g for v in h}
    for (u, v) in adj:
        adj[(u, v)] |= {(u2, v) for u2 in g[u]}
        adj[(u, v)] |= {(u, v2) for v2 in h[v]}
    return adj


def complementary_prism(adj):
    """G e o complemento de G (cópia) ligados por um emparelhamento perfeito v -- v'."""
    comp = complement(adj)
    out = {}
    for v in adj:
        out[("g", v)] = {("g", u) for u in adj[v]} | {("c", v)}
        out[("c", v)] = {("c", u) for u in comp[v]} | {("g", v)}
    return out


def is_connected(adj):
    if not adj:
        return True
    start = next(iter(adj))
    seen, stack = {start}, [start]
    while stack:
        v = stack.pop()
        for u in adj[v] - seen:
            seen.add(u)
            stack.append(u)
    return len(seen) == len(adj)


# ----------------------------------------------------------------- atribuição de papéis
def is_role_assignment(adj, p, r):
    """p é uma r-atribuição de papéis? (sobrejetora e mesma vizinhança de papéis)."""
    if set(p.values()) != set(range(r)):
        return False
    seen = {}
    for v in adj:
        roles = frozenset(p[u] for u in adj[v])
        if seen.setdefault(p[v], roles) != roles:
            return False
    return True


def role_graph(adj, p):
    """Grafo de papéis (Def. 3.2): arestas (com laços) entre papéis de vértices adjacentes."""
    return {frozenset((p[u], p[v])) for u in adj for v in adj[u]}


def find_role_assignment(adj, r):
    """Busca exaustiva (exponencial) de uma r-atribuição. Só para grafos pequenos:
    o problema é NP-completo para o produto Cartesiano já com r = 3."""
    vs = sorted(adj, key=repr)
    for labels in product(range(r), repeat=len(vs)):
        p = dict(zip(vs, labels))
        if is_role_assignment(adj, p, r):
            return p
    return None


def two_role_cartesian(g, h):
    """2-atribuição construtiva para G □ H, G e H conexos e não triviais (Teorema 4.1).

    Ordena H de modo que cada vértice (exceto o primeiro) tenha um vizinho anterior
    (BFS) e alterna o rótulo em relação a esse vizinho: p(u, v) = l(v)."""
    assert len(g) > 1 and len(h) > 1 and is_connected(g) and is_connected(h)
    root = min(h, key=repr)
    label, order = {root: 0}, [root]
    for v in order:
        for u in sorted(h[v], key=repr):
            if u not in label:
                label[u] = 1 - label[v]
                order.append(u)
    return {(u, v): label[v] for u in g for v in h}
