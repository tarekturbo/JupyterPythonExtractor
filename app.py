from flask import Flask ,render_template,url_for,request,send_file
import json
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "/"
def string_to_file(string):
    file_object = open('temporary_file.temporary', 'w')
    file_object.write(string)
    file = file_object
    file_object.flush()
    return file_object
@app.route("/")
def index():
    return render_template("index.html")
@app.route("/upload",methods=["POST"])
def upload():
    if "Jupyter" not in request.files:
        index()
    file = request.files["Jupyter"]
    if file.filename =="":
        index()
    if file.filename.split('.')[1]!="ipynb":
        return "File Extension Not allowed!"
    lines = json.loads(file.stream.read().decode('utf-8'))["cells"][0]["source"]
    code = ''.join([line for line in lines])
    if request.form.get("type") == "file":
        string_to_file(code)
        return send_file("temporary_file.temporary",as_attachment=True,attachment_filename=file.filename.split('.')[0]+".py")
    return code,{"Content-Type":"text/plain"}
if __name__ == '__main__':
    app.run(debug=True)