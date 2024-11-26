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
import { FileUploader } from './fileUploader';
import { UploadedFileDisplay } from './uploadedFileDisplay';
import { Suggestions } from './suggestions';
import { Button } from './button';

export interface InputProps {
  sendMessage: (message: string) => void;
  waiting: boolean;
  suggestions: string[];
}

export const Input = ({ sendMessage, waiting, suggestions }: InputProps) => {
  const [userInput, setUserInput] = useState<string>('');
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState<boolean>(false);
  const [isUploaded, setIsUploaded] = useState<boolean>(false);
  // TODO: Add fileId to the state
  // const [fileId, setFileId] = useState<string>('');
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

  const uploadFile = async (file: File) => {
    setIsUploading(true);
    setIsUploaded(false);

    try {
      const formData = new FormData();
      formData.append('file', file);
      const response = await fetch(`${process.env.BACKEND_URL}/uploadfile`, {
        method: 'POST',
        body: formData,
        credentials: 'include',
      });
      if (!response.ok) throw new Error(`Upload failed with status ${response.status}`);
      
      const { filename, id } = await response.json();
      console.log(`File uploaded successfully: ${filename} with id ${id}`);
      // TODO: Set fileId in the state
      // setFileId(id);
      setUploadedFile(file);
      setIsUploading(false);
      setIsUploaded(true);
    } catch (error) {
      setIsUploading(false);
      console.error(error);
    }
  };

  
  return (
    <>
      {uploadedFile && <UploadedFileDisplay fileName={uploadedFile.name} />}
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
            />

            <FileUploader
              onFileUpload={uploadFile}
              isUploading={isUploading}
              isUploaded={isUploaded}
              disabled={!!uploadedFile}
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
