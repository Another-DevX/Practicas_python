import store
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get('/', response_class=HTMLResponse)
def get_list():
    return """
    <a href="contact">Boton</a>
    """

@app.get('/contact', response_class=HTMLResponse)
def get_list():
    return """
    <h1>Hola mundo version PYTHON</h1>
    <p>Ahora es 3 veces mas dificil hacer el hola mundo tristemente</p>
    """


def run():

    store.get_categories()

if __name__ == '__main__':
    run()