import pandas as pd
import re
#from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score


# Example dataset: list of code snippets, with label "1" for obfuscated and "0" for clean
data = {
    "code": [
        "def calculate(a, b): return a + b",  # Clean
        "def XxYY(aAB, bXY): return aAB ** bXY + 2",  # Slightly obfuscated
        "for i in range(0, len(arr)): sum=sum+arr[i]",  # Clean
        "for XxYx in range(0, len(arr)): sumYYX += arrXyX[XxYx]",  # Obfuscated
        "var _0x1f = ['a', 'b', 'c'];",  # Obfuscated JS
        "sum(map(int, numbers))"  # Clean
    ],
    "label": [0, 1, 0, 1, 1, 0]
}

df = pd.DataFrame(data)
print(df.head())

# Function to calculate average length of variables or identifiers
def avg_variable_length(code):
    tokens = re.findall(r'\b\w+\b', code)
    return sum(len(token) for token in tokens) / len(tokens) if tokens else 0

# Function to detect presence of typical obfuscation patterns
def has_obfuscation_pattern(code):
    obfuscation_patterns = [r'_0x[a-fA-F0-9]', r'[A-Za-z]{2,}\d+[A-Za-z]*']  # Obfuscated patterns
    return any(re.search(pattern, code) for pattern in obfuscation_patterns)

# Feature extraction
df['avg_var_len'] = df['code'].apply(avg_variable_length)
df['has_obf_pattern'] = df['code'].apply(has_obfuscation_pattern)
print(df[['code', 'avg_var_len', 'has_obf_pattern']])


# Features (you can add more based on token analysis, entropy, etc.)
X = df[['avg_var_len', 'has_obf_pattern']].astype(float)
y = df['label']

# Split dataset into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Train Logistic Regression model
model = LogisticRegression()
model.fit(X_train, y_train)

# Predict and evaluate
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
# print(f"Model Accuracy: {accuracy * 100:.2f}%")
# New code to test for obfuscation
test_code = ("def multiply(a, b): return a * b")

# Extract features
new_features = pd.DataFrame({
    'avg_var_len': [avg_variable_length(test_code)],
    'has_obf_pattern': [has_obfuscation_pattern(test_code)]
})

# Predict obfuscation
is_obfuscated = model.predict(new_features)
print(f"Is the code obfuscated? {'Yes' if is_obfuscated[0] else 'No'}")