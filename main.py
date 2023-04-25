from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def index():
    return {'data': "Blog List"}


@app.get('/blog/{id}/comments')
def show_blog_comments(id: int):
    return {
        'blog_id': id,
        'comments': "this blog has some comments."
    }


@app.get('/blog/{id}')
def show_blog(id: int):
    return {'blog': id}
