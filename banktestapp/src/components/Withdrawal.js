import React, { useState } from 'react';
import '../CSS/Withdrawal.css';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const Withdrawal = () => {
  const [accountNumber, setAccountNumber] = useState('');
  const [amount, setAmount] = useState('');
  const [pin, setPin] = useState('');
  const [withdrawalData, setWithdrawalData] = useState(null);
  const [error, setError] = useState('');
  const navigate = useNavigate()

  const patchWithdrawal = async (event) => {
    event.preventDefault();
    try {
      console.log('Sending patch request...');
      const response = await axios.patch(`http://127.0.0.1:8000/api/withdrawal/987654321/`, {
        amount: Number(amount),
        pin: Number(pin)
      });
      console.log('Response received:', response.data);
      setWithdrawalData(response.data);
      navigate("/")

    } catch (error) {
      console.error('Error:', error);
      setError('An error occurred while processing the withdrawal. Please try again.');
    }
  };

  return (
    <div>
      <div className="login-root">
        <div className="box-root flex-flex flex-direction--column" style={{ minHeight: "auto", flexGrow: "1" }}>
          <div className="box-root flex-flex flex-direction--column" style={{ flexGrow: "1", zIndex: "9" }}>
            <div className="box-root padding-bottom--24 flex-flex flex-justifyContent--center">
              <h1 style={{ color: "rgb(84, 105, 212)" }}>Withdrawal</h1>
            </div>
            <div className="formbg-outer">
              <div className="formbg">
                <div className="formbg-inner padding-horizontal--48">
                  <form id="stripe-login" onSubmit={patchWithdrawal}>
                    <div className="field padding-bottom--24">
                      <label htmlFor="number" className="label-inline">Account number</label>
                      <input
                        type="number"
                        name="number"
                        className="input-inline"
                        value={accountNumber}
                        onChange={(event) => setAccountNumber(event.target.value)}
                      />
                    </div>
                    <div className="field padding-bottom--24">
                      <label htmlFor="amount" className="label-inline">Amount</label>
                      <input
                        type="number"
                        name="amount"
                        className="input-inline"
                        value={amount}
                        onChange={(event) => setAmount(event.target.value)}
                      />
                    </div>
                    <div className="field padding-bottom--24">
                      <label htmlFor="pin" className="label-inline">PIN</label>
                      <input
                        type="number"
                        name="pin"
                        className="input-inline"
                        value={pin}
                        onChange={(event) => setPin(event.target.value)}
                      />
                    </div>
                    <div className="field padding-bottom--24">
                      <input type="submit" name="submit" value="ok" />
                    </div>
                  </form>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      {error && (
        <div style={{ color: 'red' }}>
          <p>{error}</p>
        </div>
      )}
      {withdrawalData && (
        <div>
          <h2>Withdrawal Data:</h2>
          <p>Balance: {withdrawalData.balance}</p>
          <p>PIN: {withdrawalData.pin}</p>
        </div>
      )}
    </div>
  );
};

export default Withdrawal;
