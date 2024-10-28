import React, { useEffect, useState } from 'react';
import styles from './suggestions.module.css';
import { getSuggestions } from '../server';

export interface SuggestionsProps {
  loadPrompt: (suggestion: string) => void;
  waiting: boolean;
}

export const Suggestions = ({ loadPrompt, waiting }: SuggestionsProps) => {
  const [suggestions, setSuggestions] = useState<string[]>([]);

  useEffect(() => {
    const fetchSuggestions = async () => {
      if (!waiting) {
        const newSuggestions = await getSuggestions();
        if (Array.isArray(newSuggestions) && newSuggestions.length > 0) {
          setSuggestions(newSuggestions);
        }
      }
    };
    fetchSuggestions();
  }, [waiting]);

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
