from flask import Flask, send_from_directory, send_file
app = Flask(__name__)


@app.after_request
def add_header(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response

@app.route('/')
def playPage():
    return send_from_directory('public', 'playPage.html')

@app.route('/styles.css')
def style():
    return send_from_directory('public', 'styles.css')

def main():
    host = "0.0.0.0"
    port = 8080

    print("Listening on port " + str(port))

    app.run(host=host, port=port)

    
if __name__ == "__main__":
    main()