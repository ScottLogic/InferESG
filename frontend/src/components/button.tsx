import React from 'react';
import styles from './button.module.css';

interface ButtonProps {
  text: string;
  icon?: string;
  disabled?: boolean;
  onClick: () => void;
}

export const Button = ({ text, icon, disabled, onClick }: ButtonProps) => {
  return (
    <div className={styles.button_container}>
      <button disabled={disabled} className={styles.button} onClick={onClick}>
        {icon && <img src={icon} className={styles.icon} />}
        {text}
      </button>
    </div>
  );
};
