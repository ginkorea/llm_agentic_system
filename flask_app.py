from flask import Flask, render_template, request, redirect, url_for, jsonify
from threading import Thread
from agents.base import Agent
import os
from cleaner import Cleaner

app = Flask(__name__)

app.config["PRD_FOLDER"] = "prd"
app.config["WORK_FOLDER"] = "workbench"

progress = {"percentage": 0, "milestone": "Initializing...", "status": "running"}

cleaner = Cleaner()


def run_agent(prd_file):
    global progress
    agent = Agent(
        brain_type="code",
        memory_type="cuda",
        chaining=True,
        goal="Develop a Python Package based on the PRD.",
        goal_file=os.path.join(app.config["PRD_FOLDER"], prd_file)
    )

    def milestone_callback(name, output):
        progress["milestone"] = name
        progress["percentage"] = agent.brain.goal.get_progress()
        if agent.brain.goal.is_complete():
            progress["percentage"] = 100
            progress["status"] = "completed"

    try:
        # Initialize first milestone
        progress["milestone"] = "Starting development..."
        agent.run(callback=milestone_callback)
        progress["percentage"] = 100
        progress["status"] = "completed"
    except Exception as e:
        progress["status"] = f"error: {str(e)}"


@app.route("/")
def index():
    prd_files = [f for f in os.listdir(app.config["PRD_FOLDER"]) if os.path.isfile(os.path.join(app.config["PRD_FOLDER"], f))]
    return render_template("index.html", prd_files=prd_files, progress=progress)


@app.route("/start", methods=["POST"])
def start_development():
    prd_file = request.form.get("prd_file")
    if not prd_file:
        return redirect(url_for("index"))

    cleaner.start_fresh()
    progress.update({"percentage": 0, "milestone": "Initializing...", "status": "running"})
    thread = Thread(target=run_agent, args=(prd_file,))
    thread.start()

    return redirect(url_for("index"))


@app.route("/progress")
def view_progress():
    return jsonify(progress)


@app.route("/results")
def view_results():
    return render_template("results.html")


@app.route("/explore")
def explore_workbench():
    files = []
    for root, _, filenames in os.walk(app.config["WORK_FOLDER"]):
        for filename in filenames:
            relative_path = os.path.relpath(os.path.join(root, filename), app.config["WORK_FOLDER"])
            files.append(relative_path)
    return jsonify(files)


@app.route("/file-content")
def file_content():
    file = request.args.get("file")
    file_path = os.path.join(app.config["WORK_FOLDER"], file)
    if not os.path.exists(file_path):
        return "File not found", 404
    with open(file_path, "r") as f:
        content = f.read()
    return content


if __name__ == "__main__":
    os.makedirs(app.config["PRD_FOLDER"], exist_ok=True)
    os.makedirs(app.config["WORK_FOLDER"], exist_ok=True)
    app.run(debug=True, use_reloader=False, host="0.0.0.0", port=5000)
