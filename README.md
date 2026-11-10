# atribuicao-de-papeis-grafos

Implementação em Python de **atribuição de papéis** (*role assignment* / *role coloring*) em grafos, com verificação computacional de resultados da minha tese de doutorado sobre **produto Cartesiano** e **prisma complementar**.

> Tese: MESQUITA NEIVA, F. *Atribuição de papéis em alguns produtos de grafos*. Doutorado em Ciência da Computação, Instituto de Informática, Universidade Federal de Goiás, 2022. Orientação: Diane Castonguay. Coorientação: Elisângela Silva Dias e Julliano Rosa Nascimento.
>
> Este código foi escrito agora, de forma independente, a partir das definições e dos enunciados da tese. Ele **verifica por computador** alguns resultados em grafos pequenos. Não é uma prova e não substitui as demonstrações do texto.

## A ideia

Uma **r-atribuição de papéis** de um grafo G é uma função sobrejetora p de V(G) em {0, ..., r-1} tal que dois vértices com o mesmo papel têm o mesmo conjunto de papéis na vizinhança: p(u) = p(v) implica p(N(u)) = p(N(v)). Em redes sociais, vértices com o mesmo papel desempenham funções equivalentes na rede.

Resultados da tese que este repositório confere:

| Resultado | Enunciado | Como é conferido |
|---|---|---|
| Teorema 4.1 | G □ H (G, H conexos não triviais) sempre tem uma 2-atribuição de papéis | A construção do teorema (rótulo alternado ao longo de uma ordem BFS de H) é validada em todos os produtos de grafos conexos de 2 a 4 vértices |
| Teorema 5.11 | O prisma complementar de G tem uma 2-atribuição de papéis se e somente se G não é P3 nem o complemento de P3 | Busca exaustiva em todos os grafos rotulados de 2 a 5 vértices |
| Proposição 2.2 | O prisma complementar é sempre conexo | Teste automático |

O problema r-ATRIBUIÇÃO DE PAPÉIS é NP-completo para o produto Cartesiano com r fixo >= 3 (Teorema 4.6 e seguintes). Por isso a busca exata do código (`find_role_assignment`) é exponencial e só serve para grafos pequenos.

## Arquivos

- `roles.py`: grafos, complemento, produto Cartesiano, prisma complementar, verificação de atribuição, grafo de papéis, busca exata e construção do Teorema 4.1.
- `verify.py`: verificação exaustiva em grafos pequenos.
- `test_roles.py`: 8 testes automáticos.

## Como executar

```bash
pip install -r requirements.txt
pytest
python verify.py
```

Saída esperada de `verify.py` (cerca de 3 segundos):

```text
Teorema 4.1: construção válida em 1849 produtos G□H (G, H conexos, 2 a 4 vértices)
Teorema 5.11, n=2: confere em 2 grafos (0 exceções P3/complemento)
Teorema 5.11, n=3: confere em 8 grafos (6 exceções P3/complemento)
Teorema 5.11, n=4: confere em 64 grafos (0 exceções P3/complemento)
Teorema 5.11, n=5: confere em 1024 grafos (0 exceções P3/complemento)
```

(As 6 exceções com n=3 são as 3 rotulações de P3 e as 3 do seu complemento.) O script imprime ainda, só como observação, os grafos com até 5 vértices cujo prisma complementar não tem 3-atribuição. Essa parte não foi comparada com a caracterização completa do Teorema 5.41.

## Uso rápido

```python
from roles import *

C5 = graph_from_edges(5, [(i, (i + 1) % 5) for i in range(5)])
P3 = graph_from_edges(3, [(0, 1), (1, 2)])

print(find_role_assignment(C5, 3))                       # uma 3-atribuição de C5
print(find_role_assignment(complementary_prism(P3), 2))  # None: P3 é exceção
```

## Limitações

- A verificação cobre só grafos com poucos vértices (explosão combinatória da busca exata).
- Não implementa o algoritmo de decisão em tempo linear do Teorema 5.45 (3-atribuição em prismas complementares) nem as reduções de NP-completude.
- Confere resultados, não os demonstra.

## Autora

Fernanda Neiva Mesquita. [Lattes](https://lattes.cnpq.br/3639678638834402)
# atribuicao-de-papeis-grafos
Atribuição de papéis (role assignment) em grafos, produto Cartesiano e prisma complementar: implementação e verificação computacional de resultados da minha tese
