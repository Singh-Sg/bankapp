import React from 'react';
import './App.css';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Tablebank from './components/Tablebank';
import Transfer from './components/Transfer';
import Deposite from './components/Deposite';
import Withdrawal from './components/Withdrawal';
import Showdata from './components/Showdata';

function App() {
  return (
    <Router>
      <div className="App">
        <Tablebank />
        <Routes>
          <Route path="/" element={<Showdata />} />
          <Route path="/transfer" element={<Transfer />} />
          <Route path='/deposite' element={<Deposite />} />
          <Route path='/withdrawal' element={<Withdrawal />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
