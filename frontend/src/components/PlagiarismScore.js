import React from 'react';
import './PlagiarismScore.css';

const PlagiarismScore = ({ result }) => {
  if (!result) return null;

  return (
    <div className="plagiarism-score">
      <h3>Plagiarism Scores:</h3>
      <p>Exact Match: {result.exact_match_score.toFixed(2)}%</p>
      <p>Variable Renaming: {result.variable_renaming_score.toFixed(2)}%</p>
      <p>Structural Similarity: {result.structural_similarity_score.toFixed(2)}%</p>
    </div>
  );
};

export default PlagiarismScore;