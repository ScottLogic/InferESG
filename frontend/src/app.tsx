import React from 'react';
import styles from './app.module.css';
import { Chat } from './components/chat';
import { Input } from './components/input';
import { useMessages } from './useMessages';
import { NavBar } from './components/navbar';

export const App = () => {
  const { sendMessage, messages, waiting } = useMessages();

  return (
    <div className={styles.container}>
      <NavBar />
      <Chat messages={messages} waiting={waiting} />
      <Input sendMessage={sendMessage} waiting={waiting} />
    </div>
  );
};
