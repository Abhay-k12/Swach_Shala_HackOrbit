from flask import Flask, flash, render_template, request, redirect, url_for, session
from db_config import get_db_connection
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os
from flask import send_file
from xhtml2pdf import pisa
from io import BytesIO
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'static/uploads/'

model = load_model('model/hackrbitmodel.keras')
classification_names = ["Dirty Floor", "Overflowing Dustbins", "Trash Presence", "WaterLeaks"]
input_shape = (224, 224, 3)


# Home page
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/logout')
def logout():
    session.clear()  # Clearing all the session data
    flash('You have been logged out successfully.', 'info')  # showing flash message
    return redirect(url_for('home'))  # Redirecting to home route


# Registration Request page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        institution_name = request.form['institution_name']
        email = request.form['email']
        address = request.form['address']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO registration_requests (institution_name, email, address, password) VALUES (%s, %s, %s, %s)",
                       (institution_name, email, address, password))
        conn.commit()
        conn.close()
        return redirect(url_for('home'))
    return render_template('register.html')


# Login page (for admin & approved schools)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['user_id'] = user['id']
            session['role'] = user['role']
            session['institution_name'] = user['institution_name']
            session['email'] = user['email']
            return redirect(url_for('dashboard'))
        else:
            return "Invalid Credentials"
    return render_template('login.html')


# Dashboard Routing
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('home'))
    if session['role'] == 'admin':
        return redirect(url_for('admin_dashboard'))
    else:
        return redirect(url_for('school_dashboard'))


# School Dashboard
@app.route('/school')
def school_dashboard():
    if 'user_id' not in session or session['role'] != 'school':
        return redirect(url_for('home'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM complaints WHERE user_id=%s", (session['user_id'],))
    complaints = cursor.fetchall()
    conn.close()
    return render_template('school_dashboard.html', complaints=complaints)


# Admin Dashboard
@app.route('/admin')
def admin_dashboard():
    if 'user_id' not in session or session['role'] != 'admin':
        return redirect(url_for('home'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM registration_requests WHERE status='Pending'")
    requests_data = cursor.fetchall()

    # Fetch all pending complaints
    cursor.execute("""
        SELECT c.*, u.institution_name 
        FROM complaints c 
        JOIN users u ON c.user_id = u.id 
        WHERE c.status='Pending'
        ORDER BY u.institution_name
    """)
    complaints_data = cursor.fetchall()
    conn.close()

    # Group complaints by school
    reports = {}
    for comp in complaints_data:
        school = comp['institution_name']
        if school not in reports:
            reports[school] = []
        reports[school].append(comp)

    return render_template('admin_dashboard.html', requests=requests_data, reports=reports)


# Approve Registration Request
@app.route('/approve/<int:request_id>')
def approve_request(request_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM registration_requests WHERE id=%s", (request_id,))
    request_data = cursor.fetchone()

    cursor.execute("INSERT INTO users (institution_name, email, address, password, role) VALUES (%s, %s, %s, %s, 'school')",
                   (request_data[1], request_data[2], request_data[3], request_data[4]))

    cursor.execute("UPDATE registration_requests SET status='Approved' WHERE id=%s", (request_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin_dashboard'))


# Reject Registration Request
@app.route('/reject/<int:request_id>')
def reject_request(request_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE registration_requests SET status='Rejected' WHERE id=%s", (request_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin_dashboard'))


# Prediction route for schools
@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return redirect(url_for('school_dashboard'))

    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('school_dashboard'))

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
        
        message = ''
        if predicted_prob > 90:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO complaints (user_id, image_path, predicted_class, probability) VALUES (%s, %s, %s, %s)",
                           (session['user_id'], filepath, predicted_class, predicted_prob))
            conn.commit()
            conn.close()
        else:
            message = f"Complaint not significant. Can be addressed locally."
            predicted_class = "Mostly Clean"

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM complaints WHERE user_id=%s", (session['user_id'],))
        complaints = cursor.fetchall()
        conn.close()

        return render_template('school_dashboard.html',
                               prediction=predicted_class,
                               probability=f"{predicted_prob:.2f}%",
                               image_path=filepath,
                               complaints=complaints,
                               message=message)


# report generation 
@app.route('/generate_report/<institution_name>')
def generate_report(institution_name):
    if 'user_id' not in session or session['role'] != 'admin':
        return redirect(url_for('home'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT c.*, u.institution_name 
        FROM complaints c 
        JOIN users u ON c.user_id = u.id 
        WHERE c.status='Pending' AND u.institution_name=%s
    """, (institution_name,))
    complaints = cursor.fetchall()
    conn.close()

    rendered = render_template('report_template.html',
                               institution_name=institution_name,
                               complaints=complaints,
                               date=datetime.now().strftime("%d-%m-%Y"))

    pdf = BytesIO()
    pisa_status = pisa.CreatePDF(rendered, dest=pdf)
    pdf.seek(0)

    if pisa_status.err:
        return "Error creating PDF report"
    
    return send_file(pdf, download_name=f'{institution_name}_Report.pdf', as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
