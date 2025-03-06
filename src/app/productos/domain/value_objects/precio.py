from pydantic import BaseModel, field_validator

class Precio(BaseModel):
    valor: float

    @field_validator("valor")
    def validar_precio_positivo(cls, v):
        if v <= 0:
            raise ValueError("El precio debe ser mayor que 0")
        return v

    def __eq__(self, other):
        return isinstance(other, Precio) and self.valor == other.valor

    def __str__(self):
        return f"{self.valor:.2f}"