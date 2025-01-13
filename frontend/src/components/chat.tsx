import React, { useContext, useEffect, useState } from 'react';
import { Message, MessageComponent } from './message';
import styles from './chat.module.css';
import { Waiting } from './waiting';
import {
  WebsocketContext,
  MessageType,
  Message as wsMessage,
} from '../session/websocket-context';
import { Confirmation, ConfirmModal } from './confirm-modal';

export interface ChatProps {
  messages: Message[];
  waiting: boolean;
  setWaiting: (isWaiting: boolean) => void;
  selectedMessage: Message | null;
  selectMessage: (message: Message | null) => void;
}

const mapWsMessageToConfirmation = (
  message: wsMessage,
): Confirmation | undefined => {
  if (!message.data) {
    return;
  }
  const parts = message.data.split(':');
  return { id: parts[0], requestMessage: parts[1], result: null };
};

export const Chat = ({
  messages,
  waiting,
  setWaiting,
  selectedMessage,
  selectMessage,
}: ChatProps) => {
  const containerRef = React.useRef<HTMLDivElement>(null);
  const { lastMessage, send } = useContext(WebsocketContext);
  const [chart, setChart] = useState<string | undefined>(undefined);
  const [confirmation, setConfirmation] = useState<Confirmation | null>(null);

  useEffect(() => {
    if (lastMessage) {
      switch (lastMessage.type) {
        case MessageType.REPORT_IN_PROGRESS:
          setWaiting(true);
          break;
        case MessageType.REPORT_COMPLETE:
          setWaiting(false);
          break;
        case MessageType.REPORT_CANCELLED:
          setWaiting(false);
          break;
        case MessageType.REPORT_FAILED:
          setWaiting(false);
          break;
        case MessageType.IMAGE: {
          const imageData = `data:image/png;base64,${lastMessage.data}`;
          setChart(imageData);
          break;
        }
        case MessageType.CONFIRMATION: {
          const newConfirmation = mapWsMessageToConfirmation(lastMessage);
          if (newConfirmation) setConfirmation(newConfirmation);
          break;
        }
        default:
          break;
      }
    }
  }, [lastMessage, setWaiting]);

  useEffect(() => {
    if (containerRef.current) {
      containerRef.current.scrollTo(0, containerRef.current.scrollHeight);
    }
  }, [messages.length]);

  return (
    <>
      <ConfirmModal
        confirmation={confirmation}
        setConfirmation={setConfirmation}
        send={send}
      />
      <div ref={containerRef} className={styles.container}>
        {messages.map((message, index) => (
          <MessageComponent
            key={index}
            message={message}
            selectedMessage={selectedMessage}
            selectMessage={selectMessage}
          />
        ))}
        {chart && <img src={chart} alt="Generated chart" />}
        {waiting && <Waiting />}
      </div>
    </>
  );
};
