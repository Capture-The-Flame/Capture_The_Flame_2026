from flask import Flask, Response, json,jsonify,request
import calls,pages

app = Flask(__name__)

@app.route("/")
def home():
    html = pages.generate_page()
    return Response(html, mimetype="text/html")


@app.route("/sendToGnome", methods=["POST"])
def process_audio():
    audio = request.files['file']
    convo_history = json.loads(request.form.get('history'))
    # print(convo_history)
    response = calls.speak_to_gnome(audio,convo_history)
    return jsonify({"messages": response})

@app.route("/typeToGnome", methods=["POST"])
def process_text():
    data = request.get_json()
    message = data.get("message")
    convo_history = data.get("history")
    # response = calls.get_response_from_gnome(message,convo_history
    response = calls.build_response(message,convo_history)

    return jsonify({"messages": response})

if __name__ == "__main__":
    app.run(debug=True)

