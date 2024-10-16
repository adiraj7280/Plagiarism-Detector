import re
import Levenshtein

# Detect exact match plagiarism score between two code snippets
def detect_exact_match_score(code1, code2):
    # Clean code snippets by removing comments and whitespace
    cleaned_code1 = remove_comments_and_whitespace(code1)
    cleaned_code2 = remove_comments_and_whitespace(code2)
    
    # Calculate similarity using Levenshtein distance (as a percentage)
    similarity = Levenshtein.ratio(cleaned_code1, cleaned_code2) * 100
    return similarity

# Detect plagiarism based on variable renaming
def detect_variable_renaming_score(code1, code2):
    # Tokenize the code to replace variable names with a placeholder
    tokenized_code1 = tokenize_code(code1)
    tokenized_code2 = tokenize_code(code2)
    
    # Calculate similarity based on tokenized code
    similarity = Levenshtein.ratio(tokenized_code1, tokenized_code2) * 100
    return similarity

# Detect structural similarity in code (e.g., using similar control structures)
def detect_structural_similarity_score(code1, code2):
    # Normalize the code structure by identifying common control structures
    normalized_code1 = normalize_structure(code1)
    normalized_code2 = normalize_structure(code2)
    
    # Calculate similarity based on structural patterns
    similarity = Levenshtein.ratio(normalized_code1, normalized_code2) * 100
    return similarity

# Remove comments and whitespace from the code
def remove_comments_and_whitespace(code):
    # Remove single-line comments (Python, JS, C-style)
    code = re.sub(r'#.*', '', code)  # Python-style comments
    code = re.sub(r'//.*', '', code)  # JS/Java/C++ single-line comments
    
    # Remove block comments (JavaScript/Java/C-style)
    code = re.sub(r'/\*[\s\S]*?\*/', '', code)
    
    # Remove all remaining whitespace
    return ''.join(code.split())

# Tokenize the code by replacing variable names with a placeholder 'VAR'
def tokenize_code(code):
    # First, clean up the code by removing comments and whitespace
    cleaned_code = remove_comments_and_whitespace(code)
    
    # Use a regular expression to replace all variable-like patterns with 'VAR'
    # This treats any word-like pattern as a variable
    tokenized_code = re.sub(r'\b\w+\b', 'VAR', cleaned_code)
    return tokenized_code

# Normalize the code structure (detect loops, conditionals, etc.)
def normalize_structure(code):
    # Replace control structures with a generic placeholder
    code = re.sub(r'for\s*\(.*?\)', 'FOR_LOOP', code)
    code = re.sub(r'while\s*\(.*?\)', 'WHILE_LOOP', code)
    code = re.sub(r'if\s*\(.*?\)', 'IF_CONDITION', code)
    code = re.sub(r'elif\s*\(.*?\)', 'ELIF_CONDITION', code)
    code = re.sub(r'else\s*\{', 'ELSE_BLOCK', code)
    
    # Return the normalized code for structural comparison
    return code

# Handle batch processing of files against a master file
def batch_process(master_code, files):
    results = []
    flagged_files = []

    for file_code in files:
        # Calculate individual scores
        exact_match_score = detect_exact_match_score(master_code, file_code)
        variable_renaming_score = detect_variable_renaming_score(master_code, file_code)
        structural_similarity_score = detect_structural_similarity_score(master_code, file_code)

        # Calculate average score
        average_score = (exact_match_score + variable_renaming_score + structural_similarity_score) / 3

        result = {
            'filename': file_code['filename'],
            'exact_match_score': exact_match_score,
            'variable_renaming_score': variable_renaming_score,
            'structural_similarity_score': structural_similarity_score,
            'average_score': average_score
        }

        results.append(result)

        # Flag file if average score is above 80%
        if average_score > 80:
            flagged_files.append(file_code['filename'])

    return {'results': results, 'flagged_files': flagged_files}