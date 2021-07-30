from flask import Flask
from flask import jsonify
from flask import request
import json
from json import dumps
from bson import json_util
from flask_pymongo import PyMongo
from pymongo import message
from flask_caching import Cache


app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'restdb'
#app.config['MONGO_URI'] = 'mongodb://localhost:27017/restdb'
app.config['MONGO_URI'] = 'mongodb://test_mongodb:27017/restdb'
app.testing = True
cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})
cache.init_app(app)
mongo = PyMongo(app)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/sensor')
@cache.memoize(timeout=360)
def get_all_sensor_data():
    sensor_values = mongo.db.sensor_data.find()
    details_dicts = [sensor_value for sensor_value in sensor_values]
    details_json_string = json.dumps(details_dicts,default=json_util.default)
    return details_json_string
cached_comments = get_all_sensor_data()

@app.route('/sensor/<types>', methods=['GET'])
@cache.memoize(timeout=360)
def get_sensor_data_type(types):
    data = mongo.db.sensor_data
    if(types == 'int'):
        s = data.find({'type': types})
    elif(types == 'float'):
        s = data.find({'type': types})
    elif(types == 'str'):
        s = data.find({'type' : types})
    else:
        resp = jsonify({"error": "please pass a valid type(int, float, str) in the url type"})
        resp.status_code = 404
        return resp
    details_dicts = [sensor_value for sensor_value in s]
    details_json_string = json.dumps(details_dicts,default=json_util.default)
    return jsonify(details_json_string)

@app.route('/sensor_count/<value>/<types>', methods=['GET'])
@cache.memoize(timeout=360)
def get_count_sensor_data_type(value,types):
    data = mongo.db.sensor_data
    try:
        if(types == 'int'):
            s = data.find({'sensor_data' : int(value), 'type': types})
        elif(types == 'float'):
            s = data.find({'sensor_data' : float(value), 'type': types})
        elif(types == 'str'):
            s = data.find({'sensor_data' : value})
        else:
            resp = jsonify({"error": "please pass a valid type(int, float, str) in the url type"})
            resp.status_code = 404
            return resp
    except:
        resp = jsonify({"error": "please pass a valid type(int, float, str) in the url type"})
        resp.status_code = 404
        return resp
    return jsonify({'count' : s.count()})

@app.route('/sensor_avg/<types>', methods=['GET'])
@cache.memoize(timeout=360)
def get_avg_sensor_data_type(types):
    sensor_data = mongo.db.sensor_data
    try:
        if(types == 'int'):
            s = sensor_data.find({'type': types})
        elif(types == 'float'):
            s = sensor_data.find({'type': types})
        else:
            resp = jsonify({"error": "please pass a valid type(int, float, str) in the url type"})
            resp.status_code = 404
            return resp
        details_dicts = [sensor_value for sensor_value in s]
        details_json_string = json.dumps(details_dicts,default=json_util.default)
        values = json.loads(details_json_string)
        sensor_data_value = []
        sensordata_sum = 0
        sensordata_len = 0
        if types == 'int' or types == 'float':
            for i in values: 
                if i["type"] == types:
                    sensor_data_value.append(i["sensor_data"])
                    sensordata_sum += i["sensor_data"]
                    sensordata_len += 1
            # print(i)
        avg = sensordata_sum/sensordata_len
        return jsonify({"avg": avg})
    except:
        return jsonify({"error": "please pass a valid type(int, float, str) in the url type"})

@app.route('/sensor', methods=['POST'])
def add_sensor_data():
    sensor_data = mongo.db.sensor_data
#   name = request.json['name'] 
    data = request.json['sensor_data']
    data_type = str(type(data).__name__)
    print(data_type)
    if data and request.method == 'POST':
        data_id = sensor_data.insert_one({'sensor_data': data, "type": data_type})
        resp = jsonify({'result' : "Added Successful"})
        resp.status_code = 200
        return resp
    else:
        return not_found()


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found '+ request.url
    }
    resp = jsonify(message)
    return resp


if __name__=='__main__':
    app.run(host="0.0.0.0",port=5000)