import React, { useState } from 'react';
import './FileUpload.css';

const FileUpload = () => {
  const [file1, setFile1] = useState(null);
  const [file2, setFile2] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileChange = (setter) => (e) => {
    setter(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append('codeFile1', file1);
    formData.append('codeFile2', file2);

    try {
      const response = await fetch('http://127.0.0.1:5000/check', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Server responded with an error');
      }

      const data = await response.json();
      setResult(data);
    } catch (error) {
      setError('An error occurred while submitting the files. Please try again.');
      console.error('Error during file upload', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="file-upload">
      <h2>Upload Code Files</h2>
      <form onSubmit={handleSubmit}>
        <div className="file-inputs">
          <input type="file" onChange={handleFileChange(setFile1)} className="file-input" />
          <input type="file" onChange={handleFileChange(setFile2)} className="file-input" />
        </div>
        <button type="submit" disabled={!file1 || !file2 || loading} className="submit-button">
          {loading ? 'Processing...' : 'Submit'}
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

export default FileUpload;