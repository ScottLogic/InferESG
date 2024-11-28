import React, { useEffect } from 'react';
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
            <div className={styles.sidepanel}>
              <div className={styles.close_container}>
                <IconButton
                  icon={closeIcon}
                  altText="Close"
                  onClick={() => selectMessage(null)}
                />
              </div>
              <p>id: {selectedMessage.id}</p>
              <p>message: {selectedMessage.content}</p>
              <p>time: {selectedMessage.time}</p>
            </div>
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
            />
          </div>
        </div>
      </div>
    </>
  );
};
