import json
from typing import List

from vendas_cli.core import produto_mais_vendido, total_por_produto, valor_total
from vendas_cli.models import Venda

FORMATOS_SUPORTADOS = ("text", "json")

def _formatar_moeda(valor: float) -> str:
    negativo = valor < 0
    valor_abs = abs(valor)
    inteiro = int(valor_abs)
    centavos = int(round((valor_abs - inteiro) * 100))
    if centavos == 100:
        inteiro += 1
        centavos = 0
    inteiro_str = f"{inteiro:,}".replace(",", ".")
    prefixo = "-" if negativo else ""
    return f"{prefixo}R$ {inteiro_str},{centavos:02d}"


def gerar_relatorio_texto(vendas: List[Venda]) -> str:
    totais = total_por_produto(vendas)
    mais = produto_mais_vendido(vendas)
    total = valor_total(vendas)

    linhas = ["Relatório de Vendas", ""]
    cabecalho = f"{'Produto':<20} {'Valor Total':>14}"
    linhas.append(cabecalho)
    linhas.append("-" * 36)

    for produto in sorted(totais):
        linhas.append(f"{produto:<20} {_formatar_moeda(totais[produto]):>14}")

    linhas.append("")
    linhas.append(f"Produto mais vendido: {mais or '-'}")
    linhas.append(f"Total geral: {_formatar_moeda(total)}")
    return "\n".join(linhas) + "\n"


def gerar_relatorio_json(vendas: List[Venda]) -> str:
    totais = total_por_produto(vendas)
    dados = {
        "produtos": {
            produto: round(valor, 2) for produto, valor in totais.items()
        },
        "produto_mais_vendido": produto_mais_vendido(vendas),
        "total_geral": round(valor_total(vendas), 2),
    }
    return json.dumps(dados, ensure_ascii=False, indent=2)
