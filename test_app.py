import json
from app import app
import pytest
import os
import tempfile

def test_index():
    client = app.test_client()
    res =client.get('/')
    assert res.status_code == 200
    expected = b'<p>Hello, World!</p>'
    assert expected == res.data


def test_sensor_data_post():
    client = app.test_client()
    res = client.post('/sensor',
        data=json.dumps({'sensor_data': 15}),
        content_type='application/json',
    )
    data = json.loads(res.get_data(as_text=True))
    data_result = {"result":"Added Successful"}
    assert res.status_code == 200
    assert data  == data_result
    assert data['result'] == "Added Successful"

def test_sensor_data_get_type_int():
    client = app.test_client()
    res = client.get('/sensor/int',content_type='application/json',)
    json_data = res.get_json()
    data = json.loads(json_data)
    assert res.status_code == 200
    assert data[0]["type"] == 'int'

def test_sensor_data_get_type_float():
    client = app.test_client()
    res = client.get('/sensor/float',content_type='application/json',)
    json_data = res.get_json()
    data = json.loads(json_data)
    assert res.status_code == 200
    assert data[0]["type"] == 'float'

def test_sensor_data_get_type_str():
    client = app.test_client()
    res = client.get('/sensor/str',content_type='application/json',)
    json_data = res.get_json()
    data = json.loads(json_data)
    assert res.status_code == 200
    assert data[0]["type"] == 'str'

def test_sensor_data_get_type_invalid():
    client = app.test_client()
    res = client.get('/sensor/test',content_type='application/json',)
    assert res.status_code == 404

def test_sensor_data_get_count_type_invalid():
    client = app.test_client()
    res = client.get('/sensor_count/15/test',content_type='application/json',)
    assert res.status_code == 404

def test_sensor_data_get_avg_type_invalid():
    client = app.test_client()
    res = client.get('/sensor_avg/test',content_type='application/json',)
    assert res.status_code == 404

def test_sensor_data_get_avg_type_int():
    client = app.test_client()
    res = client.get('/sensor_avg/int',content_type='application/json',)
    assert res.status_code == 200

def test_sensor_data_get_avg_type_float():
    client = app.test_client()
    res = client.get('/sensor_avg/float',content_type='application/json',)
    assert res.status_code == 200