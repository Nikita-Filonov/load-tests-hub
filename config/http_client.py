from pydantic import HttpUrl, BaseModel


class HTTPClientConfig(BaseModel):
    url: HttpUrl
    timeout: float = 120.0
    retries: int = 5
    retry_delay: float = 3.0

    @property
    def client_url(self) -> str:
        return str(self.url)
