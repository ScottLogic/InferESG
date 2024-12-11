import React from 'react';
import styles from './button.module.css';
import classNames from 'classnames';

interface ButtonProps {
  text?: string;
  icon?: string;
  disabled?: boolean;
  isOutline?: boolean;
  isPressed?: boolean;
  isDownload?: boolean;
  href?: string;
  onClick?: () => void;
}

export const Button = ({
  text,
  icon,
  disabled,
  isOutline,
  isPressed,
  isDownload,
  href,
  onClick,
}: ButtonProps) => {
  const isIconOnly = !text && icon;

  const content = (
    <div
      className={classNames(styles.button_container, {
        [styles.outline]: isOutline,
        [styles.download]: isDownload,
      })}
    >
      <button
        disabled={disabled}
        className={classNames(styles.button, {
          [styles.iconOnly]: isIconOnly,
          [styles.withText]: !isIconOnly,
          [styles.pressed]: isPressed,
        })}
        onClick={onClick}
      >
        {icon && (
          <img
            src={icon}
            className={classNames(styles.iconBaseStyle, {
              [styles.iconOnlyStyle]: isIconOnly,
            })}
          />
        )}
        {text}
      </button>
    </div>
  );

  return href ? <a href={href}>{content}</a> : content;
};
