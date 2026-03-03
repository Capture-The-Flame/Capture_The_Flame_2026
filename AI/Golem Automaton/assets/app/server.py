#!/usr/bin/env python3

from flask import Flask, request, jsonify, render_template_string, send_file
import os
import time
import pytesseract  # This is the OCR library that reads text from images
from PIL import Image, ImageChops  # For working with images
import io
import hashlib

# Create the Flask app
app = Flask(__name__)

# CONFIGURATION - Settings for the challenge

# The correct Latin phrases (shortened to fit on parchment)
CORRECT_PHRASES = [
    "VERITAS LUX",           # "Truth is light" - gives the flag
    "FORTIS FORTUNA",        # "Fortune is brave" - Easter egg 1
    "CARPE DIEM"             # "Seize the day" - Easter egg 2
]

# The main flag that players are trying to get
FLAG = "Flame{Anc1entG0l3m}"

# Easter eggs for the other phrases
EASTER_EGGS = {
    "FORTIS FORTUNA": "The Golem wakes and bestows the warrior's blessing upon you.",
    "CARPE DIEM": "The Golem wakes and bestows the philosopher's wisdom upon you."
}

# Rate limiting: Store when each IP last submitted
# This prevents spam and gives the OCR model time to process
last_submission_time = {}
COOLDOWN_SECONDS = 5  # 5 second cooldown between submissions

# HELPER FUNCTIONS

# Verify that an image was created by make_image.sh
def check_image_authenticity(image):
    width, height = image.size
    
    # Check 1: Dimensions must be exactly 400x200
    # make_image.sh resizes to these exact dimensions
    if width != 400 or height != 200:
        return False, "Invalid image dimensions. Images must be 400x200 pixels."
    
    # Check 2: Load the original parchment to compare
    try:
        original_parchment = Image.open('/app/parchment.png')
        original_parchment = original_parchment.resize((400, 200), Image.Resampling.LANCZOS)
        
        # Convert both to RGB mode for comparison
        image_rgb = image.convert('RGB')
        parchment_rgb = original_parchment.convert('RGB')
        
        # Calculate difference between images
        # If they're too different, it's not based on our parchment
        diff = ImageChops.difference(image_rgb, parchment_rgb)
        
        # Get statistics about the differences
        stat = diff.getextrema()  # Gets min and max values for each channel
        
        # If the max difference in any channel is less than 50, it's too similar to blank parchment
        # (meaning no text was added, or wrong parchment used)
        if max(max(s) for s in stat) > 50:
            return True, "Image verified"
        else:
            return False, "Image does not appear to contain valid parchment text."
            
    except Exception as e:
        return False, f"Could not verify image authenticity: {str(e)}"

# Enforce cooldown between submissions.
def check_rate_limit(identifier):
    current_time = time.time()
    
    if identifier in last_submission_time:
        time_since_last = current_time - last_submission_time[identifier]
        if time_since_last < COOLDOWN_SECONDS:
            # User submitted too recently
            wait_time = COOLDOWN_SECONDS - time_since_last
            return False, f"Please wait {wait_time:.1f} more seconds before submitting again."
    
    # Update the last submission time
    last_submission_time[identifier] = current_time
    return True, "OK"

# WEB ROUTES

@app.route('/')
def index():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>The Old Man's Golem</title>
        <style>
            body {
                background: #1a1a1a;
                color: #d4af37;
                font-family: 'Georgia', serif;
                padding: 40px;
                max-width: 700px;
                margin: 0 auto;
                position: relative;
            }
            .scroll {
                background: #2b2416;
                border: 3px solid #8b7355;
                padding: 40px;
                border-radius: 10px;
                box-shadow: 0 0 20px rgba(0,0,0,0.5);
            }
            h1 { 
                color: #d4af37; 
                text-align: center;
                font-size: 2.8em;
                margin-bottom: 10px;
            }
            .oracle-desc {
                font-size: 1.05em;
                line-height: 1.8;
                margin-bottom: 25px;
            }
            .code-box {
                background: #1a1a1a;
                border: 1px solid #8b7355;
                padding: 12px;
                margin: 10px 0;
                border-radius: 5px;
                font-family: 'Courier New', monospace;
                font-size: 0.85em;
            }
            .whisper {
                position: fixed;
                bottom: 20px;
                right: 20px;
                background: #3a2a1a;
                border: 2px solid #8b7355;
                padding: 15px 20px;
                border-radius: 8px;
                cursor: pointer;
                font-size: 0.9em;
                box-shadow: 0 0 15px rgba(212, 175, 55, 0.3);
                transition: all 0.3s;
            }
            .whisper:hover {
                background: #4a3a2a;
                box-shadow: 0 0 25px rgba(212, 175, 55, 0.5);
            }
            .whisper-content {
                display: none;
                margin-top: 10px;
                padding-top: 10px;
                border-top: 1px solid #8b7355;
                font-style: italic;
                color: #c9a961;
            }
            .whisper.open .whisper-content {
                display: block;
            }
        </style>
        <script>
            function toggleWhisper() {
                document.getElementById('whisper').classList.toggle('open');
            }
        </script>
    </head>
    <body>
        <div class="scroll">
            <h1>The Old Man and his Golem</h1>
            
            <p class="oracle-desc">
                Hello, young lad! I see you've stumbled upon my latest work!
                It's a golem, which I created through an ancient arcane magic.
                Come try it out! All you need to do is feed it a piece of parchment
                with a certain incantation written on it. I made a tool to make the
                process easier, as well!
            </p>
            
            <p class="oracle-desc">
                To create a parchment worthy of the Golem's gaze, use the sacred incantation:
            </p>
            
            <div class="code-box">
                # Download the parchment creation script <br>
                curl -O http://localhost:5000/download/make_image.sh <br>
                curl -O http://localhost:5000/download/parchment.png <br> <br>

                # Make it executable <br>
                chmod +x make_image.sh <br> <br>

                # Create your parchment <br> 
                ./make_image.sh "YOUR PHRASE" "./scroll.png"
            </div>
            
            <p class="oracle-desc">
                Then present your scroll to the Golem:
            </p>
            
            <div class="code-box">
                curl -X POST http://localhost:5000/api/ocr -F "image=@scroll.png"
            </div>
            
            <p class="oracle-desc" style="text-align: center; margin-top: 30px; font-style: italic;">
                You could ask this Golem for anything, really; fame, wealth, luck...a <em>flag</em>... what? Who said that?
            </p>
        </div>
        
        <div id="whisper" class="whisper" onclick="toggleWhisper()">
            <div style="font-weight: bold;">psst... 👀</div>
            <div class="whisper-content">
                Check out where the robots go...<br>
                <span style="font-size: 0.8em;">beep boop 🤖</span>
            </div>
        </div>
    </body>
    </html>
    """
    return render_template_string(html)

@app.route('/robots.txt')
def robots():
    return """
        User-agent: *
        Disallow: /admin/
        Disallow: /api/internal/
        Disallow: /scribe/parchments
"""

@app.route('/scribe/parchments')
def list_parchments():
    import base64
    
    # Encode each phrase in base64
    encoded_phrases = []
    for phrase in CORRECT_PHRASES:
        encoded = base64.b64encode(phrase.encode()).decode()
        encoded_phrases.append(encoded)
    
    return jsonify({
        'message': 'These ancient texts have been written in a secret language.',
        'texts': encoded_phrases
    })

@app.route('/api/ocr', methods=['POST'])
def ocr_submit():
    
    # Use IP address for rate limiting
    ip_address = request.remote_addr
    
    # Step 1: Check rate limiting
    can_submit, message = check_rate_limit(ip_address)
    if not can_submit:
        return jsonify({'error': 'Rate limit exceeded', 'message': message}), 429
    
    # Step 2: Get the uploaded image
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    image_file = request.files['image']
    
    # Step 3: Validate image authenticity
    try:
        image = Image.open(image_file.stream)
        is_valid, validation_message = check_image_authenticity(image)
        
        if not is_valid:
            return jsonify({
                'error': 'Invalid parchment',
                'message': validation_message
            }), 400
            
    except Exception as e:
        return jsonify({'error': 'Could not read parchment', 'details': str(e)}), 400
    
    # Step 4: Perform OCR
    image_file.stream.seek(0)
    image = Image.open(image_file.stream)
    
    try:
        # Use pytesseract to read text from the image
        ocr_text = pytesseract.image_to_string(image).strip().upper()
        
        # Clean up the OCR result
        ocr_text = ' '.join(ocr_text.split())  # Normalize whitespace
        
    except Exception as e:
        return jsonify({
            'error': 'The Oracle cannot read this parchment',
            'details': str(e)
        }), 500
    
    # Step 5: Check what phrase was detected
    
    # Check if it's the winning phrase (the first one)
    if ocr_text == CORRECT_PHRASES[0]:
        return jsonify({
            'success': True,
            'oracle_speaks': 'The Golem wakes, and utters a strange phrase...',
            'phrase_read': ocr_text,
            'flag': FLAG
        })
    
    # Check if it's one of the easter egg phrases
    elif ocr_text in EASTER_EGGS:
        return jsonify({
            'success': False,
            'oracle_speaks': EASTER_EGGS[ocr_text],
            'phrase_read': ocr_text,
            'hint': 'The Golem looks at you strangely before returning to sleep.'
        })
    
    # Check if it's a correct phrase but not the right one
    elif ocr_text in CORRECT_PHRASES:
        return jsonify({
            'success': False,
            'oracle_speaks': 'The Golem wakes and looks at you strangely before returning to sleep.',
            'phrase_read': ocr_text
        })
    
    # Phrase not recognized
    else:
        return jsonify({
            'success': False,
            'oracle_speaks': 'The Golem wakes and looks at you strangely before returning to sleep.',
            'phrase_read': ocr_text
        })

@app.route('/health')
def health():
    return jsonify({
        'status': 'alive',
        'message': 'The Golem appears to be waiting patiently.'
    })

@app.route('/download/make_image.sh')
def download_script():
    """
    Download the image creation script.
    Players need this to create valid parchments.
    """
    script_path = '/app/scripts/make_image.sh'
    return send_file(
        script_path,
        as_attachment=True,
        download_name='make_image.sh',
        mimetype='text/x-shellscript'
    )

@app.route('/download/parchment.png')
def download_parchment():
    return send_file(
        '/app/parchment.png',
        as_attachment=True,
        download_name='parchment.png',
        mimetype='image/png'
    )

@app.route('/download/EzraSil-Po0B.ttf')
def download_font():
    return send_file(
        '/app/fonts/EzraSil-Po0B.ttf',
        as_attachment=True,
        download_name='EzraSil-Po0B.ttf',
        mimetype='font/ttf'
    )

# START THE SERVER
if __name__ == '__main__':
    # Start the Flask web server
    app.run(host='0.0.0.0', port=5000, debug=False)
