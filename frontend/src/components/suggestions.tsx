import React, { useRef, useState, useEffect, useCallback } from 'react';
import styles from './suggestions.module.css';

export interface SuggestionsProps {
  suggestions: string[];
  loadPrompt: (suggestion: string) => void;
}

export const Suggestions = ({ loadPrompt, suggestions }: SuggestionsProps) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const [isScrollable, setIsScrollable] = useState(false);

  const checkScrollable = useCallback(() => {
    const container = containerRef.current;
    if (container) {
      const computedStyle = window.getComputedStyle(container);
      const paddingRight = parseFloat(computedStyle.paddingRight) || 0;

      const hasOverflow = container.scrollWidth > container.offsetWidth;
      const isAtEnd =
        container.scrollLeft + container.offsetWidth >=
        container.scrollWidth - paddingRight;

      setIsScrollable(hasOverflow && !isAtEnd);
    }
  }, []);

  useEffect(() => {
    checkScrollable();
    const handleResize = () => checkScrollable();
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, [suggestions, checkScrollable]);

  return (
    <div>
      <p className={styles.decorativeText}>Suggested questions</p>
      <div className={styles.contentWrapper}>
        <div
          className={styles.container}
          ref={containerRef}
          onScroll={checkScrollable}
        >
          {suggestions.map((suggestion, index) => (
            <div
              key={index}
              onClick={() => loadPrompt(suggestion)}
              className={styles.suggestionItem}
            >
              <p className={styles.suggestionText}>{suggestion}</p>
            </div>
          ))}
        </div>
        <div
          className={`${styles.gradient} ${!isScrollable ? styles.hidden : ''}`}
        ></div>
      </div>
    </div>
  );
};
