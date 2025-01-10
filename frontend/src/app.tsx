import React, { useEffect, useState } from 'react';
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
    suggestions,
    resetMessages,
    initSuggestions,
    selectMessage,
    selectedMessage,
  } = useMessages();

  const [isWaiting, setWaiting] = useState(false);
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
              waiting={isWaiting}
              setWaiting={setWaiting}
              selectedMessage={selectedMessage}
              selectMessage={selectMessage}
            />
            <Input
              key={messages?.[0]?.time}
              sendMessage={sendMessage}
              suggestions={suggestions}
              appendMessage={appendMessage}
              waiting={setWaiting}
              isWaiting={isWaiting}
            />
          </div>
        </div>
      </div>
    </>
  );
};
