import React, { useState } from 'react';
import './TextInput.css';

const TextInput = () => {
  const [code1, setCode1] = useState("");
  const [code2, setCode2] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleChange = (setter) => (e) => {
    setter(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    const requestData = { code1, code2 };

    try {
      const response = await fetch('http://127.0.0.1:5000/check', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData),
      });

      if (!response.ok) {
        throw new Error('Server responded with an error');
      }

      const data = await response.json();
      setResult(data);
    } catch (error) {
      setError("Error during text submission");
      console.error("Error during text submission", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="text-input">
      <h2>Enter Code</h2>
      <form onSubmit={handleSubmit}>
        <textarea
          value={code1}
          onChange={handleChange(setCode1)}
          placeholder="Paste your first code snippet here..."
          className="code-textarea"
        />
        <textarea
          value={code2}
          onChange={handleChange(setCode2)}
          placeholder="Paste your second code snippet here..."
          className="code-textarea"
        />
        <button type="submit" disabled={loading} className="submit-button">
          {loading ? "Processing..." : "Submit"}
        </button>
      </form>
      {error && <p className="error-message">{error}</p>}
      {result && (
        <div className="result">
          <h3>Plagiarism Scores:</h3>
          <p>Exact Match: {result.exact_match_score.toFixed(2)}%</p>
          <p>Variable Renaming: {result.variable_renaming_score.toFixed(2)}%</p>
          <p>Structural Similarity: {result.structural_similarity_score.toFixed(2)}%</p>
        </div>
      )}
    </div>
  );
};

export default TextInput;