import React from 'react';
import styles from './tooltip.module.css';

interface Props {
  children: React.ReactNode;
}

export const Tooltip = ({ children }: Props) => (
  <div className={styles.tooltip}>{children}</div>
);
