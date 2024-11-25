import classNames from 'classnames';
import React, { useState } from 'react';
import styles from './message.module.css';
import UserIcon from '../icons/account-circle.svg';
import BotIcon from '../icons/logomark.svg';
import ChevronIcon from '../icons/chevron.svg';

export enum Role {
  User = 'User',
  Bot = 'Bot',
}

export interface Message {
  id?: string;
  role: Role;
  content: string;
  reasoning?: string;
  time: string;
}

export interface MessageProps {
  message: Message;
}

export interface MessageStyle {
  icon: string;
  class: string;
}

const roleStyleMap: Record<Role, MessageStyle> = {
  [Role.User]: {
    icon: UserIcon,
    class: styles.user,
  },
  [Role.Bot]: {
    icon: BotIcon,
    class: styles.bot,
  },
};

export const MessageComponent = ({ message }: MessageProps) => {
  const { content, role, reasoning } = message;

  const { class: roleClass, icon } = roleStyleMap[role];

  const [expanded, setExpanded] = useState(false);

  return (
    <div className={classNames(styles.container, roleClass)}>
      <div className={styles.message_container}>
        <img src={icon} className={styles.iconStyle} />
        <p className={styles.messageStyle}>{content}</p>
      </div>
      {role == Role.Bot && reasoning && (
        <>
          <div
            className={classNames(styles.reasoning_header, {
              [styles.reasoning_header_expanded]: expanded,
            })}
            role="button"
            tabIndex={0}
            onClick={() => setExpanded(!expanded)}
            onKeyDown={(event) => {
              if (event.key === 'Enter' || event.key === ' ') {
                setExpanded(!expanded);
              }
            }}
          >
            How I came to this conclusion
            <img className={styles.expandIcon} src={ChevronIcon} />
          </div>
          {expanded && <div className={styles.reason}>{reasoning}</div>}
        </>
      )}
    </div>
  );
};
