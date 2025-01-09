import React, {
  ChangeEvent,
  FormEvent,
  useCallback,
  useState,
  useLayoutEffect,
  useRef,
} from 'react';
import styles from './input.module.css';
import RightArrowIcon from '../icons/send.svg';
import { FileUpload } from './fileUpload';
import { UploadedFileDisplay } from './uploadedFileDisplay';
import { Suggestions } from './suggestions';
import { Button } from './button';
import { ChatMessageResponse, uploadFileToServer } from '../server';
import { Role } from './message';

export interface InputProps {
  appendMessage: (
    response: ChatMessageResponse,
    role: Role,
    report?: string,
    sidePanelTitle?: string,
  ) => void;
  sendMessage: (message: string) => void;
  waiting: boolean;
  suggestions: string[];
}

export const Input = ({
  appendMessage,
  sendMessage,
  waiting,
  suggestions,
}: InputProps) => {
  const [userInput, setUserInput] = useState<string>('');
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [uploadInProgress, setUploadInProgress] = useState<boolean>(false);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

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
    (event: FormEvent<HTMLElement>) => {
      event.preventDefault();
      if (!waiting && userInput.trim().length > 0) {
        sendMessage(userInput);
        setUserInput('');
      }
    },
    [sendMessage, userInput, waiting],
  );

  const uploadFile = async (file: File) => {
    setUploadInProgress(true);

    try {
      const { filename, report, id, answer } = await uploadFileToServer(file);
      setUploadedFile(file);
      appendMessage(
        {
          id,
          answer,
        },
        Role.Bot,
        report,
        `ESG Report - ${filename}`,
      );
    } catch (error) {
      console.error(error);
    } finally {
      setUploadInProgress(false);
    }
  };

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
            />
          </div>
          <div className={styles.sendButtonContainer}>
            <Button icon={RightArrowIcon} disabled={waiting} />
          </div>
        </div>
      </form>
      <Suggestions loadPrompt={setUserInput} suggestions={suggestions} />
    </>
  );
};
