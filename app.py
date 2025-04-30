from flask import Flask, render_template, request
import pandas as pd
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

dataframe = None

@app.route("/", methods=["GET", "POST"])
def index():
    global dataframe
    message = ""
    columns = []
    if request.method == "POST":
        if "file" in request.files:
            file = request.files["file"]
            if file.filename.endswith(".xlsx") or file.filename.endswith(".xls"):
                filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
                file.save(filepath)
                dataframe = pd.read_excel(filepath)
                message = f"Archivo '{file.filename}' cargado correctamente. Tiene {len(dataframe)} filas."
                columns = dataframe.columns.tolist()
            else:
                message = "Por favor subí un archivo Excel válido (.xlsx o .xls)."
        elif "consulta" in request.form and dataframe is not None:
            consulta = request.form["consulta"].lower()
            if "cuántos países" in consulta or "cuantos países" in consulta:
                for col in dataframe.columns:
                    if "país" in col.lower() or "pais" in col.lower():
                        paises = dataframe[col].nunique()
                        message = f"Hay {paises} países distintos en la columna '{col}'."
                        break
                else:
                    message = "No se encontró una columna que contenga países."
            else:
                message = "Consulta no reconocida aún. Solo se puede preguntar por países."
    return render_template("index.html", message=message, columns=columns)

if __name__ == "__main__":
    app.run(debug=True)
