from flask import Flask, render_template, request, redirect, url_for, session
from db_config import get_db_connection
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'static/uploads/'

model = load_model('model/hackrbitmodel.keras')
classification_names = ["DirtyFloor", "OverflowingDustbins", "TrashPresence", "WaterLeaks"]
input_shape = (224, 224, 3)


# Home page
@app.route('/')
def home():
    return render_template('index.html')

# Signup route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = 'user'
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
                       (username, password, role))
        conn.commit()
        conn.close()
        return redirect(url_for('home'))
    return render_template('register.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['user_id'] = user['id']
            session['role'] = user['role']
            return redirect(url_for('dashboard'))
        else:
            return "Invalid Credentials"
    return render_template('login.html')


# Dashboard
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('home'))
    if session['role'] == 'admin':
        return redirect(url_for('admin_dashboard'))
    else:
        return render_template('user_dashboard.html')

# Prediction route for users
@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return redirect(url_for('dashboard'))

    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('dashboard'))

    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        img = image.load_img(filepath, target_size=input_shape[:2])
        img_array = image.img_to_array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        predictions = model.predict(img_array)
        predicted_index = np.argmax(predictions, axis=1)[0]
        predicted_class = classification_names[predicted_index]
        predicted_prob = predictions[0][predicted_index] * 100

        if predicted_prob > 75:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO complaints (user_id, image_path, predicted_class, probability) VALUES (%s, %s, %s, %s)",
                           (session['user_id'], filepath, predicted_class, predicted_prob))
            conn.commit()
            conn.close()

        return render_template('user_dashboard.html',
                               prediction=predicted_class,
                               probability=f"{predicted_prob:.2f}%",
                               image_path=filepath)

# Admin dashboard
@app.route('/admin')
def admin_dashboard():
    if 'user_id' not in session or session['role'] != 'admin':
        return redirect(url_for('home'))
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT c.*, u.username FROM complaints c JOIN users u ON c.user_id = u.id WHERE status='Pending'")
    complaints = cursor.fetchall()
    conn.close()
    return render_template('admin_dashboard.html', complaints=complaints)

if __name__ == '__main__':
    app.run(debug=True)
