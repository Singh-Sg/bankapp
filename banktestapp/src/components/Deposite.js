import axios from 'axios'
import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { useNavigate } from 'react-router-dom';
const apiInstance = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/',
  headers: {
    'Content-Type': 'application/json',
  },
});
const Deposite = () => {
  const [amount, setAmount] = useState('');
  const [balanced, setBalanced] = useState();
  const [error, setError] = useState(null);
  const { register, handleSubmit } = useForm();
  const navigate = useNavigate()

  const patchDeposite = async (data) => {
    try {
      const response = await apiInstance.patch(`deposit/987654321/`, {
        amount: Number(data.amount),
      });
      setBalanced(response.data.balance);
      navigate("/")
    } catch (error) {
      console.error(error);
      setError(error.message);
    }
  };

  const onSubmit = async (data) => {
    await patchDeposite(data);
  };
  return (
    <div>
      <div class="login-root">
        <div class="box-root flex-flex flex-direction--column" style={{ minHeight: " auto", flexGrow: "1" }}>
          <div class="box-root  flex-flex flex-direction--column" style={{ flexGrow: "1", zIndex: "9" }}>
            <div class="box-root  padding-bottom--24 flex-flex flex-justifyContent--center">
              <h1 style={{ color: "rgb(84, 105, 212)" }}>Deposit</h1>
            </div>
            <div class="formbg-outer">
              <div class="formbg">
                <div class="formbg-inner padding-horizontal--48">
                  <form id="stripe-login" onSubmit={handleSubmit(onSubmit)}>
                    <div class="field padding-bottom--24">
                      <label for="accountNumber">Account number </label>
                      <input type="number" {...register('accountNumber')} />
                    </div>
                    <div class="field padding-bottom--24">
                      <label for="amount">Amount  </label>
                      <input type="number" {...register('amount')} value={amount} onChange={(e) => setAmount(e.target.value)} />
                    </div>
                    <div class="field padding-bottom--24">
                      <input type="submit" name="submit" value="send" />
                    </div>
                    {error && <div style={{ color: 'red' }}>{error}</div>}
                  </form>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Deposite

