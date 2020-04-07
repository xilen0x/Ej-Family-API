from flask import Flask, render_template, jsonify, request
from flask_script import Manager
from flask_cors import CORS
from family import Family


app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['DEBUG'] = True
app.config['ENV'] = 'development'


manager = Manager(app)

fam = Family('Astorga')
@app.route('/')
def root():
    return render_template('index.htm')


@app.route('/family', methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/family/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def family(id=None):
    if request.method == 'GET':
        if id is not None:
            member = fam.get_member(id)  # obtengo todos los members segun id
            if member:
                return jsonify(member), 200
            else:
                return jsonify({"msg": "Not Found"}), 404
        else:
            members = fam.get_all_members()  # devuelve todos los members
            return jsonify(members), 200

    if request.method == 'POST':
        if not request.json.get("name"):
            return jsonify({"name":"Es requerido"}),422
        if not request.json.get("age"):
            return jsonify({"age":"Es requerido"}),422
        if not request.json.get("lucky_numbers"):
            return jsonify({"lucky_numbers":"Es requerido"}),422
            
        name = request.json.get("name")
        age = request.json.get("age")
        lucky_numbers = request.json.get("lucky_numbers")

        member = fam.add_member({
            "name": name,
            "age": age,
            "lucky_numbers": lucky_numbers
        })  # make a new member
        return jsonify(member), 201

    if request.method == 'PUT':
        return jsonify({"msg": "PUT"}), 200

    if request.method == 'DELETE':
        return jsonify({"msg": "DELETE"}), 200


if __name__ == '__main__':
    manager.run()
