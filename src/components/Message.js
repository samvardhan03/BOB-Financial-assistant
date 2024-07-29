import React from 'react';
import './Message.css';

const Message = ({ message }) => {
  return (
    <div className={`message ${message.sender}`}>
      {message.text}
    </div>
  );
};

export default Message;
