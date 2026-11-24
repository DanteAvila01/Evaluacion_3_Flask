from secrets import token_hex

from flask import Flask, abort, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = token_hex(32)


@app.get("/")
def inicio():
    return render_template("index.html")


@app.route("/ejercicio1", methods=["GET", "POST"])
def ejercicio1():
    if request.method == "GET":
        return render_template("ejercicio1.html")

    notas = [
        request.form.get(campo, type=int)
        for campo in ("nota1", "nota2", "nota3")
    ]
    asistencia = request.form.get("asistencia", type=int)

    if any(nota is None or not 10 <= nota <= 70 for nota in notas):
        return render_template(
            "ejercicio1.html", error="Ingresa tres notas enteras de 10 a 70."
        ), 400

    if asistencia is None or not 0 <= asistencia <= 100:
        return render_template(
            "ejercicio1.html", error="Ingresa una asistencia entera de 0 a 100."
        ), 400

    promedio = sum(notas) / len(notas)
    estado = "APROBADO" if promedio >= 40 and asistencia >= 75 else "REPROBADO"

    session["resultado_1"] = [
        ("Promedio", f"{promedio:.2f}".replace(".", ",")),
        ("Asistencia", f"{asistencia} %"),
        ("Estado", estado),
    ]
    return redirect(url_for("resultado", numero=1), code=303)


@app.route("/ejercicio2", methods=["GET", "POST"])
def ejercicio2():
    if request.method == "GET":
        return render_template("ejercicio2.html", nombres=["", "", ""])

    nombres = [
        request.form.get(campo, "").strip()
        for campo in ("nombre1", "nombre2", "nombre3")
    ]

    if not all(nombres) or len({nombre.casefold() for nombre in nombres}) != 3:
        return render_template(
            "ejercicio2.html",
            nombres=nombres,
            error="Ingresa tres nombres diferentes.",
        ), 400

    nombre_mas_largo = max(nombres, key=len)

    session["resultado_2"] = [
        ("Nombre con más caracteres", nombre_mas_largo),
        ("Cantidad de caracteres", len(nombre_mas_largo)),
    ]
    return redirect(url_for("resultado", numero=2), code=303)


@app.get("/resultado/<int:numero>")
def resultado(numero):
    if numero not in (1, 2):
        abort(404)

    datos = session.get(f"resultado_{numero}")
    origen = f"ejercicio{numero}"

    if datos is None:
        return redirect(url_for(origen))

    return render_template("resultado.html", origen=origen, datos=datos)


if __name__ == "__main__":
    app.run()
