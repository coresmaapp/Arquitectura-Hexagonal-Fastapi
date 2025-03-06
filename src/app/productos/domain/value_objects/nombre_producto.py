from pydantic import BaseModel, Field, field_validator

class NombreProducto(BaseModel):
    valor: str = Field(..., description="Nombre del producto")

    @field_validator("valor")
    def validar_nombre(cls, v):
        if not v.strip():
            raise ValueError("El nombre no puede estar vacío")
        if len(v) > 50:
            raise ValueError("El nombre no puede exceder los 50 caracteres")
        return v

    def __eq__(self, other):
        return isinstance(other, NombreProducto) and self.valor == other.valor

    def __str__(self):
        return self.valor
