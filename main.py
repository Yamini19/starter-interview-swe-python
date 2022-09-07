import datetime
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
    column_names=["Time","Name",'Value']
    
    try: 
        rawData = pd.DataFrame(pd.read_csv(io.StringIO(data.decode('utf-8')), names=column_names, sep= " ",index_col= False))
        rawData['Time'] = pd.to_datetime(rawData['Time'], unit='s')
        rawData.astype({'Value': 'float'}).dtypes
        type(rawData.shape)
    except pd.errors.ParserError as error:
        return jsonify({ "success":  'false'})
    except ValueError as error:
        return jsonify({ "success":  'false'})


    for ind in rawData.index:
        reading = Reading(rawData['Time'][ind], rawData['Name'][ind], rawData['Value'][ind])
        add_reading(reading)
    return jsonify({ "success": "true" })


@app.route("/data", methods=['GET'])
def get_data():
    # TODO: check what dates have been requested, and retrieve all data within the given range
    fromDate = request.args.get('from')
    toDate = request.args.get('to')

    if fromDate is None or fromDate == '""':
        return jsonify({ "message": "Please provide a valid From Date" })
    if toDate is None or toDate == '""':
        return jsonify({ "message": "Please provide a valid To Date" })
    
    try:
        fromDate= datetime.datetime.strptime(fromDate, '%Y-%m-%d').date()
        toDate= datetime.datetime.strptime(toDate, "%Y-%m-%d").date()
    except ValueError as error: 
        return jsonify({ "message":  str(error)})
    
    if toDate < fromDate:
        return jsonify({ "message": "parameter TO should be greater or equal to FROM" })

    response = []

    filteredReading = get_reading(fromDate, toDate)

    for reading in filteredReading: 
        response.append(Reading(str(reading.time),reading.name,reading.value).to_json())
    
    return jsonify(response)


if __name__ == "__main__":
    app.run()
