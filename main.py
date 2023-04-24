from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def index():
    return {'data': "Blog List"}


@app.get('/blog/{id}')
def show_blog(id: int):
    return {'blog': id}
