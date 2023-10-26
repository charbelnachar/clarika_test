# clarika_test

# Ejercicio de API REST para Árbol

Este ejercicio consiste en implementar endpoints para una API REST que permita realizar diversas operaciones en un Árbol y sus nodos. El desarrollo de la API se llevará a cabo utilizando el framework Django.

## Contexto

El Árbol que se trabajará en la API deberá constar de un único nodo base, el cual no podrá ser eliminado y poseerá un valor asociado. Cada nodo del Árbol estará caracterizado por un campo denominado "valor", que tendrá una longitud máxima de 30 caracteres. El Árbol podrá tener como máximo 10 niveles de nodos. Al eliminar un nodo del Árbol, este deberá ser marcado como "borrado", y esta condición también aplicará a todos sus nodos hijos.

## Ejercicio

El candidato deberá implementar, al menos, tres de los siguientes endpoints de la API:

- Agregar un nuevo nodo al Árbol.
- Agregar un nuevo subárbol a un nodo específico del Árbol.
- Establecer el valor de un nodo particular del Árbol.
- Borrar un nodo del Árbol.
- Restablecer un nodo previamente borrado.
- Restablecer un nodo y todos sus nodos hijos previamente borrados.
- Restablecer el Árbol a su estado por defecto, con 4 niveles y 10 nodos.
- Obtener un subárbol a partir de un nodo especificado.
- Obtener un subárbol a partir de un nodo especificado, incluyendo todos sus nodos borrados.

## Entregable

El candidato deberá crear un repositorio en GitHub, GitLab o Bitbucket, seleccionando la plataforma que considere más adecuada. La solución desarrollada deberá ser subida al repositorio y deberá incluir pruebas funcionales que demuestren el correcto funcionamiento de los endpoints implementados. No se requiere implementar una base de datos en esta etapa, pero los tests deben ejecutarse exitosamente para demostrar la eficacia de los endpoints seleccionados. Se valorará especialmente la adopción del paradigma orientado a objetos en la solución propuesta.

## Requisitos

- Python 3.8 o superior
- Django 4.2 o superior

## Instalación

Clonar el repositorio:
```
git clone https://github.com/charbelnachar/clarika_test
```
Instalar las dependencias:
```
pip install -r requirements.txt
```

## Ejecución

Iniciar el servidor:
```
python manage.py runserver
```
Acceder a la API:
```
http://localhost:8000/
```

## Pruebas

Para ejecutar las pruebas, ejecutar el siguiente comando:

```
python manage.py test
```

## Objetivos

El objetivo de este ejercicio es evaluar las habilidades del candidato en el desarrollo de APIs REST con Python y Django. En particular, se valorará la capacidad del candidato para:

- Implementar endpoints RESTful de acuerdo con las especificaciones proporcionadas.
- Utilizar el paradigma orientado a objetos de manera efectiva.
- Escribir pruebas funcionales que demuestren el correcto funcionamiento de la API.

Buena suerte!




## Endpoint: Devolver Árbol

**URL**: `http://127.0.0.1:8000/devolver_arbol/?flag_deleted=true&node_id=1`

**Método**: `GET`

**Body**: No tiene

**Respuesta exitosa**:

Código: `200 OK`

Contenido:
```json
{
  "data_out": {
    "node_id": 1,
    "value": "root",
    "deleted": true,
    "children": [
      {
        "node_id": 2,
        "value": "asad",
        "deleted": true,
        "children": []
      }
    ]
  }
}

```


## Endpoint: Agregar Subárbol a Nodo

**URL**: `http://127.0.0.1:8000/agregar_sub_arbol_nodo/`

**Método**: `PUT`

**Body**:
```json
{
  "node_id": 1,
  "subtree": {
    "node_id": 1,
    "value": "root",
    "children": [
      {
        "node_id": 2,
        "value": "child 1",
        "children": [],
        "deleted": false
      },
      {
        "node_id": 3,
        "value": "child 2",
        "children": [
          {
            "node_id": 4,
            "value": "grandchild 1",
            "children": [],
            "deleted": false
          }
        ],
        "deleted": false
      }
    ],
    "deleted": false
  }
}
```
**Respuesta  exitosa**:

Código: `200 OK`

Contenido:
```json
{
  "success": {
    "node_id": 1,
    "value": "root",
    "deleted": false,
    "children": [
      {
        "node_id": 2,
        "value": "root",
        "deleted": false,
        "children": [
          {
            "node_id": 3,
            "value": "child 1",
            "deleted": false,
            "children": []
          },
          {
            "node_id": 4,
            "value": "child 2",
            "deleted": false,
            "children": [
              {
                "node_id": 5,
                "value": "grandchild 1",
                "deleted": false,
                "children": []
              }
            ]
          }
        ]
      }
    ]
  }
}

```


## Endpoint: Agregar Nodo con Valor

**URL**: `http://127.0.0.1:8000/agregar_nodo_valor/`

**Método**: `POST`

**Body**:
```json
{
	"node_value":"prueba",
	"parent_id":1
}
```
**Respuesta exitosa**:

Código: `200 OK`

Contenido:
```json
{
  "node_id": node_id
}

```

## Endpoint: Editar Valor de Nodo

**URL**: `http://127.0.0.1:8000/editar_valor_nodo/`

**Método**: `PUT`

**Body**:
```json
{
	"node_value":"cambio",
	"node_id":1
}
```
## Endpoint: Borrar Nodo

**URL**: `http://127.0.0.1:8000/borrar_nodo/`

**Método**: `DELETE`

**Body**:
```json
{
	"flag_children":true,
	"node_id":1
}
```
## Endpoint: Restaurar Nodo

**URL**: `http://127.0.0.1:8000/restaurar_nodo/`

**Método**: `PUT`

**Body**: No tiene

**Respuesta exitosa**:

Código: `200 OK`

Contenido:
```json
{
  "success": "El id: 1 fue restuarado"
}
```


