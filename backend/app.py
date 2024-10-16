from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
import re
import Levenshtein
from detectors import detect_exact_match_score, detect_variable_renaming_score, detect_structural_similarity_score
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Max file size: 16MB

ALLOWED_EXTENSIONS = {'py', 'js', 'java', 'cpp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/check', methods=['POST'])
def check_code():
    code1 = None
    code2 = None

    # Handle file-based plagiarism check
    if 'codeFile1' in request.files and 'codeFile2' in request.files:
        file1 = request.files['codeFile1']
        file2 = request.files['codeFile2']

        if file1 and allowed_file(file1.filename):
            filename1 = secure_filename(file1.filename)
            filepath1 = os.path.join(app.config['UPLOAD_FOLDER'], filename1)
            file1.save(filepath1)
            with open(filepath1, 'r') as f:
                code1 = f.read()
        else:
            return jsonify({'error': 'Invalid file type for file1'}), 400

        if file2 and allowed_file(file2.filename):
            filename2 = secure_filename(file2.filename)
            filepath2 = os.path.join(app.config['UPLOAD_FOLDER'], filename2)
            file2.save(filepath2)
            with open(filepath2, 'r') as f:
                code2 = f.read()
        else:
            return jsonify({'error': 'Invalid file type for file2'}), 400

    # Handle text-based plagiarism check
    elif request.is_json:
        data = request.get_json()
        code1 = data.get('code1', None)
        code2 = data.get('code2', None)

    # Ensure both code1 and code2 are provided for text or file
    if not code1 or not code2:
        return jsonify({'error': 'Both code inputs are required'}), 400

    try:
        # Calculate individual scores for plagiarism detection
        exact_match_score = detect_exact_match_score(code1, code2)
        variable_renaming_score = detect_variable_renaming_score(code1, code2)
        structural_similarity_score = detect_structural_similarity_score(code1, code2)
    except Exception as e:
        return jsonify({'error': f'Error during plagiarism detection: {str(e)}'}), 500

    result = {
        'exact_match_score': exact_match_score,
        'variable_renaming_score': variable_renaming_score,
        'structural_similarity_score': structural_similarity_score
    }

    return jsonify(result)

@app.route('/batch_check', methods=['POST'])
def batch_check():
    if 'masterFile' not in request.files or 'files[]' not in request.files:
        return jsonify({'error': 'Master file and other files are required'}), 400

    master_file = request.files['masterFile']
    other_files = request.files.getlist('files[]')

    if not allowed_file(master_file.filename):
        return jsonify({'error': 'Invalid file type for master file'}), 400

    # Save master file
    master_filename = secure_filename(master_file.filename)
    master_filepath = os.path.join(app.config['UPLOAD_FOLDER'], master_filename)
    master_file.save(master_filepath)
    with open(master_filepath, 'r') as f:
        master_code = f.read()

    results = []
    flagged_files = []

    for file in other_files:
        if not allowed_file(file.filename):
            continue

        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        with open(filepath, 'r') as f:
            file_code = f.read()

        # Calculate individual scores
        exact_match_score = detect_exact_match_score(master_code, file_code)
        variable_renaming_score = detect_variable_renaming_score(master_code, file_code)
        structural_similarity_score = detect_structural_similarity_score(master_code, file_code)

        average_score = (exact_match_score + variable_renaming_score + structural_similarity_score) / 3

        result = {
            'filename': file.filename,
            'exact_match_score': exact_match_score,
            'variable_renaming_score': variable_renaming_score,
            'structural_similarity_score': structural_similarity_score,
            'average_score': average_score
        }

        results.append(result)

        # Flag file if average score is above 80%
        if average_score > 80:
            flagged_files.append(file.filename)

    return jsonify({'results': results, 'flagged_files': flagged_files})

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)