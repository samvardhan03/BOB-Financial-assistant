import React from 'react';
import logo from './logo.png';
import Chat from './components/Chat';
import './App.css';

const App = () => {
  return (
    <div className="app">
      <header className="app-header">
        <img src={logo} className="app-logo" alt="logo" />
        <h1>BOB</h1>
        <h2>Your AI powered financial assistant</h2>
      </header>
      <div className="chat-wrapper">
        <Chat />
      </div>
    </div>
  );
};

export default App;

