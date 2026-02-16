
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/")
def index():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Simple Chat Agent</title>
        <style>
            body { font-family: sans-serif; display: flex; flex-direction: column; height: 100vh; margin: 0; }
            #chat { flex: 1; overflow-y: auto; padding: 20px; background: #f4f4f9; }
            #input-area { padding: 20px; border-top: 1px solid #ddd; display: flex; }
            #message { flex: 1; padding: 10px; border: 1px solid #ccc; border-radius: 4px; }
            #send { padding: 10px 20px; margin-left: 10px; background: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; }
            .msg { margin-bottom: 10px; padding: 10px; border-radius: 4px; max-width: 80%; }
            .user { background: #007bff; color: white; align-self: flex-end; margin-left: auto; }
            .agent { background: #e9e9eb; color: #333; align-self: flex-start; }
        </style>
    </head>
    <body>
        <div id="chat"></div>
        <div id="input-area">
            <input type="text" id="message" placeholder="Type a message..." onkeypress="if(event.key === 'Enter') send()">
            <button id="send" onclick="send()">Send</button>
        </div>
        <script>
            function appendMessage(role, text) {
                const chat = document.getElementById('chat');
                const div = document.createElement('div');
                div.className = 'msg ' + role;
                div.innerText = text;
                chat.appendChild(div);
                chat.scrollTop = chat.scrollHeight;
            }

            async function send() {
                const input = document.getElementById('message');
                const text = input.value.trim();
                if (!text) return;
                
                appendMessage('user', text);
                input.value = '';

                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: text })
                });
                const data = await response.json();
                appendMessage('agent', data.response);
            }

            // Initial greeting
            appendMessage('agent', 'Hello! How can I help you today?');
        </script>
    </body>
    </html>
    """

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")
    # A simple echo-like response for now, can be expanded with more logic
    response = f"You said: {user_message}. I'm a simple agent hosted on Render!"
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
