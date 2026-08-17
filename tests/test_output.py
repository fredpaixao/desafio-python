import json
from datetime import date

from vendas_cli.models import Venda
from vendas_cli.output import (
    FORMATOS_SUPORTADOS,
    _formatar_moeda,
    gerar_relatorio_json,
    gerar_relatorio_texto,
)

VENDAS = [
    Venda("Camiseta", 3, 49.90, date(2025, 1, 15)),
    Venda("Calça", 2, 99.90, date(2025, 1, 15)),
    Venda("Camiseta", 1, 49.90, date(2025, 1, 15)),
]


def test_gerar_relatorio_texto():
    texto = gerar_relatorio_texto(VENDAS)
    assert "Relatório de Vendas" in texto
    assert "Camiseta" in texto and "R$ 199,60" in texto
    assert "Calça" in texto and "R$ 199,80" in texto
    assert "Produto mais vendido: Camiseta" in texto
    assert "Total geral: R$ 399,40" in texto


def test_gerar_relatorio_json():
    dados = json.loads(gerar_relatorio_json(VENDAS))
    assert dados["produto_mais_vendido"] == "Camiseta"
    assert dados["total_geral"] == 399.4
    assert dados["produtos"] == {"Camiseta": 199.6, "Calça": 199.8}
    assert "Calça" in gerar_relatorio_json(VENDAS)


def test_gerar_relatorio_vazio():
    assert json.loads(gerar_relatorio_json([]))["produto_mais_vendido"] is None
    assert "Produto mais vendido: -" in gerar_relatorio_texto([])


def test_formatos_suportados_e_moeda():
    assert FORMATOS_SUPORTADOS == ("text", "json")
    assert _formatar_moeda(0.999) == "R$ 1,00"
    assert _formatar_moeda(1.999) == "R$ 2,00"
