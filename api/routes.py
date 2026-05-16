# api/routes.py

from flask import Flask, request, jsonify
from screening_ai.report_generator import generate_screening_report

app = Flask(__name__)

@app.route("/screening/start", methods=["POST"])
def start_screening():
    data = request.json
    candidate_id = data["candidate_id"]
    job_id = data["job_id"]
    answers = data["answers"]
    # Simulated scoring + behavior outputs
    scores = data["scores"]
    behavior_reports = data["behavior"]
    
    report = generate_screening_report(
        candidate_id,
        job_id,
        answers,
        scores,
        behavior_reports
    )
    return jsonify(report)
