#Testing API With Postman
from flask import Flask, jsonify, request, make_response
from model import Data

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def hello():
    data = [{
        'nama': 'Ari Gunawan',
        'alamat': 'Kace',
        'usia': '24',
        'pesan': 'Semangat'
    }]
    return make_response(jsonify({'data': data}), 200)

@app.route('/mahasiswa', methods=['GET','POST','PUT','DELETE'])
def mahasiswa():
    try: 
        # Panggil class model database
        dt = Data()
        values = ()

        # Jika Method GET
        if request.method == 'GET':
            id_ = request.args.get("id")
            if id_:
                query = "SELECT * FROM datamahasiswa where id = %s "
                values = (id_,)
            else:
                query = "SELECT * FROM datamahasiswa"
            data = dt.get_data(query, values)

        # Jika Method POST
        elif request.method == 'POST':
            datainput = request.json
            nama = datainput['nama']
            alamat = datainput['alamat']
            usia = datainput['usia']

            query = "INSERT INTO datamahasiswa (nama, alamat, usia) values (%s,%s,%s) "                
            values = (nama, alamat, usia,)
            dt.insert_data(query, values)
            data = [{
                'pesan': 'berhasil menambah data'
            }]
        
        #Jika Method PUT
        elif request.method == 'PUT':
            query = "UPDATE datamahasiswa SET id = %s "
            datainput = request.json
            id_ = datainput['id']
            values += (id_,)

            if 'nama' in datainput:
                nama = datainput['nama']
                values += (nama, )
                query += ", nama = %s"
            if 'alamat' in datainput:
                alamat = datainput['alamat']
                values += (alamat, )
                query += ", alamat = %s"
            if 'usia' in datainput:
                usia = datainput['usia']
                values += (usia, )
                query += ", usia = %s"

            query += " where id = %s "
            values += (id_,)
            dt.insert_data(query, values)
            data = [{
                'pesan': 'berhasil mengubah data'
            }]

            # Selain itu adalah DELETE, bila ada method selain keempat ini maka dipastikan akan langsung error karena method tidak di assign.
        else:
                query = "DELETE FROM datamahasiswa where id = %s "
                id_ = request.args.get("id")
                values = (id_,)
                dt.insert_data(query, values)
                data = [{
                    'pesan': 'berhasil menghapus data'
                }]
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 400)
    return make_response(jsonify({'data': data}), 200)

app.run()
