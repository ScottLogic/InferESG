import React, { ChangeEvent, useState } from 'react';
import styles from './fileUploader.module.css';
import UploadIcon from '../icons/upload.svg';
import UploadInProgressIcon from '../icons/upload-in-progress.svg';
import CheckCircleIcon from '../icons/check-circle.svg';

interface FileUploaderProps {
  onFileUpload: (file: File) => Promise<void>;
  isUploading: boolean;
  isUploaded: boolean;
  disabled: boolean;
}

export const FileUploader = ({
  onFileUpload,
  isUploading,
  isUploaded,
  disabled,
}: FileUploaderProps) => {
  const [showTooltip, setShowTooltip] = useState<boolean>(false);

  const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      onFileUpload(file);
    }
  };

  const tooltipContent = disabled ? (
    <>
      <p>You already uploaded one file.</p>
      <p>You can upload a different file by starting a new chat.</p>
      <p>Starting a new chat will reset your existing conversation history.</p>
    </>
  ) : (
    <p>You can only upload one .csv, .pdf or .txt file to this chat.</p>
  );

  return (
    <div
      className={styles.uploadButton_container}
      onMouseEnter={() => setShowTooltip(true)}
      onMouseLeave={() => setShowTooltip(false)}
    >
      <label className={styles.uploadButton}>
        {isUploading ? (
          <img src={UploadInProgressIcon} alt="Uploading..." />
        ) : isUploaded ? (
          <img src={CheckCircleIcon} alt="Upload Complete" />
        ) : (
          <img src={UploadIcon} alt="Upload" />
        )}
        <input
          type="file"
          accept=".csv, .pdf, .txt"
          onChange={handleFileChange}
          style={{ display: 'none' }}
          disabled={disabled}
        />
      </label>
      {showTooltip && <div className={styles.tooltip}>{tooltipContent}</div>}
    </div>
  );
};
