from datetime import date

import pytest

from vendas_cli.core import (
    filtrar_por_periodo,
    produto_mais_vendido,
    total_por_produto,
    valor_total,
)
from vendas_cli.models import Venda


def _venda(produto, quantidade, preco, dia, mes=1, ano=2025):
    return Venda(produto, quantidade, preco, date(ano, mes, dia))


VENDAS = [
    _venda("Camiseta", 3, 49.90, 15),
    _venda("Calça", 2, 99.90, 20),
    _venda("Camiseta", 1, 49.90, 3, mes=2),
    _venda("Tênis", 1, 199.90, 10, mes=2),
]


def test_total_por_produto_e_valor_total():
    totais = total_por_produto(VENDAS)
    assert totais["Camiseta"] == pytest.approx(199.6)
    assert totais["Calça"] == pytest.approx(199.8)
    assert totais["Tênis"] == pytest.approx(199.9)
    assert valor_total(VENDAS) == pytest.approx(599.3)
    assert total_por_produto([]) == {}
    assert valor_total([]) == 0.0


def test_produto_mais_vendido():
    assert produto_mais_vendido(VENDAS) == "Camiseta"
    assert produto_mais_vendido([]) is None


@pytest.mark.parametrize(
    "inicio,fim,esperado",
    [
        (date(2025, 1, 1), date(2025, 1, 31), 2),
        (date(2025, 2, 1), None, 2),
        (None, date(2025, 1, 31), 2),
        (None, None, 4),
        (date(2025, 1, 15), date(2025, 2, 3), 3),
        (date(2026, 1, 1), date(2026, 12, 31), 0),
    ],
)
def test_filtrar_por_periodo(inicio, fim, esperado):
    filtradas = filtrar_por_periodo(VENDAS, inicio, fim)
    assert len(filtradas) == esperado
