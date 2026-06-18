from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from datetime import datetime
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# =====================================================
# SECRET KEY
# =====================================================

app.secret_key = "complainthub_secret"

# =====================================================
# CONFIG
# =====================================================

UPLOAD_FOLDER = 'static/uploads'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# =====================================================
# DATABASE
# =====================================================

def init_db():

    conn = sqlite3.connect('ComplaintHub.db')

    c = conn.cursor()

    # =====================================================
    # COMPLAINTS TABLE
    # =====================================================

    c.execute('''

    CREATE TABLE IF NOT EXISTS complaints (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        name TEXT,
        phone TEXT,

        category TEXT,
        description TEXT,

        location TEXT,
        area TEXT,

        image TEXT,

        status TEXT,
        priority TEXT,
        created_at TEXT

    )

    ''')

    # =====================================================
    # FEEDBACKS TABLE
    # =====================================================

    c.execute('''

    CREATE TABLE IF NOT EXISTS feedbacks (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        name TEXT,
        phone TEXT,

        category TEXT,

        message TEXT,

        review TEXT

    )

    ''')

    conn.commit()

    # =====================================================
    # SAMPLE DATA
    # =====================================================

    c.execute("SELECT COUNT(*) FROM complaints")

    count = c.fetchone()[0]

    if count == 0:

        sample_data = [

            (
                "Rahul Kumar",
                "9876543210",
                "Water Leakage",
                "Water pipe leaking continuously near apartment.",
                "14.4426,79.9865",
                "Balaji Nagar",
                "water.jpg",
                "Pending",
                "High",
                "29-05-2026 10:30 AM"
            ),

            (
                "Akhil Reddy",
                "9876501234",
                "Garbage",
                "Garbage not cleaned from past 5 days.",
                "14.4500,79.9900",
                "Nellore Main Road",
                "garbage.jpg",
                "In Progress",
                "Medium",
                "29-05-2026 11:30 AM"
            ),

            (
                "Priya Sharma",
                "9988776655",
                "Road Damage",
                "Large potholes causing traffic and accidents.",
                "16.5062,80.6480",
                "Vijayawada Highway",
                "road.jpg",
                "Resolved",
                "High",
                "28-05-2026 09:00 AM"
            ),

            (
                "Kiran",
                "9123456780",
                "Street Light",
                "Street lights not working properly.",
                "14.4550,79.9950",
                "RTC Colony",
                "streetlight.jpg",
                "Pending",
                "Low",
                "28-05-2026 12:00 PM"
            )

        ]

        c.executemany('''

        INSERT INTO complaints
        (
            name,
            phone,
            category,
            description,
            location,
            area,
            image,
            status,
            priority,
            created_at
        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

        ''', sample_data)

        conn.commit()

    conn.close()

# =====================================================
# HOME
# =====================================================

@app.route('/')

def home():

    return render_template('index.html')

# =====================================================
# GALLERY
# =====================================================

@app.route('/gallery')

def gallery():

    return render_template('gallery.html')

# =====================================================
# CONTACT PAGE
# =====================================================

@app.route('/contact')

def contact():

    return render_template('contact.html')

# =====================================================
# SUBMIT FEEDBACK
# =====================================================

@app.route('/submit-feedback', methods=['POST'])

def submit_feedback():

    name = request.form['name']

    phone = request.form['phone']

    category = request.form['category']

    message = request.form['message']

    review = request.form['review']

    conn = sqlite3.connect('ComplaintHub.db')

    c = conn.cursor()

    c.execute('''

    INSERT INTO feedbacks
    (
        name,
        phone,
        category,
        message,
        review
    )

    VALUES (?, ?, ?, ?, ?)

    ''', (

        name,
        phone,
        category,
        message,
        review

    ))

    conn.commit()

    conn.close()

    return redirect('/contact')

# =====================================================
# SUBMIT COMPLAINT
# =====================================================

@app.route('/submit', methods=['GET', 'POST'])
@app.route('/report', methods=['GET', 'POST'])

def submit():

    if request.method == 'POST':

        name = request.form.get('name')

        phone = request.form.get('phone')

        category = request.form.get('category')

        description = request.form.get('description')

        location = request.form.get('location')

        area = request.form.get('area')

        priority = request.form.get('priority')

        image = request.files.get('photo')

        filename = ""

        if image and image.filename != "":

            filename = secure_filename(image.filename)

            image.save(
                os.path.join(
                    app.config['UPLOAD_FOLDER'],
                    filename
                )
            )

        conn = sqlite3.connect('ComplaintHub.db')

        c = conn.cursor()

                # CURRENT DATE & TIME

        created_at = datetime.now().strftime(
            "%d-%m-%Y %I:%M %p"
        )

        c.execute('''

        INSERT INTO complaints
        (
            name,
            phone,
            category,
            description,
            location,
            area,
            image,
            status,
            priority,
            created_at
        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

        ''', (

            name,
            phone,
            category,
            description,
            location,
            area,
            filename,
            'Pending',
            priority,
            created_at

        ))

        conn.commit()

        conn.close()

        return redirect('/track')

    return render_template('submit_complaint.html')

# =====================================================
# TRACK COMPLAINTS
# =====================================================

@app.route('/track', methods=['GET', 'POST'])

def track():

    complaints = []

    if request.method == 'POST':

        phone = request.form.get('phone')

        conn = sqlite3.connect('ComplaintHub.db')

        c = conn.cursor()

        c.execute(
            "SELECT * FROM complaints WHERE phone=? ORDER BY id DESC",
            (phone,)
        )

        complaints = c.fetchall()

        conn.close()

    return render_template(
        'track.html',
        complaints=complaints
    )

# =====================================================
# ADMIN LOGIN
# =====================================================

@app.route('/admin', methods=['GET', 'POST'])

def admin_login():

    if request.method == 'POST':

        username = request.form.get('username')

        password = request.form.get('password')

        if username == "admin" and password == "admin123":

            session['admin'] = True

            return redirect('/admin-dashboard')

        else:

            return "Invalid Username or Password"

    return render_template('admin/admin_login.html')

# =====================================================
# ADMIN LOGOUT
# =====================================================

@app.route('/admin/logout')

def admin_logout():

    session.pop('admin', None)

    return redirect(url_for('home'))

# =====================================================
# ADMIN DASHBOARD
# =====================================================

@app.route('/admin-dashboard')

def admin_dashboard():

    if 'admin' not in session:

        return redirect('/admin')

    conn = sqlite3.connect('ComplaintHub.db')

    c = conn.cursor()

    c.execute("SELECT * FROM complaints ORDER BY id DESC")

    complaints = c.fetchall()

    # =====================================================
    # COUNTS
    # =====================================================

    c.execute("SELECT COUNT(*) FROM complaints")

    total = c.fetchone()[0]

    c.execute(
        "SELECT COUNT(*) FROM complaints WHERE status='Pending'"
    )

    pending = c.fetchone()[0]

    c.execute(
        "SELECT COUNT(*) FROM complaints WHERE status='In Progress'"
    )

    progress = c.fetchone()[0]

    c.execute(
        "SELECT COUNT(*) FROM complaints WHERE status='Resolved'"
    )

    resolved = c.fetchone()[0]

    # =====================================================
    # MAP LOCATIONS
    # =====================================================

    map_locations = []

    for complaint in complaints:

        try:

            coordinates = complaint[5].split(',')

            latitude = float(coordinates[0])

            longitude = float(coordinates[1])

            map_locations.append({

                "name": complaint[1],
                "category": complaint[3],
                "area": complaint[6],
                "status": complaint[8],
                "date": complaint[10],
                "lat": latitude,
                "lng": longitude

            })

            

        except:

            pass
    from collections import Counter

    weekly_counter = Counter()

    c.execute(
    "SELECT created_at FROM complaints"
)

    dates = c.fetchall()

    for item in dates:

        try:

            dt = datetime.strptime(
                 item[0],
                "%d-%m-%Y %I:%M %p"
        )

            day = dt.strftime("%a")

            weekly_counter[day] += 1

        except:

          pass

        weekly_counts = [

    weekly_counter['Mon'],
    weekly_counter['Tue'],
    weekly_counter['Wed'],
    weekly_counter['Thu'],
    weekly_counter['Fri'],
    weekly_counter['Sat'],
    weekly_counter['Sun']

]
    conn.close()

        # ==========================================
    # WEEKLY TREND SAMPLE DATA
    # ==========================================

    
    return render_template(

        'admin/admin_dashboard.html',

        complaints=complaints,

        total=total,

        pending=pending,

        progress=progress,

        resolved=resolved,

        map_locations=map_locations,

        weekly_counts=weekly_counts

    )

# =====================================================
# ADMIN COMPLAINTS
# =====================================================

@app.route('/admin/complaints')

def admin_complaints():

    if 'admin' not in session:

        return redirect('/admin')

    conn = sqlite3.connect('ComplaintHub.db')

    c = conn.cursor()

    c.execute(
        "SELECT * FROM complaints ORDER BY id DESC"
    )

    complaints = c.fetchall()

    conn.close()

    return render_template(
        'admin/complaints.html',
        complaints=complaints
    )

# =====================================================
# COMPLAINT DETAILS
# =====================================================

@app.route('/complaint/<int:id>')

def complaint_view(id):

    if 'admin' not in session:

        return redirect('/admin')

    conn = sqlite3.connect('ComplaintHub.db')

    c = conn.cursor()

    c.execute(
        "SELECT * FROM complaints WHERE id=?",
        (id,)
    )

    complaint = c.fetchone()

    conn.close()

    return render_template(
        'admin/complaint_view.html',
        complaint=complaint
    )

# =====================================================
# UPDATE STATUS
# =====================================================

@app.route('/update-status/<int:id>/<status>')

def update_status(id, status):

    if 'admin' not in session:

        return redirect('/admin')

    conn = sqlite3.connect('ComplaintHub.db')

    c = conn.cursor()

    c.execute(
        "UPDATE complaints SET status=? WHERE id=?",
        (status, id)
    )

    conn.commit()

    conn.close()

    return redirect(
        url_for('complaint_view', id=id)
    )

# =====================================================
# DELETE COMPLAINT
# =====================================================

@app.route('/delete-complaint/<int:id>')

def delete_complaint(id):

    if 'admin' not in session:

        return redirect('/admin')

    conn = sqlite3.connect('ComplaintHub.db')

    c = conn.cursor()

    c.execute(
        "DELETE FROM complaints WHERE id=?",
        (id,)
    )

    conn.commit()

    conn.close()

    return redirect('/admin/complaints')

# =====================================================
# ANALYTICS
# =====================================================

@app.route('/admin/analytics')

def analytics():

    if 'admin' not in session:

        return redirect('/admin')

    conn = sqlite3.connect('ComplaintHub.db')

    c = conn.cursor()

    # ==========================================
    # STATUS COUNTS
    # ==========================================

    c.execute(
        "SELECT COUNT(*) FROM complaints WHERE status='Pending'"
    )

    pending = c.fetchone()[0]

    c.execute(
        "SELECT COUNT(*) FROM complaints WHERE status='In Progress'"
    )

    progress = c.fetchone()[0]

    c.execute(
        "SELECT COUNT(*) FROM complaints WHERE status='Resolved'"
    )

    resolved = c.fetchone()[0]

    # ==========================================
    # CATEGORY DATA
    # ==========================================

    c.execute('''

        SELECT category, COUNT(*)

        FROM complaints

        GROUP BY category

    ''')

    category_data = c.fetchall()

    category_labels = []
    category_counts = []

    for row in category_data:

        category_labels.append(row[0])

        category_counts.append(row[1])

    # ==========================================
    # HIGH PRIORITY CATEGORY DATA
    # ==========================================

    c.execute('''

        SELECT category, COUNT(*)

        FROM complaints

        WHERE priority='High'

        GROUP BY category

    ''')

    high_priority = c.fetchall()

    # ==========================================
    # WEEKLY TREND
    # ==========================================

    from collections import Counter

    weekly_counter = Counter()

    c.execute(
        "SELECT created_at FROM complaints"
    )

    dates = c.fetchall()

    for item in dates:

        try:

            dt = datetime.strptime(
                item[0],
                "%d-%m-%Y %I:%M %p"
            )

            day = dt.strftime("%a")

            weekly_counter[day] += 1

        except:

            pass

    weekly_counts = [

        weekly_counter['Mon'],
        weekly_counter['Tue'],
        weekly_counter['Wed'],
        weekly_counter['Thu'],
        weekly_counter['Fri'],
        weekly_counter['Sat'],
        weekly_counter['Sun']

    ]

    conn.close()

    return render_template(

        'admin/analytics.html',

        pending=pending,

        progress=progress,

        resolved=resolved,

        category_labels=category_labels,

        category_counts=category_counts,

        weekly_counts=weekly_counts

    )

# =====================================================
# ADMIN FEEDBACKS
# =====================================================

@app.route('/admin/feedbacks')

def feedbacks():

    if 'admin' not in session:

        return redirect('/admin')

    conn = sqlite3.connect('ComplaintHub.db')

    c = conn.cursor()

    c.execute(
        "SELECT * FROM feedbacks ORDER BY id DESC"
    )

    feedbacks = c.fetchall()

    conn.close()

    return render_template(
        'admin/feedbacks.html',
        feedbacks=feedbacks
    )

# =====================================================
# RUN APP
# =====================================================

if __name__ == '__main__':

    init_db()

    app.run(debug=True)