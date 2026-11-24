from flask import Flask, jsonify, request, render_template
import redis

app = Flask(__name__)

# TODO: Configura la conexión a Redis 
#redis_client = redis_client es el objeto de conexión a Redis
redis_client = redis.StrictRedis(
    host='redis-practica-001.redis-practica.nti8eg.use1.cache.amazonaws.com',
    port=6379,
    decode_responses=True,
    ssl=True
)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/products', methods=['GET'])
def get_products():
    
    products = []
    # TODO: Obtener la lista de productos de Redis
    for key in redis_client.scan_iter('producto:*'):
        product = redis_client.hgetall(key)
        products.append(product)

    return jsonify(products)

@app.route('/cart', methods=['GET'])
def get_cart():
    
    cart_items = []
    # TODO: Obtener los elementos de la cesta desde Redis
    for key in redis_client.scan_iter('cesta:*'):
        item = redis_client.hgetall(key)
        cart_items.append(item)

    return jsonify(cart_items)

@app.route('/cart', methods=['POST'])
def add_to_cart():
    # TODO: Añadir un producto a la cesta en Redis con las verificaciones pertinentes
    data = request.get_json()
    product_id = data.get('product_id')
    product_key = "producto:" + str(product_id)

    if redis_client.exists(product_key):
        new_stock = redis_client.hincrby(product_key, "stock", -1)
        if new_stock < 0:
            redis_client.hincrby(product_key, "stock", 1)
            return jsonify({"error": "Sin stock"}), 400
        
        product = redis_client.hgetall(product_key)
        cart_key = "cesta:" + str(product_id)
        
        if not (redis_client.exists(cart_key)):
            redis_client.hset(cart_key, mapping={
                "id": product["id"],
                "name": product["name"],
                "price": product["price"],
                "quantity": 0
            })
        redis_client.hincrby(cart_key, "quantity", 1)

        return jsonify({
            "status": "added",
            "message": "Producto añadido a la cesta",
            "product": redis_client.hgetall(cart_key)
        })

    return jsonify({"error": "El producto no existe"}), 404


@app.route('/checkout', methods=['POST'])
def checkout():
    # TODO: Procesar la compra y limpiar la cesta en Redis
    purchased_items = []
    for key in redis_client.scan_iter("cesta:*"):
        item = redis_client.hgetall(key)
        purchased_items.append(item)
        redis_client.delete(key)
    
    return jsonify({
        "status": "completed",
        "message": "Compra completada",
        "products": purchased_items
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
