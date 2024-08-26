from fastapi import FastAPI

from moldock.http_api.api import route

app = FastAPI(docs_url="/")
app.include_router(route)
