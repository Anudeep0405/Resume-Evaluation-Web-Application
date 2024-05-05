from flask import Flask, request, render_template, jsonify
import PyPDF2

app = Flask(__name__)

def extract_text_from_pdf(file):
    try:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page_num in range(len(reader.pages)):
            text += reader.pages[page_num].extract_text()
        return text
    except:
        print("Error occurred while extracting text from the PDF.")
        return None

def evaluate_resume_for_job(resume_text, job_keywords):
    # Convert resume text and job keywords to lowercase for case-insensitive comparison
    resume_text_lower = resume_text.lower()

    # Initialize a score for matching keywords
    match_score = 0

    # Iterate through job keywords and check if they appear in the resume text
    for keyword in job_keywords:
        if keyword.lower() in resume_text_lower:
            match_score += 1

    # Normalize the score to a percentage
    total_keywords = len(job_keywords)
    score_percentage = (match_score / total_keywords) * 100

    return score_percentage

def evaluate_resume_for_selected_job(resume_text, selected_job_role, job_descriptions):
    if selected_job_role not in job_descriptions:
        return {"error": "Selected job role not found in job descriptions."}

    selected_job_keywords = job_descriptions[selected_job_role]
    return {selected_job_role: evaluate_resume_for_job(resume_text, selected_job_keywords)}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/evaluate', methods=['POST'])
def evaluate():
    job_descriptions = {
    "Software Engineer": ['Python', 'Java', 'web development', 'JavaScript', 'React', 'MySQL', 'Django', 'REST API'],
    "Data Scientist": ['Python', 'R', 'machine learning', 'data visualization', 'numpy', 'pandas', 'scikit-learn', 'SQL'],
    "Frontend Developer": ['HTML', 'CSS', 'JavaScript', 'React', 'Angular', 'Bootstrap', 'SASS', 'UI/UX design'],
    "Backend Developer": ['Python', 'Java', 'Node.js', 'Django', 'Spring Boot', 'Express.js', 'MongoDB', 'SQL'],
    "UI/UX Designer": ['UI design', 'UX design', 'Adobe XD', 'Sketch', 'Figma', 'InVision', 'Wireframing', 'Prototyping'],
    "Project Manager": ['project management', 'leadership', 'communication', 'Agile methodology', 'Scrum', 'Gantt charts', 'Risk management', 'Stakeholder management'],
    "Marketing Specialist": ['digital marketing', 'SEO', 'social media', 'Google Analytics', 'Content marketing', 'Email marketing', 'PPC advertising', 'Marketing automation'],
    "Financial Analyst": ['financial modeling', 'data analysis', 'Excel', 'financial reporting', 'forecasting', 'valuation', 'VBA', 'SQL'],
    "Human Resources Manager": ['recruitment', 'employee relations', 'HR policies', 'performance management', 'training and development', 'compensation and benefits', 'HRIS', 'employment law'],
    "Content Writer": ['copywriting', 'content marketing', 'SEO optimization', 'blogging', 'content strategy', 'editing', 'keyword research', 'social media content'],
    "Network Engineer": ['networking protocols', 'Cisco', 'firewalls', 'routing and switching', 'LAN/WAN', 'TCP/IP', 'VPN', 'Wireshark'],
    "DevOps Engineer": ['CI/CD', 'Docker', 'Kubernetes', 'Jenkins', 'Ansible', 'Terraform', 'AWS', 'Linux'],
    "Business Analyst": ['business requirements', 'data modeling', 'SQL', 'business process improvement', 'requirements gathering', 'Use case diagrams', 'SWOT analysis', 'UML'],
    "Quality Assurance Engineer": ['test automation', 'manual testing', 'bug tracking', 'Selenium', 'JUnit', 'JIRA', 'Load testing', 'Regression testing'],
    "System Administrator": ['Linux', 'Windows Server', 'Shell scripting', 'Active Directory', 'VMware', 'Backup and recovery', 'Monitoring tools', 'Server configuration'],
    "Database Administrator": ['SQL', 'database optimization', 'backup and recovery', 'MySQL', 'PostgreSQL', 'NoSQL', 'Data modeling', 'Database security'],
    "Technical Support Specialist": ['troubleshooting', 'ticketing systems', 'customer service', 'ITIL', 'Remote support', 'Hardware diagnostics', 'Windows troubleshooting', 'Mac troubleshooting'],
    "Sales Manager": ['sales strategies', 'customer relationship management', 'negotiation', 'Salesforce', 'Lead generation', 'Account management', 'Sales forecasting', 'Cold calling'],
    "Graphic Designer": ['Adobe Photoshop', 'Illustrator', 'typography', 'InDesign', 'Sketch', 'Logo design', 'Print design', 'Color theory'],
    "Legal Counsel": ['contract drafting', 'legal research', 'negotiation', 'Intellectual property law', 'Contract law', 'Legal writing', 'Corporate law', 'Privacy law'],
}




    resume_file = request.files['resume']  # Get the file object
    resume_text = extract_text_from_pdf(resume_file)  # Pass the file object to the function
    selected_job_role = request.form['job_role']  # Get the selected job role from the form

    if resume_text:
        evaluation_result = evaluate_resume_for_selected_job(resume_text, selected_job_role, job_descriptions)
        return jsonify(evaluation_result)
    else:
        return jsonify({"error": "Failed to extract text from the PDF resume."})

if __name__ == "__main__":
    app.run(debug=True)
