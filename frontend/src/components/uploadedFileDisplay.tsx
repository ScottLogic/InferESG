import React from 'react';
import styles from './uploadedFileDisplay.module.css';
import AttachmentIcon from '../icons/attachment.svg';

interface UploadedFileDisplayProps {
  fileName: string;
  onClick: () => void;
}

export const UploadedFileDisplay = ({
  fileName,
  onClick,
}: UploadedFileDisplayProps) => (
  <div className={styles.uploadedFileContainer}>
    <span
      className={styles.uploadedFile}
      role="button"
      onClick={onClick}
      title="Append the filename to the end of the message"
    >
      <img
        src={AttachmentIcon}
        alt="Attachment"
        className={styles.attachmentIcon}
      />
      {fileName}
    </span>
  </div>
);
