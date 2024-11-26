import React from 'react';
import styles from './icon-button.module.css';

interface IconButtonProps {
  altText?: string;
  icon?: string;
  disabled?: boolean;
  onClick?: () => void;
}

export const IconButton = ({
  altText,
  icon,
  disabled,
  onClick,
}: IconButtonProps) => {
  return (
    <div className={styles.iconButton_container}>
      <button
        disabled={disabled}
        type="button"
        className={styles.iconButton}
        onClick={onClick}
      >
        <img src={icon} className={styles.iconButton} alt={altText} />
      </button>
    </div>
  );
};
