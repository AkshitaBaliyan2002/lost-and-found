from flask import Flask, render_template, request, redirect

app = Flask(__name__)
items = []
next_id = 1


@app.route("/")
@app.route("/")
def index():
    q = request.args.get("q", "").strip().lower()
    shown = [i for i in items if q in i["name"].lower()] if q else items
    return render_template("index.html", items=shown, q=q)


@app.route("/add", methods=["POST"])
def add():
    global next_id
    name = request.form.get("name", "").strip()
    place = request.form.get("place", "").strip()
    kind = request.form.get("kind", "Lost")
    if name and kind in ("Lost", "Found"):
        items.append({
            "id": next_id,
            "name": name,
            "place": place,
            "kind": kind,
            "claimed": False,
        })
        next_id += 1
    return redirect("/")

@app.route("/claim/<int:item_id>")
def claim(item_id):
    for i in items:
        if i["id"] == item_id:
            i["claimed"] = True
    return redirect("/")



if __name__ == "__main__":
    app.run(port=5000)