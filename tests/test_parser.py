from pathlib import Path

import pytest

from vendas_cli.models import Venda
from vendas_cli.parser import ErroCsv, ler_vendas, parsear_data

CSV_VALIDO = """produto,quantidade,preco_unitario,data
Camiseta,3,49.90,2025-01-15
Calça,2,99.90,2025-01-20
Camiseta,1,49.90,2025-02-03
"""


def _escrever(tmp_path: Path, conteudo: str) -> Path:
    arquivo = tmp_path / "vendas.csv"
    arquivo.write_text(conteudo, encoding="utf-8")
    return arquivo


def test_ler_vendas_valido(tmp_path):
    vendas = ler_vendas(_escrever(tmp_path, CSV_VALIDO))
    assert len(vendas) == 3
    assert vendas[0] == Venda(
        produto="Camiseta",
        quantidade=3,
        preco_unitario=49.9,
        data=parsear_data("2025-01-15"),
    )


def test_ler_vendas_ignora_linhas_vazias(tmp_path):
    vendas = ler_vendas(_escrever(tmp_path, CSV_VALIDO + "\n\n  \n"))
    assert len(vendas) == 3


def test_ler_vendas_arquivo_inexistente(tmp_path):
    with pytest.raises(ErroCsv, match="Arquivo não encontrado"):
        ler_vendas(tmp_path / "nao_existe.csv")


def test_ler_vendas_cabecalho_invalido(tmp_path):
    arquivo = _escrever(tmp_path, "a,b,c,d\nX,1,2.0,2025-01-01\n")
    with pytest.raises(ErroCsv, match="colunas incorreto"):
        ler_vendas(arquivo)


@pytest.mark.parametrize(
    "linha,mensagem",
    [
        ("X,1,2.0", "número de colunas incorreto"),
        (",1,2.0,2025-01-01\n", "produto vazio"),
        ("X,abc,2.0,2025-01-01\n", "valor inválido"),
        ("X,1,foo,2025-01-01\n", "valor inválido"),
        ("X,1,2.0,31/01/2025\n", "valor inválido"),
        ("X,0,2.0,2025-01-01\n", "quantidade deve ser positiva"),
        ("X,1,-5.0,2025-01-01\n", "preço unitário deve ser >= 0"),
    ],
)
def test_ler_vendas_erros_de_validacao(tmp_path, linha, mensagem):
    cabecalho = "produto,quantidade,preco_unitario,data\n"
    arquivo = _escrever(tmp_path, cabecalho + linha)
    with pytest.raises(ErroCsv, match=mensagem):
        ler_vendas(arquivo)


def test_ler_vendas_sem_linhas_de_dados(tmp_path):
    arquivo = _escrever(tmp_path, "produto,quantidade,preco_unitario,data\n")
    with pytest.raises(ErroCsv, match="sem linhas de dados"):
        ler_vendas(arquivo)


def test_ler_vendas_encoding_invalido(tmp_path):
    arquivo = tmp_path / "vendas.csv"
    arquivo.write_bytes(b"\xff\xfe produto,quantidade,preco_unitario,data\n")
    with pytest.raises(ErroCsv, match="não está em UTF-8"):
        ler_vendas(arquivo)


def test_ler_vendas_falha_ao_ler(tmp_path, monkeypatch):
    arquivo = _escrever(tmp_path, CSV_VALIDO)

    def _abrir_falhando(*args, **kwargs):
        raise PermissionError("permissão negada")

    monkeypatch.setattr(Path, "open", _abrir_falhando)
    with pytest.raises(ErroCsv, match="falha ao ler arquivo"):
        ler_vendas(arquivo)


@pytest.mark.parametrize(
    "valor,esperado",
    [("2025-12-31", "2025-12-31"), ("2025-01-01", "2025-01-01")],
)
def test_parsear_data_valida(valor, esperado):
    assert parsear_data(valor).isoformat() == esperado


def test_parsear_data_invalida():
    with pytest.raises(ValueError):
        parsear_data("31/12/2025")
