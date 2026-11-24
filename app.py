from flask import Flask, render_template, request, redirect

app = Flask(__name__)
items = []
next_id = 1


@app.route("/")
def index():
    q = request.args.get("q", "").strip().lower()
    kind = request.args.get("kind", "")
    shown = [
        i for i in items
        if (not q or q in i["name"].lower())
        and (not kind or i["kind"] == kind)
    ]
    return render_template("index.html", items=shown, q=q, kind=kind)

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


@app.route("/delete/<int:item_id>")
def delete(item_id):
    items[:] = [i for i in items if i["id"] != item_id]
    return redirect("/")


if __name__ == "__main__":
    app.run(port=5000)