from datetime import date
from typing import Dict, List, Optional

from vendas_cli.models import Venda


def filtrar_por_periodo(
    vendas: List[Venda],
    inicio: Optional[date] = None,
    fim: Optional[date] = None,
) -> List[Venda]:
    return [
        venda
        for venda in vendas
        if (inicio is None or venda.data >= inicio)
        and (fim is None or venda.data <= fim)
    ]


def total_por_produto(vendas: List[Venda]) -> Dict[str, float]:
    totais: Dict[str, float] = {}
    for venda in vendas:
        totais[venda.produto] = totais.get(venda.produto, 0.0) + venda.valor_total
    return totais


def valor_total(vendas: List[Venda]) -> float:
    return sum(v.valor_total for v in vendas)


def produto_mais_vendido(vendas: List[Venda]) -> Optional[str]:
    quantidades: Dict[str, int] = {}
    for venda in vendas:
        quantidades[venda.produto] = (
            quantidades.get(venda.produto, 0) + venda.quantidade
        )
    if not quantidades:
        return None
    return max(sorted(quantidades), key=quantidades.get)
