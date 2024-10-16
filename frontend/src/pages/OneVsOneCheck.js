import React from 'react';
import FileUpload from '../components/FileUpload';
import TextInput from '../components/TextInput';
import './OneVsOneCheck.css';

const OneVsOneCheck = () => {
  return (
    <div className="one-vs-one-check">
      <div className="check-card">
        <h1 className="card-title">1 vs 1 Plagiarism Check</h1>
        <p className="card-description">
          Upload a file or enter text to compare for plagiarism.
        </p>
        <div className="check-content">
          <FileUpload />
          <div className="divider"></div>
          <TextInput />
        </div>
      </div>
    </div>
  );
};

export default OneVsOneCheck;