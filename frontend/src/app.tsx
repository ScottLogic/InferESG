import React, { useEffect } from 'react';
import styles from './app.module.css';
import { Chat } from './components/chat';
import { Input } from './components/input';
import { useMessages } from './useMessages';
import { NavBar } from './components/navbar';
import { Sidebar } from './components/sidebar';

export const App = () => {
  const {
    appendMessage,
    sendMessage,
    messages,
    waiting,
    suggestions,
    resetMessages,
    initSuggestions,
    selectMessage,
    selectedMessage,
  } = useMessages();

  useEffect(() => {
    initSuggestions();
  }, []);

  return (
    <>
      <NavBar startNewConversation={resetMessages} />
      <div className={styles.container}>
        {selectedMessage && (
          <div className={styles.column}>
            <Sidebar
              selectedMessage={selectedMessage}
              selectMessage={selectMessage}
            />
          </div>
        )}
        <div className={styles.column}>
          <div className={styles.chatContainer}>
            <Chat
              messages={messages}
              waiting={waiting}
              selectedMessage={selectedMessage}
              selectMessage={selectMessage}
            />
            <Input
              key={messages?.[0]?.time}
              sendMessage={sendMessage}
              waiting={waiting}
              suggestions={suggestions}
              appendMessage={appendMessage}
            />
          </div>
        </div>
      </div>
    </>
  );
};
