from flask import Flask, render_template, jsonify, request
import pickle
import pandas as pd

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route("/", methods=["GET"])
def get():
    return jsonify({
        "message": "GET method",
    }, 200)

@app.route("/<int:id>", methods=["GET", "POST"])
def post(id):
    if request.method == "GET":
        return render_template("main.html", id=id)
    else:
        return jsonify({
            "message": "POST method"
        }, 201)
    
@app.route("/create", methods = ["GET", "POST"])
def createPost():
    if request.method == "GET":
        return render_template("post_form.html")
    else:
        form = request.form
        title = form["name"]
        content = form["description"]
        id = form["id"]

        if not title or not content:
            return jsonify({
                "error": "Missing title or content"
            }, 402)
        print (title, content, id)
        return render_template("post.html", title=title, content=content, id=id)
    
@app.route("/predict", methods=["POST"])
def predictValue():
    with open('lr_model.pkl', 'rb') as file:
        model = pickle.load(file)
    
    cgpa = request.form["cgpa"]
    placement_exam_marks = request.form["placement_exam_marks"]
    name = request.form["name"]
    job = request.form["description"]

    cgpa = int(cgpa)
    placement_exam_marks = int(placement_exam_marks)

    val_to_predict = [[cgpa, placement_exam_marks]]
    df = pd.DataFrame(val_to_predict)
    prediction = model.predict(df.values.reshape(1, -1))
    prediction = float(prediction[0])
    print(prediction)
    formatted_prediction = '{:.2f}'.format(prediction)
    print("prediction is ", formatted_prediction)

    return render_template("show.html", prediction=prediction, name=name,job=job)
