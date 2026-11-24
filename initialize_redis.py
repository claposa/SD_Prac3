import redis

def initialize_products(redis_client):
    #TODO: carga 10 productos a la base de datos en AWS.
    products = [
        {
            "id": "1",
            "name": "Laptop",
            "price": "899.99",
            "description": "Ordenador portatil",
            "stock": "15"
        },
        {
            "id": "2",
            "name": "Smartphone",
            "price": "599.99",
            "description": "Telefono movil",
            "stock": "20"
        },
        {
            "id": "3",
            "name": "Tablet",
            "price": "349.99",
            "description": "Tablet de 10 pulgadas",
            "stock": "12"
        },
        {
            "id": "4",
            "name": "Keyboard",
            "price": "49.99",
            "description": "Teclado mecanico",
            "stock": "30"
        },
        {
            "id": "5",
            "name": "Mouse",
            "price": "24.99",
            "description": "Raton inalambrico",
            "stock": "40"
        },
        {
            "id": "6",
            "name": "Monitor",
            "price": "199.99",
            "description": "Monitor Full HD",
            "stock": "10"
        },
        {
            "id": "7",
            "name": "Headphones",
            "price": "79.99",
            "description": "Auriculares bluetooth",
            "stock": "25"
        },
        {
            "id": "8",
            "name": "Webcam",
            "price": "59.99",
            "description": "Camara web HD",
            "stock": "18"
        },
        {
            "id": "9",
            "name": "Printer",
            "price": "129.99",
            "description": "Impresora multifuncion",
            "stock": "8"
        },
        {
            "id": "10",
            "name": "USB",
            "price": "12.99",
            "description": "Memoria USB de 64GB",
            "stock": "50"
        }
    ]

    for product in products:
        key = "producto:" + product["id"]
        redis_client.hset(key, mapping=product)


if __name__ == "__main__":
    try:
        #TODO: Configura la conexión a Redis 
        #redis_client = redis_client es el objeto de conexión a Redis
        redis_client = redis.StrictRedis(
            host='redis-practica-001.redis-practica.nti8eg.use1.cache.amazonaws.com:6379',
            port=6379,
            decode_responses=True
            ssl=True
        )

        redis_client.ping()
        
        # Inicializa los productos en Redis
        initialize_products(redis_client)
        print("¡Productos inicializados en Redis!")

    except Exception as e:
        print(f"Error al conectarse a Redis: {e}")
