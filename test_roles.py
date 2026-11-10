from roles import (cartesian_product, complement, complementary_prism,
                   find_role_assignment, graph_from_edges, is_connected,
                   is_role_assignment, role_graph, two_role_cartesian)

P3 = graph_from_edges(3, [(0, 1), (1, 2)])
C5 = graph_from_edges(5, [(i, (i + 1) % 5) for i in range(5)])
K2 = graph_from_edges(2, [(0, 1)])


def test_ciclo_5_tem_3_papeis():
    # Ex. da tese: C5 tem 3-atribuição de papéis (a busca encontra uma)
    p = find_role_assignment(C5, 3)
    assert p is not None and is_role_assignment(C5, p, 3)


def test_toda_atribuicao_n_vertices():
    # Proposição 3.4: G de ordem n tem n-atribuição (cada vértice com papel próprio)
    assert is_role_assignment(P3, {0: 0, 1: 1, 2: 2}, 3)


def test_atribuicao_invalida():
    assert not is_role_assignment(P3, {0: 0, 1: 0, 2: 1}, 2)


def test_grafo_de_papeis():
    p = {0: 0, 1: 1, 2: 0}
    assert is_role_assignment(P3, p, 2)
    assert role_graph(P3, p) == {frozenset((0, 1))}


def test_complemento_involutivo():
    assert complement(complement(C5)) == C5


def test_prisma_complementar_conexo():
    # Proposição 2.2
    assert is_connected(complementary_prism(P3))
    assert len(complementary_prism(C5)) == 10


def test_prisma_de_p3_sem_2_atribuicao():
    # Teorema 5.11: P3 é exceção
    assert find_role_assignment(complementary_prism(P3), 2) is None


def test_produto_cartesiano_2_atribuicao():
    # Teorema 4.1
    prod = cartesian_product(C5, P3)
    assert is_role_assignment(prod, two_role_cartesian(C5, P3), 2)
    prod2 = cartesian_product(K2, K2)
    assert is_role_assignment(prod2, two_role_cartesian(K2, K2), 2)
