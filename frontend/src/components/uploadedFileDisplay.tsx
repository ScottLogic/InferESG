import React, { useState } from 'react';
import styles from './uploadedFileDisplay.module.css';
import AttachmentIcon from '../icons/attachment.svg';
import { Tooltip } from './tooltip';

interface UploadedFileDisplayProps {
  fileName: string;
  onClick: () => void;
}

export const UploadedFileDisplay = ({
  fileName,
  onClick,
}: UploadedFileDisplayProps) => {
  const [showTooltip, setShowTooltip] = useState<boolean>(false);

  return (
    <div className={styles.uploadedFileContainer}>
      <div className={styles.uploadedFileTooltipContainer}>
        <span
          className={styles.uploadedFile}
          role="button"
          onClick={onClick}
          onMouseEnter={() => setShowTooltip(true)}
          onMouseLeave={() => setShowTooltip(false)}
        >
          <img
            src={AttachmentIcon}
            alt="Attachment"
            className={styles.attachmentIcon}
          />
          {fileName}
        </span>
        {showTooltip && (
          <Tooltip>
            <p>Append the filename to the end of the message</p>
          </Tooltip>
        )}
      </div>
    </div>
  );
};
