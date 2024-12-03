import React from 'react';
import Markdown from 'react-markdown';
import { Message } from './message';
import closeIcon from '../icons/close.svg';
import { IconButton } from './icon-button';
import { DataGrid } from './data-grid';

import styles from './sidebar.module.css';

interface SidebarProps {
  selectedMessage: Message;
  selectMessage: (message: Message | null) => void;
}

export const Sidebar = ({ selectedMessage, selectMessage }: SidebarProps) => {
  const { report, dataset, sidePanelTitle } = selectedMessage;

  return (
    <>
      {report && (
        <>
          <div className={styles.close_container}>
            <h1>{sidePanelTitle}</h1>
            <IconButton
              icon={closeIcon}
              altText="Close"
              onClick={() => selectMessage(null)}
            />
          </div>
          <hr className={styles.custom_hr} />
          <div className={styles.sidepanel}>
            <div className={styles.markdown_container}>
              <Markdown>{String(report)}</Markdown>
            </div>
          </div>
        </>
      )}
      {dataset && (
        <>
          <div className={styles.standalone_close_container}>
            <IconButton
              icon={closeIcon}
              altText="Close"
              onClick={() => selectMessage(null)}
            />
          </div>
          <DataGrid dataset={dataset} />
        </>
      )}
    </>
  );
};
