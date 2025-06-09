from flask import Flask, render_template, request
import mariadb
import datetime

app = Flask(__name__)

DB_CONFIG = {
    "host": "freeradiusIP",
    "port": 3306,
    "user": "readonlyuser",
    "password": "userpassword",
    "database": "radius"
}

def get_db_connection():
    return mariadb.connect(**DB_CONFIG)

@app.route('/', methods=['GET'])
def index():
    username = request.args.get('username', default=None, type=str)
    start_date = request.args.get('start_date', default=None, type=str)
    end_date = request.args.get('end_date', default=None, type=str)

    query = "SELECT id, username, reply, authdate FROM radpostauth"
    conditions = []
    params = []

    if username:
        conditions.append("username = ?")
        params.append(username)

    if start_date:
        conditions.append("authdate >= ?")
        params.append(start_date)

    if end_date:
        conditions.append("authdate <= ?")
        params.append(end_date)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " ORDER BY authdate DESC LIMIT 100"

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(query, params)
    rows = cur.fetchall()
    conn.close()

    return render_template('index.html', records=rows)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

