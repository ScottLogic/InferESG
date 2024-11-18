import React, { useEffect } from 'react';
import styles from './app.module.css';
import { Chat } from './components/chat';
import { Input } from './components/input';
import { useMessages } from './useMessages';
import { NavBar } from './components/navbar';

export const App = () => {
  const {
    sendMessage,
    messages,
    waiting,
    suggestions,
    resetMessages,
    initSuggestions,
  } = useMessages();

  useEffect(() => {
    initSuggestions();
  }, []);

  return (
    <div className={styles.container}>
      <NavBar startNewConversation={resetMessages} />
      <Chat messages={messages} waiting={waiting} />
      <Input
        key={messages?.[0]?.time}
        sendMessage={sendMessage}
        waiting={waiting}
        suggestions={suggestions}
      />
    </div>
  );
};
