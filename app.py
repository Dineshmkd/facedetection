from flask import Flask, render_template, request, redirect, url_for, Response, jsonify
import cv2
import face_recognition_utils
import database

app = Flask(__name__)
database.init_db() 
camera_active = False
video_capture = None

@app.route('/')
def home():
    values = request.args.getlist('values')
    if values:
        return render_template('index.html', values=values)
    
    return render_template('index.html')

@app.route('/navigateRegister')
def navigateRegister():
    return render_template('register.html')

@app.route('/navigateDetails')
def navigateDetails():
    return render_template('details.html')

def generate_frames():
    global video_capture, camera_active
    video_capture = cv2.VideoCapture(0)
    
    while camera_active:
        success, frame = video_capture.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')   

    video_capture.release()

@app.route('/video_feed')    
def video_feed():
    global camera_active

    camera_active = True
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/stop_camera', methods=['POST'])
def stop_camera():
    global camera_active  
    camera_active = False
     # Close the camera
    return jsonify({'message': 'Camera stopped'})


@app.route('/register', methods=['POST'])
def register():
    print("Inside register")
    name = request.form['name']
    roll_number = request.form['roll_number']
    image_path = face_recognition_utils.capture_image(roll_number, name)
    
    if image_path:
        value = face_recognition_utils.encode_faces()
        if value == 'Registration successfull.':
            database.add_student(name, roll_number, image_path)
        
        return jsonify({"message": value})
        
    return jsonify({"message": ''})

@app.route('/attendance', methods=['GET'])
def attendance():
    print("inside attandenace")
    cam = cv2.VideoCapture(0)
    ret, frame = cam.read()
    cam.release()
    
    if ret:
        student_name = face_recognition_utils.recognize_face(frame)
        if student_name and student_name != "Unknown":
            print(student_name)
            values = database.get_student_id_by_name(student_name.split("_")[0])
            database.mark_attendance(student_name.split("_")[0])
            return jsonify({"values": values})
    return jsonify({"values": []}) 

if __name__ == '__main__':
    app.run(debug=True)
