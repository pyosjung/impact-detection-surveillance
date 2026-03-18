#server.py
from embeddedSystem import EmbeddedSystem
from flask import Flask, render_template, send_file, request, url_for, redirect
from flask_socketio import SocketIO, emit
import threading
import logging
from serverData import web_server_ip, web_server_port
from userData import users_login_info


# Flask 객체 생성 및 SocketIO 설정
app = Flask(__name__)
socketio = SocketIO(app, async_mode='threading')
system = EmbeddedSystem()
system.camera_module.load_video_list()


# Flask 에서 기본 설정된 werkzeug 로그 끄기
logging.getLogger('werkzeug').disabled = True


# Shock alert callback
def shock_alert_handler(data):
    socketio.emit('shock_alert', data)
system.set_shock_alert_callback(shock_alert_handler)

# video list update callback
def video_list_update_handler(data):
    socketio.emit('video_list_response', data)
system.set_video_list_update_callback(video_list_update_handler)


# Flask route handler
@app.route('/')
def home_page():
    return redirect(url_for('login_page'))

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/logout')
def logout_page():
    return redirect(url_for('login_page'))

@app.route('/index')
def index_page():
    return render_template('index.html')


# SocketIO event handler
@socketio.on('login')
def handle_login(data):
    username = data.get('username')
    system.send_mail.recipient_email = data.get('username')
    password = data.get('password')
    # print(f"Received login request: {username}, {password}")  # 로깅 추가
    
    if username in users_login_info and users_login_info[username] == password:
        print(f"User {username} logged in successfully.")  # 로깅 추가
        emit('login_response', {'success': True})
    else:
        print(f"Login failed for user {username}.")  # 로깅 추가
        emit('login_response', {'success': False, 'message': 'Invalid username or password'})

@socketio.on('connect')
def handle_connect():
    client_ip_addr = str(request.remote_addr)
    print(f"{client_ip_addr} Client connected")

@socketio.on('disconnect')
def handle_disconnect():
    client_ip_addr = str(request.remote_addr)
    print(f"{client_ip_addr} Client disconnected")

@socketio.on('start') 
def handle_start_event(json):
    client_ip_addr = str(request.remote_addr)
    if not system.active:
        system.active = True
        print(f"{client_ip_addr} {str(json['data'])}")
        emit('server_message', {'data': 'The server starts the system.'}, broadcast=True)

@socketio.on('stop') 
def handle_stop_event(json):
    client_ip_addr = str(request.remote_addr)
    if system.active:
        system.active = False
        print(f"{client_ip_addr} {str(json['data'])}")
        emit('server_message', {'data': 'The server stops the system.'}, broadcast=True)

@socketio.on('video_list_request')
def handle_video_list_request_event():
    emit('video_list_response', {'video_list': system.camera_module.video_list})

@app.route('/video/<video_name>')
def video(video_name):
    return send_file(system.camera_module.directory_path+video_name)

def run_server():
    socketio.run(app, host=web_server_ip , port=web_server_port)

def run_system():
    system.run()

if __name__ == "__main__":
    web_thread = threading.Thread(target=run_server)
    system_thread = threading.Thread(target=run_system)
    web_thread.start()
    system_thread.start()