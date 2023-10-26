# clarika_test

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


