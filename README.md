# vendas-cli

Gerador de Relatório de Vendas Avançado — CLI em Python que processa um arquivo CSV de vendas e gera relatórios em texto (tabela) ou JSON, com filtro por intervalo de datas.

## Funcionalidades

- Leitura de CSV usando apenas bibliotecas padrão (`csv`, `argparse`, `logging`)
- Total de vendas por produto
- Valor total de todas as vendas
- Produto mais vendido
- Filtro opcional por intervalo de datas (`--start` / `--end`)
- Saída em texto formatado (tabela) ou JSON (`--format text|json`)
- Tipagem estática (`typing`) e estrutura modular
- Tratamento de erros e logs
- Testes unitários com pytest (cobertura ≥ 80%)

## Estrutura

```
desafio-python/
├── vendas_cli/
│   ├── __init__.py
│   ├── cli.py        # interface de linha de comando (argparse + logging)
│   ├── parser.py     # leitura e validação do CSV
│   ├── core.py       # cálculos e agregações
│   ├── output.py     # formatação de saída (text/JSON)
│   └── models.py     # modelo de dados
├── tests/            # testes unitários
├── pyproject.toml    # definição do pacote e comando vendas-cli
├── pytest.ini        # configuração do pytest + cobertura
└── vendas.csv        # arquivo de exemplo
```

## Formato do CSV

O arquivo deve ter o cabeçalho exato e as colunas nesta ordem:

```csv
produto,quantidade,preco_unitario,data
Camiseta,3,49.90,2025-01-15
Calça,2,99.90,2025-01-20
```

- `produto`: texto (não pode ser vazio)
- `quantidade`: inteiro positivo
- `preco_unitario`: número ≥ 0 (aceita vírgula ou ponto como decimal)
- `data`: formato `YYYY-MM-DD`

## Instalação

Requer Python 3.10+.

```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -e .
```

## Uso

```bash
# Relatório em texto (padrão)
vendas-cli vendas.csv

# Relatório em texto explícito
vendas-cli vendas.csv --format text

# Relatório em JSON
vendas-cli vendas.csv --format json

# Com filtro por intervalo de datas
vendas-cli vendas.csv --format json --start 2025-01-01 --end 2025-03-31

# Ajuda
vendas-cli --help
```

### Exemplo de saída (text)

Saída real com o `vendas.csv` de exemplo (exibida parcialmente):

```
Relatório de Vendas

Produto                 Valor Total
------------------------------------
Bermuda                   R$ 239,60
Blusa                     R$ 159,60
Boné                       R$ 89,70
Calça                     R$ 299,70
Camiseta                  R$ 349,30
...

Produto mais vendido: Camiseta
Total geral: R$ 4.164,00
```

### Exemplo de saída (JSON)

Saída real com o `vendas.csv` de exemplo (parcial):

```json
{
  "produtos": {
    "Camiseta": 349.3,
    "Calça": 299.7,
    "Tênis": 599.7
  },
  "produto_mais_vendido": "Camiseta",
  "total_geral": 4164.0
}
```

## Testes

```bash
pytest
```

A configuração (`pytest.ini`) já exige cobertura mínima de 80% e falha o teste se não for atingida.

## Códigos de saída

| Código | Significado                              |
|--------|------------------------------------------|
| 0      | Sucesso                                  |
| 1      | Erro ao ler/processar o arquivo CSV      |
| 2      | Argumentos inválidos (`--start` > `--end`) |

## Logs

A CLI usa o módulo `logging` e registra informações e erros no stderr com data/hora (ex.: arquivo processado, relatório gerado, erros de leitura).
