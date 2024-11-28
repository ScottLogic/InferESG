import React from 'react';
import styles from './uploadedFileDisplay.module.css';
import AttachmentIcon from '../icons/attachment.svg';

interface UploadedFileDisplayProps {
  fileName: string;
}

export const UploadedFileDisplay = ({ fileName }: UploadedFileDisplayProps) => (
  <div className={styles.uploadedFileContainer}>
    <span className={styles.uploadedFile}>
      <img
        src={AttachmentIcon}
        alt="Attachment"
        className={styles.attachmentIcon}
      />
      {fileName}
    </span>
  </div>
);
