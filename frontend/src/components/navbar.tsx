import React from 'react';
import styles from './navbar.module.css';
import ChatIcon from '../icons/chat.svg';
import { Button } from './button';
import logo from '../icons/primary-logo-dark.svg';

interface NavbarProps {
  startNewConversation: () => void;
}

export const NavBar = ({ startNewConversation }: NavbarProps) => {
  return (
    <div className={styles.container}>
      <div>
        <img src={logo} title="Infer ESG" />
      </div>
      <div>
        <Button
          icon={ChatIcon}
          text="Start new chat"
          onClick={startNewConversation}
        />
      </div>
    </div>
  );
};
