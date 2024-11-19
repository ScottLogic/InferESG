import { useCallback, useState } from 'react';
import { Message, Role } from './components/message';
import { getResponse, getSuggestions, resetChat } from './server';

const starterMessage: Message = {
  role: Role.Bot,
  content: 'Hello, how can I help you?',
  time: new Date().toLocaleTimeString(),
};

export interface UseMessagesHook {
  sendMessage: (message: string) => void;
  resetMessages: () => void;
  initSuggestions: () => void;
  messages: Message[];
  suggestions: string[];
  waiting: boolean;
}

export const useMessages = (): UseMessagesHook => {
  const [waiting, setWaiting] = useState<boolean>(false);
  const [messages, setMessages] = useState<Message[]>([starterMessage]);
  const [suggestions, setSuggestions] = useState<string[]>([]);

  const fetchSuggestions = useCallback(async () => {
    const newSuggestions = await getSuggestions();
    if (Array.isArray(newSuggestions) && newSuggestions.length > 0) {
      setSuggestions(newSuggestions);
    }
  }, []);

  const appendMessage = useCallback((message: string, role: Role) => {
    setMessages((prevMessages) => [
      ...prevMessages,
      { role, content: message, time: new Date().toLocaleTimeString() },
    ]);
  }, []);

  const sendMessage = useCallback(
    async (message: string) => {
      appendMessage(message, Role.User);
      setWaiting(true);
      const response = await getResponse(message);
      setWaiting(false);
      appendMessage(response.message, Role.Bot);
      if (message !== 'healthcheck') {
        fetchSuggestions();
      }
    },
    [appendMessage, messages],
  );

  const resetMessages = useCallback(async () => {
    await resetChat();
    setWaiting(false);
    setMessages([{ ...starterMessage, time: new Date().toLocaleTimeString() }]);
    setSuggestions([]);
    fetchSuggestions();
  }, []);

  return {
    sendMessage,
    messages,
    suggestions,
    waiting,
    resetMessages,
    initSuggestions: fetchSuggestions,
  };
};
