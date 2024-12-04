import React, { useEffect } from 'react';
import styles from './app.module.css';
import { Chat } from './components/chat';
import { Input } from './components/input';
import { useMessages } from './useMessages';
import { NavBar } from './components/navbar';
import closeIcon from './icons/close.svg';
import { IconButton } from './components/icon-button';
import Markdown from 'react-markdown';

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
            <div className={styles.close_container}>
              <h1>{selectedMessage.sidePanelTitle}</h1>
              <IconButton
                icon={closeIcon}
                altText="Close"
                onClick={() => selectMessage(null)}
              />
            </div>
            <hr className={styles.custom_hr} />
            <div className={styles.sidepanel}>
              <div className={styles.markdown_container}>
                <Markdown>{String(selectedMessage.report)}</Markdown>
              </div>
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
              appendMessage={appendMessage}
            />
          </div>
        </div>
      </div>
    </>
  );
};
