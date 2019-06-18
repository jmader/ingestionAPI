import db_conn
import instrument
import nires
import hires
import deimos
import lris
import kcwi
import nirc2
import nirspec
import osiris
import esi
import mosfire
import weather

from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)

INSTRUMENTS = {
        'deimos':deimos.Deimos,
        'esi':esi.Esi,
        'hires':hires.Hires,
        'kcwi':kcwi.Kcwi,
        'lris':lris.Lris,
        'mosfire':mosfire.Mosfire,
        'nirc2':nirc2.Nirc2,
        'nires':nires.Nires,
        'nirspec':nirspec.Nirspec,
        'osiris':osiris.Osiris,
        'weather':weather.Weather
        }

@app.route('/tpx_status', methods=('GET','POST'))
def tpx_status():
    args = request.args
    instr = args['instr']
    date = args['date']
    statusType = args['statusType']
    status = args['status']
    response = ''
    print('instr: ', instr, '\ndate: ', date, '\nstatusType: ', statusType, '\nstatus: ', status)
    try:
        instrumentStatus = INSTRUMENTS[instr](instr, date, statusType, status)
    except Exception as e:
        print(e)
        print('error creating the object')
        response = 'error creating the object'
    else:
        try:
            response = instrumentStatus.types[instrumentStatus.statusType]()
        except Exception as e:
            print(e)
            print('error executing the status type')
            response = 'error executing the status type'
        else:
            print(response)
    return response

if __name__ == '__main__':
    host = '0.0.0.0'
    port = 50505
    debug = True
    app.run(host=host,port=port,debug=debug)
