import React, { useState } from 'react';
import axios from 'axios';
import { Upload, FileText, AlertTriangle, CheckCircle, X } from 'lucide-react';
import './BatchUpload.css';

const BatchUpload = () => {
  const [masterFile, setMasterFile] = useState(null);
  const [files, setFiles] = useState([]);
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [flaggedFiles, setFlaggedFiles] = useState([]);

  const handleMasterFileChange = (e) => {
    setMasterFile(e.target.files[0]);
  };

  const handleFilesChange = (e) => {
    setFiles(Array.from(e.target.files));
  };

  const removeFile = (index) => {
    setFiles(files.filter((_, i) => i !== index));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('masterFile', masterFile);
    files.forEach(file => formData.append('files[]', file));
    
    setLoading(true);
    setError(null);

    try {
      const response = await axios.post('http://127.0.0.1:5000/batch_check', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setResults(response.data.results);
      setFlaggedFiles(response.data.flagged_files);
    } catch (error) {
      setError('An error occurred while submitting the files. Please try again.');
      console.error('Error during file upload', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="batch-upload">
      <h2>Batch Plagiarism Check</h2>
      <form onSubmit={handleSubmit}>
        <div className="file-upload-section">
          <div className="file-input master-file">
            <label htmlFor="masterFile">
              <Upload size={24} />
              <span>{masterFile ? masterFile.name : 'Upload Master File'}</span>
            </label>
            <input
              id="masterFile"
              type="file"
              onChange={handleMasterFileChange}
              accept=".py,.js,.java,.cpp"
              hidden
            />
          </div>
          <div className="file-input comparison-files">
            <label htmlFor="batchFiles">
              <FileText size={24} />
              <span>Upload Comparison Files</span>
            </label>
            <input
              id="batchFiles"
              type="file"
              onChange={handleFilesChange}
              accept=".py,.js,.java,.cpp"
              multiple
              hidden
            />
          </div>
        </div>
        {files.length > 0 && (
          <div className="file-list">
            <h3>Selected Files:</h3>
            <ul>
              {files.map((file, index) => (
                <li key={index}>
                  <FileText size={16} />
                  <span>{file.name}</span>
                  <button type="button" onClick={() => removeFile(index)}>
                    <X size={16} />
                  </button>
                </li>
              ))}
            </ul>
          </div>
        )}
        <button className="submit-button" type="submit" disabled={!masterFile || files.length === 0 || loading}>
          {loading ? 'Processing...' : 'Start Plagiarism Check'}
        </button>
      </form>

      {error && (
        <div className="message error">
          <AlertTriangle size={24} />
          <p>{error}</p>
        </div>
      )}

      {results && (
        <div className="results">
          <h3>Plagiarism Check Results</h3>
          {results.map((result, index) => (
            <div key={index} className={`result-item ${flaggedFiles.includes(result.filename) ? 'flagged' : ''}`}>
              <h4>
                <FileText size={18} />
                {result.filename}
                {flaggedFiles.includes(result.filename) && (
                  <span className="flag">
                    <AlertTriangle size={18} />
                    Flagged
                  </span>
                )}
              </h4>
              <div className="scores">
                <ScoreBar label="Exact Match" score={result.exact_match_score} />
                <ScoreBar label="Variable Renaming" score={result.variable_renaming_score} />
                <ScoreBar label="Structural Similarity" score={result.structural_similarity_score} />
                <ScoreBar label="Average" score={result.average_score} />
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

const ScoreBar = ({ label, score }) => (
  <div className="score-bar">
    <span className="label">{label}</span>
    <div className="bar">
      <div className="fill" style={{ width: `${score}%` }}></div>
    </div>
    <span className="score">{score.toFixed(2)}%</span>
  </div>
);

export default BatchUpload;