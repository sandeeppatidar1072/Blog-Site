from flask import Flask, render_template, request, redirect
import os
import sqlite3

app = Flask(__name__)

# DATABASE CONNECTION
db = sqlite3.connect("database.db", check_same_thread=False)
cursor = db.cursor()


@app.route("/")
def home():
    return render_template("index.html")


# ADD BLOG
@app.route("/add-blog", methods=["GET", "POST"])
def add_blog():

    if request.method == "POST":

        title = request.form['title']
        description = request.form['description']
        image = request.files['image']

        upload_folder = os.path.join(app.root_path, "static", "uploads")

        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        file_path = os.path.join(upload_folder, image.filename)
        image.save(file_path)

        path = "static/uploads/" + image.filename

        sql = "INSERT INTO blogs (title, description, image) VALUES (?,?,?)"
        val = (title, description, path)

        cursor.execute(sql, val)
        db.commit()

        return redirect("/blogs")

    return render_template("add_blog.html")


# BLOG LIST
@app.route("/blogs")
def blogs():

    cursor.execute("SELECT * FROM blogs")
    data = cursor.fetchall()

    return render_template("blog_list.html", blogs=data)


# BLOG DETAIL
@app.route("/blog/<int:id>")
def blog_detail(id):

    cursor.execute("SELECT * FROM blogs WHERE id=?", (id,))
    blog = cursor.fetchone()

    return render_template("blog_detail.html", blog=blog)


# ADD PRODUCT
@app.route("/add-product", methods=["GET", "POST"])
def add_product():

    if request.method == "POST":

        name = request.form['name']
        price = request.form['price']
        description = request.form['description']
        image = request.files['image']

        upload_folder = os.path.join(app.root_path, "static", "uploads")

        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        file_path = os.path.join(upload_folder, image.filename)
        image.save(file_path)

        path = "static/uploads/" + image.filename

        sql = "INSERT INTO products (name,price,description,image) VALUES (?,?,?,?)"
        val = (name, price, description, path)

        cursor.execute(sql, val)
        db.commit()

        return redirect("/products")

    return render_template("add_product.html")


# PRODUCT LIST
@app.route("/products")
def products():

    cursor.execute("SELECT * FROM products")
    data = cursor.fetchall()

    return render_template("product_list.html", products=data)


# DELETE PRODUCT
@app.route("/delete-product/<int:id>")
def delete_product(id):

    cursor.execute("DELETE FROM products WHERE id=?", (id,))
    db.commit()

    return redirect("/products")


# EDIT PRODUCT
@app.route("/edit-product/<int:id>", methods=["GET", "POST"])
def edit_product(id):

    if request.method == "POST":

        name = request.form['name']
        price = request.form['price']
        description = request.form['description']

        sql = "UPDATE products SET name=?, price=?, description=? WHERE id=?"
        val = (name, price, description, id)

        cursor.execute(sql, val)
        db.commit()

        return redirect("/products")

    cursor.execute("SELECT * FROM products WHERE id=?", (id,))
    product = cursor.fetchone()

    return render_template("edit_product.html", product=product)


# ADD TO CART
@app.route("/add-to-cart/<int:id>")
def add_to_cart(id):

    cursor.execute("INSERT INTO cart (product_id, quantity) VALUES (?,1)", (id,))
    db.commit()

    return redirect("/cart")


# CART PAGE
@app.route("/cart")
def cart():

    query = """
    SELECT cart.id, products.name, products.price, products.image, cart.quantity
    FROM cart
    JOIN products ON cart.product_id = products.id
    """

    cursor.execute(query)
    items = cursor.fetchall()

    return render_template("cart.html", items=items)


# REMOVE FROM CART
@app.route("/remove-cart/<int:id>")
def remove_cart(id):

    cursor.execute("DELETE FROM cart WHERE id=?", (id,))
    db.commit()

    return redirect("/cart")


if __name__ == "__main__":
    app.run(debug=True)