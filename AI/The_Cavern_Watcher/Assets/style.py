def get_page_style():
    return f"""        <style>

        body {{
            font-family: Arial, sans-serif;
            margin: 0px;
            overflow:hidden;
            display:flex;
            align-items: flex-start;
            justify-content: flex-start;
        }}

        .backdrop{{
            position: absolute;
            padding:0px;
            margin:0px;
            min-width:100vw;
            height:100vh;
            z-index: -1;
        }}
        </style>"""

def get_chat_style():
    return f"""
        <style>
            .chat-box {{
            background: #d9d3d315;
            margin-left: 2%;
            margin-top:1%;
            padding: 1em;
            border-radius: 10px;
            width: 40vw;
            height:90vh;
        }}

        .messages {{
            min-height: 90%;
            max-height: 70%;
            overflow-y: auto;
            margin-bottom: 1em;
            padding: 10px;
            border-radius: 5px;
            background: #d9d3d332;
            display: flex;
            flex-direction: column;
            gap: 0.5em;
        }}

        .message {{
            max-width: 70%;
            padding: 0.7em 1em;
            border-radius: 15px;
            word-wrap: break-word;
            font-size: 1em;
        }}

        .message.user {{
            align-self: flex-end;
            background-color: #4893b579;
            color: white;
            border-bottom-right-radius: 0;
        }}

        .message.gnome {{
            align-self: flex-start;
            background-color: #8b71228f;
            color: black;
            border-bottom-left-radius: 0;
        }}

        .input-area {{
            display: flex;
            gap: 0.3em;
            width: 100%;
        }}

        .input-area input {{
            flex: 1;
            padding: 0.5em;
            border-radius: 5px;
            border: none;
            font-size: 1em;
        }}

        .input-area button {{
            padding: 0.5em 1em;
            border: none;
            border-radius: 5px;
            background-color: #4bc9d5;
            color: white;
            cursor: pointer;
        }}

        .input-area button:hover {{
            background-color: #3572b9;
        }}

        </style>
    """