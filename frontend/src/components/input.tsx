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
import UploadIcon from '../icons/upload.svg';
import { Suggestions } from './suggestions';
import { Button } from './button';

export interface InputProps {
  sendMessage: (message: string) => void;
  waiting: boolean;
  suggestions: string[];
}

export const Input = ({ sendMessage, waiting, suggestions }: InputProps) => {
  const [userInput, setUserInput] = useState<string>('');
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const onChange = useCallback((event: ChangeEvent<HTMLTextAreaElement>) => {
    setUserInput(event.target.value);
  }, []);

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

  return (
    <>
      <form onSubmit={onSend} className={styles.inputContainer}>
        <div className={styles.parentDiv}>
          <textarea
            className={styles.textarea}
            ref={textareaRef}
            placeholder="Send a Message..."
            value={userInput}
            onChange={onChange}
            rows={1}
          />
          <div className={styles.uploadButton_container}>
            <button className={styles.uploadButton} disabled>
              <img src={UploadIcon} />
            </button>
          </div>
        </div>
        <div className={styles.sendButtonContainer}>
          <Button icon={RightArrowIcon} disabled={waiting} />
        </div>
      </form>
      <Suggestions loadPrompt={setUserInput} suggestions={suggestions} />
    </>
  );
};
