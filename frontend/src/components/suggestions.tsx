import React from 'react';
import styles from './suggestions.module.css';

export interface SuggestionsProps {
  suggestions: string[];
  loadPrompt: (suggestion: string) => void;
}

export const Suggestions = ({ loadPrompt, suggestions }: SuggestionsProps) => {
  return (
    <div className={styles.container}>
      {suggestions.map((suggestion, index) => (
        <p key={index} onClick={() => loadPrompt(suggestion)}>
          {suggestion}
        </p>
      ))}
    </div>
  );
};
