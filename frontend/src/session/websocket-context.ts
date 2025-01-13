import { createContext } from 'react';

export enum MessageType {
  PING = 'ping',
  CHAT = 'chat',
  IMAGE = 'image',
  CONFIRMATION = 'confirmation',
  REPORT_IN_PROGRESS = 'report:in-progress',
  REPORT_COMPLETE = 'report:complete',
  REPORT_CANCELLED = 'report:cancelled',
  REPORT_FAILED = 'report:failed',
}

export interface Message {
  type: MessageType;
  data?: string;
}

export interface Connection {
  isConnected: boolean;
  lastMessage: Message | null;
  send: (message: Message) => void;
}

export const WebsocketContext = createContext<Connection>({
  isConnected: false,
  lastMessage: null,
  send: () => {},
});
