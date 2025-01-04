import requests

# Obtener todas las películas
response = requests.get('http://localhost:5000/peliculas')
peliculas = response.json()
print("Películas existentes:")
for pelicula in peliculas:
    print(f"ID: {pelicula['id']}, Título: {pelicula['titulo']}, Género: {pelicula['genero']}")
print()

# Agregar una nueva película
nueva_pelicula = {
    'titulo': 'Pelicula de prueba',
    'genero': 'Acción'
}
response = requests.post('http://localhost:5000/peliculas', json=nueva_pelicula)
if response.status_code == 201:
    pelicula_agregada = response.json()
    print("Película agregada:")
    print(f"ID: {pelicula_agregada['id']}, Título: {pelicula_agregada['titulo']}, Género: {pelicula_agregada['genero']}")
else:
    print("Error al agregar la película.")
print()

# Obtener detalles de una película específica
id_pelicula = 1  # ID de la película a obtener
response = requests.get(f'http://localhost:5000/peliculas/{id_pelicula}')
if response.status_code == 200:
    pelicula = response.json()
    print("Detalles de la película:")
    print(f"ID: {pelicula['id']}, Título: {pelicula['titulo']}, Género: {pelicula['genero']}")
else:
    print("Error al obtener los detalles de la película.")
print()

# Actualizar los detalles de una película
id_pelicula = 1  # ID de la película a actualizar
datos_actualizados = {
    'titulo': 'Nuevo título',
    'genero': 'Comedia'
}
response = requests.put(f'http://localhost:5000/peliculas/{id_pelicula}', json=datos_actualizados)
if response.status_code == 200:
    pelicula_actualizada = response.json()
    print("Película actualizada:")
    print(f"ID: {pelicula_actualizada['id']}, Título: {pelicula_actualizada['titulo']}, Género: {pelicula_actualizada['genero']}")
else:
    print("Error al actualizar la película.")
print()

# Eliminar una película
id_pelicula = 8  # ID de la película a eliminar
response = requests.delete(f'http://localhost:5000/peliculas/{id_pelicula}')
if response.status_code == 200:
    print("Película eliminada correctamente.")
else:
    print("Error al eliminar la película.")
print()

id_pelicula = 1  # ID de la película a obtener
response = requests.get(f'http://localhost:5000/peliculas/{id_pelicula}')
if response.status_code == 200:
    pelicula = response.json()
    print("Detalles de la película:")
    print(f"ID: {pelicula['id']}, Título: {pelicula['titulo']}, Género: {pelicula['genero']}")
else:
    print("Error al obtener los detalles de la película.")
print()

genero_pelicula = 'Drama'
response = requests.get(f'http://localhost:5000/peliculas/{genero_pelicula}')
print("Peliculas del genero %s:" % genero_pelicula)
if response.status_code == 200:
    listapelis = response.json()
    for peli in listapelis:
        print(peli)
else:
    print("Error al obtener la lista de peliculas por genero")
print()
    
search_keyword = 'The'
response = requests.get(f'http://localhost:5000/peliculas/search/{search_keyword}')
print("Resultados de busqueda:")
if response.status_code == 200:
    listapelis = response.json()
    for peli in listapelis:
        print(peli)
else:
    print("Error al buscar la pelicula solicitada")
print()

response = requests.get('http://localhost:5000/peliculas/rand')
if response.status_code == 200:
    print(response.json())
else:
    print("Error")
print()

genero_pelicula = 'Comedia'
response = requests.get(f'http://localhost:5000/peliculas/rand/{genero_pelicula}')
if response.status_code == 200:
    peli_random = response.json()
    print("Peli random de %s:" % genero_pelicula)
    print(peli_random)
else:
    print("Error al obtener la pelicula")
print()

genero_pelicula = 'Drama'
response = requests.get(f'http://localhost:5000/peliculas/rand/feriado/{genero_pelicula}')
if response.status_code == 200:
    fyp = response.json()
    print(f"""El proximo feriado es el {fyp[0]['dia']}/{fyp[0]['mes']} con motivo {fyp[0]['motivo']}, \
te sugiero ver la pelicula de {fyp[1]['genero']}: {fyp[1]['titulo']}""" )
else:
    print("Error al obtener feriado/peli")
