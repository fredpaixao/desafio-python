import json
from pathlib import Path

from vendas_cli.cli import main

CSV_VALIDO = """produto,quantidade,preco_unitario,data
Camiseta,3,49.90,2025-01-15
Calça,2,99.90,2025-01-20
Tênis,1,199.90,2025-03-10
"""


def _escrever(tmp_path: Path) -> Path:
    arquivo = tmp_path / "vendas.csv"
    arquivo.write_text(CSV_VALIDO, encoding="utf-8")
    return arquivo


def test_main_formato_text(capsys, tmp_path):
    arquivo = _escrever(tmp_path)
    assert main([str(arquivo)]) == 0
    saida = capsys.readouterr().out
    assert "Relatório de Vendas" in saida
    assert "Total geral" in saida


def test_main_formato_json_com_filtro(capsys, tmp_path):
    arquivo = _escrever(tmp_path)
    assert main([str(arquivo), "--format", "json"]) == 0
    dados = json.loads(capsys.readouterr().out)
    assert dados["produto_mais_vendido"] == "Camiseta"

    assert main(
        [str(arquivo), "--format", "json", "--start", "2025-01-01", "--end", "2025-01-31"]
    ) == 0
    dados = json.loads(capsys.readouterr().out)
    assert dados["total_geral"] == 349.5


def test_main_arquivo_inexistente(caplog, tmp_path):
    assert main([str(tmp_path / "nao_existe.csv")]) == 1
    assert any("Arquivo não encontrado" in r.message for r in caplog.records)


def test_main_start_maior_que_end(caplog, tmp_path):
    arquivo = _escrever(tmp_path)
    assert main([str(arquivo), "--start", "2025-06-01", "--end", "2025-01-01"]) == 2
    assert any("posterior à data final" in r.message for r in caplog.records)


def test_main_periodo_sem_vendas(caplog, tmp_path):
    arquivo = _escrever(tmp_path)
    assert main([str(arquivo), "--start", "2026-01-01", "--end", "2026-12-31"]) == 0
    assert any("Nenhuma venda no período" in r.message for r in caplog.records)
