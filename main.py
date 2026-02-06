from flask import request, Flask, jsonify
from dotenv import load_dotenv
from agents import resume_text, analyse_woman_psicological_issue

load_dotenv()
app = Flask(__name__)

@app.route('/resume', methods=['POST'])
def resume_text_with_llm():
    data = request.get_json()
    text_to_resume = data.get('text')

    resume = resume_text(text_to_resume)

    return resume, 200

@app.route('/analyse-psycological-issue', methods=['POST'])
def analyse_psicological_issue():
    data = request.get_json()
    text_to_analyse = data.get('text')

    resume = analyse_woman_psicological_issue(text_to_analyse)

    return resume, 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
