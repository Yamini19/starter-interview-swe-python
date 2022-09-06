from curses import raw
import io
import pandas as pd
from flask import Flask, jsonify, request

from db import Reading, add_reading, get_reading

app = Flask(__name__)

@app.route("/data", methods=['POST'])
def post_data():
    # TODO: parse incoming data, and save it to the database
    # data is of the form:
    #  {timestamp} {name} {value}

    data = request.data
    column_names=["TimeStamp","Name",'Value']
    rawData = pd.DataFrame(pd.read_csv(io.StringIO(data.decode('utf-8')), names=column_names, sep= " "))
    rawData['Time'] = pd.to_datetime(rawData['TimeStamp'], 
                                  unit='s')

    for ind in rawData.index:
        print(rawData['Time'][ind], rawData['Name'][ind], rawData['Value'][ind])
        reading = Reading(rawData['Time'][ind], rawData['Name'][ind], rawData['Value'][ind])
        add_reading(str(rawData['TimeStamp'][ind]), reading)
    return jsonify({ "success": "true" })


@app.route("/data", methods=['GET'])
def get_data():
    # TODO: check what dates have been requested, and retrieve all data within the given range
    get_reading("1649941817")
    return jsonify({ "success": "true" })


if __name__ == "__main__":
    app.run()
