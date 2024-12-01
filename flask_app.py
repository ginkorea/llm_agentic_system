from flask import Flask, render_template, request, redirect, url_for, jsonify
from threading import Thread
from agents.base import Agent
from cleaner import Cleaner
import os

# Initialize Flask app
app = Flask(__name__)

# Configuration for directories
app.config["PRD_FOLDER"] = "prd"  # Folder containing PRD files
app.config["WORK_FOLDER"] = "workbench"

# Global variable to store progress
progress = {"percentage": 0, "milestone": ""}

# Cleaner instance to manage workspace cleanup
cleaner = Cleaner()


def run_agent(prd_file):
    global progress

    # Initialize the agent
    agent = Agent(
        brain_type="code",
        memory_type="cuda",
        chaining=True,
        goal="Develop a Python Package based on the PRD.",
        goal_file=os.path.join(app.config["PRD_FOLDER"], prd_file)
    )

    # Callback for milestone completion
    def milestone_callback(name, output):
        progress["milestone"] = name
        progress["percentage"] = agent.brain.goal.get_progress()

    # Run the agent with the milestone callback
    agent.run(callback=milestone_callback)


@app.route("/")
def index():
    prd_files = [
        f for f in os.listdir(app.config["PRD_FOLDER"])
        if os.path.isfile(os.path.join(app.config["PRD_FOLDER"], f))
    ]
    return render_template("index.html", prd_files=prd_files)


@app.route("/start", methods=["POST"])
def start_development():
    prd_file = request.form.get("prd_file")
    if not prd_file:
        return redirect(url_for("index"))

    cleaner.start_fresh()
    thread = Thread(target=run_agent, args=(prd_file,))
    thread.start()
    return redirect(url_for("view_progress"))


@app.route("/progress")
def view_progress():
    return jsonify(progress)


@app.route("/results")
def view_results():
    milestone_outputs = progress.get("milestone_outputs", {})
    return render_template("results.html", milestone_outputs=milestone_outputs)


if __name__ == "__main__":
    os.makedirs(app.config["PRD_FOLDER"], exist_ok=True)
    os.makedirs(app.config["WORK_FOLDER"], exist_ok=True)

    # Disable the reloader
    app.run(debug=True, host="0.0.0.0", port=5000, use_reloader=False)
