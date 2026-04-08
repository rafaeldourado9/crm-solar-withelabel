from pydantic import BaseModel


class GerarDocxRequest(BaseModel):
    variaveis: dict[str, str]


class GerarDocxResponse(BaseModel):
    filename: str
    content_type: str = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
