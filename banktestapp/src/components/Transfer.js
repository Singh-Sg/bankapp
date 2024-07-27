import React from "react";
import '../CSS/Tranfer.css';
import axios from "axios";
import { useNavigate } from 'react-router-dom';

const Transfer = () => {
  const [transferData, setTransferData] = React.useState({
    amount: '',
    from_account: '',
    to_account: ''
  });
  const navigate = useNavigate()
  const handleChange = (e) => {
    setTransferData({ ...transferData, [e.target.name]: e.target.value });
  };

  const postTransfer = (e) => {
    e.preventDefault();
    const payload = {
      amount: Number(transferData.amount),
      from_account: Number(transferData.from_account),
      to_account: Number(transferData.to_account)
    };

    axios.post("http://127.0.0.1:8000/api/transfer/", payload)
      .then((response) => {
        console.log("Response of post transfer API is:", response);
        navigate("/")
      })
      .catch((error) => {
        console.error("Error in post transfer API:", error);
      });
  };

  return (
    <React.Fragment>
      <div className="login-root">
        <div className="box-root flex-flex flex-direction--column" style={{ minHeight: "auto", flexGrow: 1 }}>
          <div className="box-root flex-flex flex-direction--column" style={{ flexGrow: 1, zIndex: 9 }}>
            <div className="box-root padding-bottom--24 flex-flex flex-justifyContent--center">
              <h1 style={{ color: "rgb(84, 105, 212)" }}>Transfer</h1>
            </div>
            <div className="formbg-outer">
              <div className="formbg">
                <div className="formbg-inner padding-horizontal--48">
                  <form id="stripe-login" onSubmit={postTransfer}>
                    <div className="field padding-bottom--24">
                      <label htmlFor="amount">Amount</label>
                      <input type="number" name="amount" value={transferData.amount} onChange={handleChange} required />
                    </div>
                    <div className="field padding-bottom--24">
                      <label htmlFor="from_account">From Account</label>
                      <input type="number" name="from_account" value={transferData.from_account} onChange={handleChange} required />
                    </div>
                    <div className="field padding-bottom--24">
                      <label htmlFor="to_account">To Account</label>
                      <input type="number" name="to_account" value={transferData.to_account} onChange={handleChange} required />
                    </div>
                    <div className="field padding-bottom--24">
                      <input type="submit" name="submit" value="Transfer" />
                    </div>
                  </form>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </React.Fragment>
  );
}

export default Transfer;
