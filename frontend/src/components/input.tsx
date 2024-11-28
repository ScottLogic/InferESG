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
      let { filename, id, report } = await uploadFileToServer(file); //  change to const
      console.log(`File uploaded successfully: ${filename} with id ${id}`);
      report = `# ESG Report Analysis

      ## Basic:
      
      1. **What is the name of the company that this document refers to?**
         - Amazon Web Services EU SARL (UK Branch) (“AWS UK”), part of Amazon.com, Inc. (“Amazon”).
      
      2. **What year or years does the information refer too?**
         - The document refers to the years 2020, 2023, and 2024.
      
      3. **Summarise in one sentence what the document is about?**
         - This document outlines AWS UK's commitment and plans to achieve net-zero emissions by 2040, including their baseline emissions, current emissions reporting, and carbon reduction projects.
      
      ## ESG (Environment, Social, Governance):
      
      1. **Which aspects of ESG does this document primarily discuss, respond with a percentage of each topic covered by the document.**
         - Environmental: 95%
         - Social: 0%
         - Governance: 5%
      
      2. **What aspects of ESG are not discussed in the document?**
         - Social aspects are not discussed in the document.
      
      ## Environmental:
      
      1. **What environmental goals does this document describe?**
         - Achieving net-zero emissions by 2040.
         - Matching 100% of electricity use with renewable energy by 2030 (achieved in 2023).
      
      2. **What beneficial environmental claims does the company make?**
         - Achieved 100% renewable energy for electricity use by 2023, seven years ahead of the target.
         - Implemented various renewable energy projects, including wind and solar farms.
      
      3. **What potential environment greenwashing can you identify that should be fact checked?**
         - The claim of achieving 100% renewable energy use should be verified through independent sources.
         - The impact of the renewable energy projects on local ecosystems and communities should be assessed.
      
      4. **What environmental regulations, standards or certifications can you identify in the document?**
         - PPN 06/21 and associated guidance for Carbon Reduction Plans.
         - GHG Reporting Protocol corporate standard.
         - SECR requirements.
         - Corporate Value Chain (Scope 3) Standard.
      
      ## Social:
      
      1. **What social goals does this document describe?**
         - None
      
      2. **What beneficial societal claims does the company make?**
         - None
      
      3. **What potential societal greenwashing can you identify that should be fact checked?**
         - None
      
      4. **What societal regulations, standards or certifications can you identify in the document?**
         - None
      
      ## Governance:
      
      1. **What governance goals does this document describe?**
         - The document mentions that the Carbon Reduction Plan has been reviewed and signed off by the board of directors.
      
      2. **What beneficial governance claims does the company make?**
         - The company claims to be transparent and shares progress in its annual Sustainability Report.
      
      3. **What potential governance greenwashing can you identify that should be fact checked?**
         - The transparency and accuracy of the annual Sustainability Report should be verified.
         - The involvement of the board of directors in reviewing and signing off the Carbon Reduction Plan should be confirmed.
      
      4. **What governance regulations, standards or certifications can you identify in the document?**
         - The document mentions that it has been completed in accordance with PPN 06/21 and associated guidance for Carbon Reduction Plans.
      
      ## Conclusion:
      
      1. **What is your conclusion about the claims and potential greenwashing in this document?**
         - The document makes significant environmental claims, particularly about achieving net-zero emissions and using 100% renewable energy. While these claims are impressive, they should be independently verified to ensure there is no greenwashing. The governance aspects mentioned are minimal and should also be fact-checked.
      
      2. **What are your recommended next steps to verify any of the claims in this document?**
         - Verify the renewable energy projects and their impacts through independent sources.
         - Confirm the accuracy of the emissions data and the methodology used.
         - Check the transparency and accuracy of the annual Sustainability Report.
         - Confirm the involvement of the board of directors in the review and sign-off process.`;
      setUploadedFile(file);
      appendMessage(
        { answer: 'Your report is ready to view.' },
        Role.Bot,
        report,
      );
    } catch (error) {
      console.error(error);
    } finally {
      setUploadInProgress(false);
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
            <FileUpload
              onFileUpload={uploadFile}
              uploadInProgress={uploadInProgress}
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
