import React, {
  ChangeEvent,
  FormEvent,
  useCallback,
  useState,
  useLayoutEffect,
  useRef,
  useContext,
  useEffect,
} from 'react';
import styles from './input.module.css';
import RightArrowIcon from '../icons/send.svg';
import { FileUpload } from './fileUpload';
import { UploadedFileDisplay } from './uploadedFileDisplay';
import { Suggestions } from './suggestions';
import { Button } from './button';
import { ChatMessageResponse, uploadFileToServer } from '../server';
import { Role } from './message';
import { MessageType, WebsocketContext } from '../session/websocket-context';

export interface InputProps {
  appendMessage: (
    response: ChatMessageResponse,
    role: Role,
    report?: string,
    sidePanelTitle?: string,
  ) => void;
  sendMessage: (message: string) => void;
  waiting: (isWaiting: boolean) => void;
  isWaiting: boolean;
  suggestions: string[];
}

export const Input = ({
  appendMessage,
  sendMessage,
  waiting,
  suggestions,
  isWaiting,
}: InputProps) => {
  const [userInput, setUserInput] = useState<string>('');
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [uploadInProgress, setUploadInProgress] = useState<boolean>(false);
  const [uploadComplete, setUploadComplete] = useState<boolean>(false);
  const { lastMessage } = useContext(WebsocketContext);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const [currentReportId, setCurrentReportId] = useState<string | null>(null);

  const onChange = useCallback((event: ChangeEvent<HTMLTextAreaElement>) => {
    setUserInput(event.target.value);
  }, []);

  const onSelectedUploadedFile = useCallback(() => {
    if (uploadedFile) setUserInput(userInput + uploadedFile.name);
  }, [uploadedFile, userInput, setUserInput]);

  useLayoutEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      const textareaHeight = textareaRef.current.scrollHeight;

      if (textareaHeight > 110) {
        textareaRef.current.style.height = '110px';
        textareaRef.current.style.overflowY = 'auto';
      } else {
        textareaRef.current.style.height = `${textareaHeight}px`;
        textareaRef.current.style.overflowY = 'hidden';
      }
    }
  }, [userInput]);

  const onSend = useCallback(
    async (event: FormEvent<HTMLElement>) => {
      event.preventDefault();
      if (!isWaiting && userInput.trim().length > 0) {
        setUserInput('');
        waiting(true);

        try {
          await sendMessage(userInput);
          waiting(false);
        } catch (error) {
          console.error(error);
          waiting(false);
        }
      }
    },
    [sendMessage, userInput, isWaiting, waiting],
  );

  const uploadFile = async (file: File) => {
    setUploadInProgress(true);
    setUploadComplete(false);

    try {
      const { id } = await uploadFileToServer(file);
      setCurrentReportId(id);
      setUploadedFile(file);
      setUploadComplete(true);
      waiting(true);
    } catch (error) {
      waiting(false);
      console.error(error);
    } finally {
      setUploadInProgress(false);
    }
  };

  useEffect(() => {
    if (lastMessage) {
      const actualType = Array.isArray(lastMessage.type)
        ? lastMessage.type[0]
        : lastMessage.type;

      if (
        actualType === MessageType.REPORT_COMPLETE &&
        lastMessage.data &&
        currentReportId
      ) {
        const reportData = JSON.parse(lastMessage.data);
        appendMessage(
          {
            id: reportData.id,
            answer: reportData.answer,
          },
          Role.Bot,
          reportData.report,
          `ESG Report - ${reportData.filename}`,
        );
        waiting(false);
        setCurrentReportId(null);
      }
    }
  }, [lastMessage, currentReportId, appendMessage, waiting]);

  return (
    <>
      {uploadedFile && (
        <UploadedFileDisplay
          fileName={uploadedFile.name}
          onClick={onSelectedUploadedFile}
        />
      )}
      <form onSubmit={onSend} className={styles.inputContainer}>
        <div className={styles.inputRow}>
          <div className={styles.parentDiv}>
            <textarea
              className={styles.textarea}
              ref={textareaRef}
              placeholder="Send a Message..."
              value={userInput}
              onChange={onChange}
              rows={1}
              onKeyDown={(event) => {
                if (event.key === 'Enter' && event.shiftKey == false) {
                  onSend(event);
                }
              }}
            />
            <FileUpload
              onFileUpload={uploadFile}
              uploadInProgress={uploadInProgress}
              disabled={!!uploadedFile || uploadInProgress}
              uploadComplete={uploadComplete}
            />
          </div>
          <div className={styles.sendButtonContainer}>
            <Button
              icon={RightArrowIcon}
              disabled={uploadInProgress || isWaiting}
            />
          </div>
        </div>
      </form>
      <Suggestions loadPrompt={setUserInput} suggestions={suggestions} />
    </>
  );
};
