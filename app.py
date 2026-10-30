import os
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "wishlist-demo-key")

VERSION = os.environ.get("APP_VERSION", "v3").lower()
if VERSION not in ("v1", "v2", "v3"):
    VERSION = "v3"

# Simple in-memory storage for this demonstration.
wishlist = []
next_id = 1


@app.route("/", methods=["GET"])
def home():
    return render_template(
        "index.html",
        version=VERSION,
        items=wishlist if VERSION == "v3" else [],
        can_add=True,
        can_remove=VERSION in ("v2", "v3"),
        can_view=VERSION == "v3",
    )


@app.route("/add", methods=["POST"])
def add_item():
    global next_id

    item_name = request.form.get("item_name", "").strip()

    if not item_name:
        flash("Please enter an item name.", "error")
    elif len(item_name) > 100:
        flash("Item name must be 100 characters or fewer.", "error")
    else:
        wishlist.append({"id": next_id, "name": item_name})
        next_id += 1
        flash(f"Successfully added: {item_name}", "success")

    return redirect(url_for("home"))


@app.route("/remove", methods=["POST"])
def remove_item():
    if VERSION not in ("v2", "v3"):
        return "Remove is not available in V1.", 404

    item_name = request.form.get("item_name", "").strip()

    for item in wishlist:
        if item["name"].casefold() == item_name.casefold():
            wishlist.remove(item)
            flash(f"Successfully removed: {item_name}", "success")
            break
    else:
        flash("Item not found. Enter the exact saved item name.", "error")

    return redirect(url_for("home"))


@app.route("/health")
def health():
    return {"status": "healthy", "version": VERSION}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)