from pydantic import BaseModel


class Throughput(BaseModel):
    value: int
