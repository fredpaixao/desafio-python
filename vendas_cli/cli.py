import argparse
import logging
import sys
from pathlib import Path
from typing import List, Optional

from vendas_cli.core import filtrar_por_periodo, produto_mais_vendido
from vendas_cli.output import (
    FORMATOS_SUPORTADOS,
    gerar_relatorio_json,
    gerar_relatorio_texto,
)
from vendas_cli.parser import ErroCsv, ler_vendas, parsear_data

logger = logging.getLogger(__name__)


def main(argv: Optional[List[str]] = None) -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    parser = argparse.ArgumentParser(
        prog="vendas-cli",
        description="Gera relatórios de vendas a partir de um arquivo CSV.",
    )
    parser.add_argument("arquivo", type=Path, help="caminho do arquivo CSV de vendas")
    parser.add_argument(
        "--format",
        dest="formato",
        choices=FORMATOS_SUPORTADOS,
        default="text",
        help="formato de saída do relatório (padrão: text)",
    )
    parser.add_argument(
        "--start", type=parsear_data, default=None, help="data inicial (YYYY-MM-DD)"
    )
    parser.add_argument(
        "--end", type=parsear_data, default=None, help="data final (YYYY-MM-DD)"
    )
    args = parser.parse_args(argv)

    if args.start and args.end and args.start > args.end:
        logger.error("Data inicial (%s) posterior à data final (%s)", args.start, args.end)
        return 2

    try:
        vendas = ler_vendas(args.arquivo)
    except ErroCsv as erro:
        logger.error("%s", erro)
        return 1

    vendas_filtradas = filtrar_por_periodo(vendas, args.start, args.end)

    if not vendas_filtradas:
        logger.warning("Nenhuma venda no período informado.")
        return 0

    if args.formato == "json":
        print(gerar_relatorio_json(vendas_filtradas))
    else:
        print(gerar_relatorio_texto(vendas_filtradas))

    logger.info(
        "Relatório gerado: %d vendas, formato=%s", len(vendas_filtradas), args.formato
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
