from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class Venda:

    produto: str
    quantidade: int
    preco_unitario: float
    data: date

    @property
    def valor_total(self) -> float:
        return self.quantidade * self.preco_unitario
