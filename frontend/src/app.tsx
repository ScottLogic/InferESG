import React, { useEffect, useState } from 'react';
import styles from './app.module.css';
import { Chat } from './components/chat';
import { Input } from './components/input';
import { useMessages } from './useMessages';
import { NavBar } from './components/navbar';
import closeIcon from './icons/close.svg';
import { IconButton } from './components/icon-button';

export const App = () => {
  const {
    sendMessage,
    messages,
    waiting,
    suggestions,
    resetMessages,
    initSuggestions,
  } = useMessages();

  const [showSidebar, setShowSidebar] = useState(false);

  useEffect(() => {
    initSuggestions();
  }, []);

  return (
    <>
      <NavBar startNewConversation={resetMessages} />
      <div className={styles.container}>
        {showSidebar && (
          <div className={styles.column}>
            <div className={styles.sidepanel}>
              <div className={styles.close_container}>
                <IconButton
                  icon={closeIcon}
                  altText="Close"
                  onClick={() => setShowSidebar(false)}
                />
              </div>
              <p>Sidebar content</p>
            </div>
          </div>
        )}
        <div className={styles.column}>
          <div className={styles.chatContainer}>
            <Chat messages={messages} waiting={waiting} />
            <Input
              key={messages?.[0]?.time}
              sendMessage={sendMessage}
              waiting={waiting}
              suggestions={suggestions}
            />
          </div>
        </div>
      </div>
    </>
  );
};
