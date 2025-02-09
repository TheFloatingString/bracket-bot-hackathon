from flask import Flask, Response
import cv2
from pyngrok import ngrok
import threading
import time

from src import motor_funcs

app = Flask(__name__)

# Global variable to store the camera object
camera = None

def get_camera():
    """Initialize or return existing camera object"""
    global camera
    if camera is None:
        camera = cv2.VideoCapture(0)
    return camera

def generate_frames():
    """Generate frames from camera"""
    camera = get_camera()
    while True:
        success, frame = camera.read()
        if not success:
            break
        
        # Encode frame as JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        
        # Yield the frame in byte format
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    """Serve a simple HTML page with the video stream"""
    return """
    <html>
        <head>
            <title>Video Stream</title>
        </head>
        <body>
            <h1>Live Video Stream</h1>
            <img src="/video_feed" width="640" height="480">
        </body>
    </html>
    """

@app.route('/video_feed')
def video_feed():
    """Route for streaming video"""
    return Response(generate_frames(),
                   mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/motor/forward")
def motor_forward():
    motor_funcs.motor_forward()
    return {"message": "forward"}

@app.route("/motor/backward")
def motor_backward():
    motor_funcs.motor_backward()
    return {"message": "backward"}

@app.route("/motor/left")
def motor_left():
    motor_funcs.motor_left()
    return {"message": "left"}

@app.route("/motor/right")
def motor_right():
    motor_funcs.motor_right()
    return {"message": "right"}

@app.route("/motor/stop")
def motor_stop():
    motor_funcs.motor_stop()
    return {"message": "stop"}

def cleanup():
    """Release camera resources"""
    global camera
    if camera is not None:
        camera.release()

if __name__ == '__main__':
    # Start ngrok tunnel
    # public_url = ngrok.connect(5000)
    # print(f' * Public URL: {public_url}')
    
    # Register cleanup function
    import atexit
    atexit.register(cleanup)
    
    # Run Flask app
    app.run(host='0.0.0.0', port=5000)
