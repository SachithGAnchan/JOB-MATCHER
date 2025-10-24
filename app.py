from flask import Flask, render_template, request
import json
import difflib

app = Flask(__name__)

# Load job data
with open("jobs.json") as f:
    jobs = json.load(f)
all_skills = sorted({skill.lower() for job in jobs for skill in job["skills"]})

@app.route("/", methods=["GET", "POST"])
def index():
    matches = []
    message = ""

    if request.method == "POST":
        user_input = request.form["skills"]
        raw_skills = [skill.strip().lower() for skill in user_input.split(",") if skill.strip()]
        
        all_job_skills = {s.lower() for job in jobs for s in job["skills"]}

        user_skills = []
        for skill in raw_skills:
            close_matches = difflib.get_close_matches(skill, all_job_skills, n=1, cutoff=0.6)
            if close_matches:
                user_skills.append(close_matches[0])
            else:
                print(f"No close match for: {skill}")

        for job in jobs:
            job_skills = [s.lower() for s in job["skills"]]
            match_count = len(set(user_skills) & set(job_skills))
            if match_count > 0:
                job["match_score"] = match_count
                matches.append(job)

        matches.sort(key=lambda x: x["match_score"], reverse=True)

        if not matches:
            message = "No matching jobs found. Please check your spelling or try different skills."

    return render_template("index.html", matches=matches, message=message,all_skills=all_skills)


if __name__ == "__main__":
    app.run(debug=True)
