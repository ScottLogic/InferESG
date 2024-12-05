import { useCallback, useState } from 'react';
import { Message, Role } from './components/message';
import {
  ChatMessageResponse,
  getResponse,
  getSuggestions,
  resetChat,
} from './server';

const botMessage = `Hello. I am InferESG and I can help you analyse a company's sustainability messaging and detect potential greenwashing. 

To start, upload a document with corporate sustainability messaging and I will analyse the file and create a report about it. My report will review the Environment, Social and Governance content, surface the sustainability statements that are most relevant to the company's industry and flag possible cases of greenwashing for you to investigate further. 

Notes:  I cannot definitively determine what is or is not greenwashing, it is up to you to determine what is greenwashing based on available evidence.

You will always be able to see how I came to my answers by clicking on the "How I came to this conclusion" button in my answers.

I work best with larger files such as Sustainability Reports.
`;

const starterMessage: Message = {
  role: Role.Bot,
  content: botMessage,
  time: new Date().toLocaleTimeString(),
};

export interface UseMessagesHook {
  appendMessage: (response: ChatMessageResponse, role: Role) => void;
  sendMessage: (message: string) => void;
  resetMessages: () => void;
  initSuggestions: () => void;
  selectMessage: (message: Message | null) => void;
  messages: Message[];
  suggestions: string[];
  waiting: boolean;
  selectedMessage: Message | null;
}

export const useMessages = (): UseMessagesHook => {
  const [waiting, setWaiting] = useState<boolean>(false);
  const [messages, setMessages] = useState<Message[]>([starterMessage]);
  const [suggestions, setSuggestions] = useState<string[]>([]);
  const [selectedMessage, selectMessage] = useState<Message | null>(null);

  const fetchSuggestions = useCallback(async () => {
    const newSuggestions = await getSuggestions();
    if (Array.isArray(newSuggestions) && newSuggestions.length > 0) {
      setSuggestions(newSuggestions);
    }
  }, []);

  const appendMessage = useCallback(
    (
      response: ChatMessageResponse,
      role: Role,
      report?: string,
      sidePanelTitle?: string,
    ) => {
      setMessages((prevMessages) => [
        ...prevMessages,
        {
          role,
          id: response.id,
          content: response.answer,
          reasoning: response.reasoning,
          time: new Date().toLocaleTimeString(),
          report,
          sidePanelTitle,
        },
      ]);
    },
    [],
  );

  const sendMessage = useCallback(
    async (message: string) => {
      appendMessage({ answer: message }, Role.User);
      setWaiting(true);
      const response = await getResponse(message);
      setWaiting(false);
      appendMessage(response, Role.Bot);
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
    appendMessage,
    sendMessage,
    messages,
    suggestions,
    waiting,
    resetMessages,
    initSuggestions: fetchSuggestions,
    selectedMessage,
    selectMessage,
  };
};
