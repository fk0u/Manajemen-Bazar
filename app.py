from flask import Flask, render_template, request, jsonify
from flask_frozen import Freezer

app = Flask(__name__)
freezer = Freezer(app)

financial_data = []
transaction_id_counter = 1

@app.route('/')
def index():
    return render_template('index.html', financial_data=financial_data)

@app.route('/tambah_transaksi', methods=['POST'])
def tambah_transaksi():
    global transaction_id_counter
    data = request.get_json()
    data['id'] = transaction_id_counter
    transaction_id_counter += 1
    financial_data.append(data)
    return jsonify(success=True)

@app.route('/get_data_keuangan')
def get_data_keuangan():
    return jsonify(financial_data)

@app.route('/hapus_transaksi/<int:transaction_id>', methods=['DELETE'])
def hapus_transaksi(transaction_id):
    global financial_data
    financial_data = [data for data in financial_data if data.get('id') != transaction_id]
    return jsonify(success=True)

@freezer.register_generator
def hapus_transaksi():
    for data in financial_data:
        yield {'transaction_id': data['id']}

if __name__ == '__main__':
    freezer.freeze()
    app.run(debug=True)
