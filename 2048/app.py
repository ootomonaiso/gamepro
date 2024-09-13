from flask import Flask, request, jsonify, render_template, redirect, url_for
from game2048 import Game2048
import mariadb
import logging
from sshtunnel import SSHTunnelForwarder
from automate import app as automate_app  # automate.py のブループリントをインポート

# Flask アプリケーションの初期化
app = Flask(__name__)
app.register_blueprint(automate_app)  # automate.py のブループリントを登録

game = Game2048()
connection = None
server = None

def create_ssh_tunnel():
    global server
    server = SSHTunnelForwarder(
        ('xs333002.xsrv.jp', 10022),
        ssh_username='xs333002',
        ssh_pkey=r'2048\xs333002 (1).key',
        remote_bind_address=('localhost', 3306),
        local_bind_address=('localhost', 10022)
    )
    server.start()
    logging.info("SSHトンネルが正常に開始されました")

def get_db_connection():
    global connection
    if connection is None:
        try:
            connection = mariadb.connect(
                host='localhost',
                port=10022,
                user='xs333002_root',
                password='Stemask1234',
                database='xs333002_stem'
            )
        except mariadb.Error as e:
            logging.error(f"Database connection error: {e}")
            raise
    return connection

@app.route('/')
def index():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        query = "SELECT username, score FROM game_results ORDER BY score DESC LIMIT 10"
        cursor.execute(query)
        rankings = cursor.fetchall()
        cursor.close()
    except mariadb.Error as e:
        logging.error(f"Database error: {e}")
        rankings = []

    return render_template('index.html', rankings=rankings)

@app.route('/game')
def game_page():
    return render_template('game.html')

@app.route('/api/move', methods=['POST'])
def move():
    direction = request.json.get('direction')
    if direction in ['up', 'down', 'left', 'right']:
        game.move(direction)
        if game.game_over:
            return jsonify({'game_over': True, 'state': game.get_state()})
        return jsonify({'game_over': False, 'state': game.get_state()})
    return jsonify({'error': 'Invalid direction'}), 400

@app.route('/api/reset', methods=['POST'])
def reset():
    global game
    game = Game2048()
    return jsonify(game.get_state())

@app.route('/result')
def result():
    score = request.args.get('score', 0)
    return render_template('result.html', score=score)

@app.route('/save_result', methods=['POST'])
def save_result():
    username = request.form.get('username')
    score = request.form.get('score')
    
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = "INSERT INTO game_results (username, score) VALUES (%s, %s)"
        cursor.execute(query, (username, score))
        connection.commit()
        cursor.close()
        return redirect(url_for('index'))
    except mariadb.Error as e:
        logging.error(f"Database error: {e}")
        return "データベースエラー", 500

if __name__ == '__main__':
    create_ssh_tunnel()
    try:
        app.run(debug=True)
    finally:
        if server:
            server.stop()
            logging.info("SSHトンネルが停止しました")
