import csv
import logging
from datetime import datetime
from pathlib import Path
from typing import List

from vendas_cli.models import Venda

logger = logging.getLogger(__name__)

CAMPOS = ["produto", "quantidade", "preco_unitario", "data"]

class ErroCsv(Exception):
    """Erro ao ler ou validar um arquivo CSV de vendas."""


def ler_vendas(caminho: Path) -> List[Venda]:
    caminho = Path(caminho)
    if not caminho.is_file():
        raise ErroCsv(f"Arquivo não encontrado: {caminho}")

    vendas: List[Venda] = []
    try:
        with caminho.open(newline="", encoding="utf-8") as arquivo:
            leitor = csv.DictReader(arquivo)
            for numero, linha in enumerate(leitor, start=2):
                if all(
                    v is None or (isinstance(v, str) and not v.strip())
                    for v in linha.values()
                ):
                    continue
                if any(linha.get(c) is None for c in CAMPOS):
                    raise ErroCsv(f"{caminho}:{numero}: número de colunas incorreto")
                produto = linha["produto"].strip()
                if not produto:
                    raise ErroCsv(f"{caminho}:{numero}: produto vazio")
                try:
                    quantidade = int(linha["quantidade"])
                    preco = float(linha["preco_unitario"].replace(",", "."))
                    data = datetime.strptime(linha["data"], "%Y-%m-%d").date()
                except (ValueError, KeyError) as e:
                    raise ErroCsv(
                        f"{caminho}:{numero}: valor inválido ({e})"
                    ) from e
                if quantidade <= 0:
                    raise ErroCsv(f"{caminho}:{numero}: quantidade deve ser positiva")
                if preco < 0:
                    raise ErroCsv(
                        f"{caminho}:{numero}: preço unitário deve ser >= 0"
                    )
                vendas.append(
                    Venda(
                        produto=produto,
                        quantidade=quantidade,
                        preco_unitario=preco,
                        data=data,
                    )
                )
    except ErroCsv:
        raise
    except UnicodeDecodeError as e:
        raise ErroCsv(
            f"{caminho}: arquivo não está em UTF-8 ({e})"
        ) from e
    except OSError as e:
        raise ErroCsv(f"{caminho}: falha ao ler arquivo ({e})") from e

    if not vendas:
        raise ErroCsv(f"{caminho}: arquivo sem linhas de dados válidas")

    logger.info("Lidas %d vendas de %s", len(vendas), caminho)
    return vendas


def parsear_data(valor: str):
    return datetime.strptime(valor, "%Y-%m-%d").date()
