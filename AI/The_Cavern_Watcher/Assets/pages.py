import style
import scripts

path = "http://127.0.0.1:5000/"

def generate_page():
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>The Cavern Watcher</title>
        <link rel="icon" type="image/x-icon" href="{path}static/gnome_icon.png">

        {style.get_page_style()}
    </head>
    <body>
        <img class="backdrop" src="{path}static/gnome_backdrop.webp"></img>
        <div>
            {generate_chat_box()}
        </div>
    </body>
    </html>
    """

def generate_chat_box():
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">

        {style.get_chat_style()}
    </head>
    <body>
        <div class="chat-box">
            <div class="messages" id="messages">

            </div>
            <div class="input-area">
                <input type="text" id="userInput" placeholder="Type your message...">
                <button class="sendBtn">Send</button>
                <button id="recordBtn" class="recordBtn">Record</button>
            </div>
    </div>
        {scripts.get_chat_scripts()}
    </body>
    </html>
    """

