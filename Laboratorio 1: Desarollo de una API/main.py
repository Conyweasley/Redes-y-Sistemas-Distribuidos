from flask import Flask, jsonify, request
import random
from proximo_feriado import NextHoliday

app = Flask(__name__)
peliculas = [
    {'id': 1, 'titulo': 'Indiana Jones', 'genero': 'Acción'},
    {'id': 2, 'titulo': 'Star Wars', 'genero': 'Acción'},
    {'id': 3, 'titulo': 'Interstellar', 'genero': 'Ciencia ficción'},
    {'id': 4, 'titulo': 'Jurassic Park', 'genero': 'Aventura'},
    {'id': 5, 'titulo': 'The Avengers', 'genero': 'Acción'},
    {'id': 6, 'titulo': 'Back to the Future', 'genero': 'Ciencia ficción'},
    {'id': 7, 'titulo': 'The Lord of the Rings', 'genero': 'Fantasía'},
    {'id': 8, 'titulo': 'The Dark Knight', 'genero': 'Acción'},
    {'id': 9, 'titulo': 'Inception', 'genero': 'Ciencia ficción'},
    {'id': 10, 'titulo': 'The Shawshank Redemption', 'genero': 'Drama'},
    {'id': 11, 'titulo': 'Pulp Fiction', 'genero': 'Crimen'},
    {'id': 12, 'titulo': 'Fight Club', 'genero': 'Drama'}
]


def obtener_peliculas():
    return jsonify(peliculas)


def obtener_pelicula(id):
    # Lógica para buscar la película por su ID y devolver sus detalles
    if id <= len(peliculas) and id > 0:
        pelicula_encontrada = peliculas[id-1]
        return jsonify(pelicula_encontrada), 200
    else:
        return 400


def agregar_pelicula():
    nueva_pelicula = {
        'id': obtener_nuevo_id(),
        'titulo': request.json['titulo'],
        'genero': request.json['genero']
    }
    peliculas.append(nueva_pelicula)
    print(peliculas)
    return jsonify(nueva_pelicula), 201


def actualizar_pelicula(id):
    # Lógica para buscar la película por su ID y actualizar sus detalles
    if id <= len(peliculas) and id > 0:
        peliculas[id-1]['titulo'] = request.json['titulo']
        peliculas[id-1]['genero'] = request.json['genero']

        pelicula_actualizada = peliculas[id-1]
        return jsonify(pelicula_actualizada), 200
    else:
        return 400


def eliminar_pelicula(id):
    # Lógica para buscar la película por su ID y eliminarla
    if id != len(peliculas):
        peliculas[id-1]['titulo'] = peliculas[-1]['titulo']
        peliculas[id-1]['genero'] = peliculas[-1]['genero']

    del peliculas[-1]
    return jsonify({'mensaje': 'Película eliminada correctamente'}), 200


def obtener_nuevo_id():
    if len(peliculas) > 0:
        ultimo_id = peliculas[-1]['id']
        return ultimo_id + 1
    else:
        return 1

def lista_por_genero(genero):
    listapelis = []
    for peli in peliculas:
        if peli['genero'] == genero:
           listapelis.append(peli)
    return jsonify(listapelis), 200

def buscar_pelicula(keyword):
    listapelis = []
    lowerkey = keyword.lower()
    for peli in peliculas:
        if lowerkey in peli['titulo'].lower():
            listapelis.append(peli)
    if listapelis == []:
        return 400
    return jsonify(listapelis), 200

def random_peli():
    peli_random = peliculas[random.randint(0, len(peliculas)-1)]
    return jsonify(peli_random), 200

def random_por_genero(genero):
    lista_random = []
    for peli in peliculas:
        if peli['genero'] == genero:
           lista_random.append(peli)
    if lista_random == []:
        return 400
    peli_random = lista_random[random.randint(0, len(lista_random)-1)]
    return jsonify(peli_random), 200

def feriado_cinefilo(genero):
    next_holiday = NextHoliday()
    next_holiday.fetch_holidays()
    holiday = next_holiday.holiday
    
    lista_random = []
    for peli in peliculas:
        if peli['genero'] == genero:
           lista_random.append(peli)
    if lista_random == []:
        return 400
    peli_random = lista_random[random.randint(0, len(lista_random)-1)]
    
    feriado_y_peli = [holiday, peli_random]

    return jsonify(feriado_y_peli), 200
    

app.add_url_rule('/peliculas', 'obtener_peliculas', obtener_peliculas, methods=['GET'])
app.add_url_rule('/peliculas/<int:id>', 'obtener_pelicula', obtener_pelicula, methods=['GET'])
app.add_url_rule('/peliculas', 'agregar_pelicula', agregar_pelicula, methods=['POST'])
app.add_url_rule('/peliculas/<int:id>', 'actualizar_pelicula', actualizar_pelicula, methods=['PUT'])
app.add_url_rule('/peliculas/<int:id>', 'eliminar_pelicula', eliminar_pelicula, methods=['DELETE'])
app.add_url_rule('/peliculas/<string:genero>', 'lista_por_genero', lista_por_genero, methods=['GET'])
app.add_url_rule('/peliculas/search/<string:keyword>', 'buscar_pelicula', buscar_pelicula, methods=['GET'])
app.add_url_rule('/peliculas/rand', 'random_peli', random_peli, methods=['GET'])
app.add_url_rule('/peliculas/rand/<string:genero>', 'random_por_genero', random_por_genero, methods=['GET'])
app.add_url_rule('/peliculas/rand/feriado/<string:genero>', 'feriado_cinefilo', feriado_cinefilo, methods=['GET'])

if __name__ == '__main__':
    app.run()
