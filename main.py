from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def index(limit: int = 10, published: bool = True):
    if published:
        return {'data': f"{limit} published blogs"}
    return {'data': f"{limit} blogs"}


@app.get('/blog/{id}/comments')
def show_blog_comments(id: int):
    return {
        'blog_id': id,
        'comments': "this blog has some comments."
    }


@app.get('/blog/unpublished')
def show_unpublished_blogs():
    return {'unpublished': [1, 2, 3, 4, 5]}


@app.get('/blog/{id}')
def show_blog(id: int):
    return {'blog': id}
