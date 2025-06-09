import logo from './BMW_logo.png';
import './App.css';
import React, { useState } from 'react';
import PredictionModal from './PredictionModal'; // Import the PredictionModal component

function App() {
  const [isModalOpen, setIsModalOpen] = useState(false);

  const openModal = () => setIsModalOpen(true);
  const closeModal = () => setIsModalOpen(false);

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          BMW Car Price Predictor
        </p>
        <button onClick={openModal} style={{padding: '10px 20px', fontSize: '16px'}}>
          Open Price Predictor
        </button>
      </header>
      <PredictionModal isOpen={isModalOpen} onClose={closeModal} />
    </div>
  );
}

export default App;
