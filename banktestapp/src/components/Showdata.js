import React, { useState, useEffect } from 'react';
import MUIDataTable from "mui-datatables";
import '../CSS/Showdata.css'
import axios from 'axios';

const Showdata = () => {
  const [dataShow, setDataShow] = useState([]);
  const [filteredData, setFilteredData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedType, setSelectedType] = useState('all');

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        const response = await axios.get("http://127.0.0.1:8000/api/StatementAPIView/987654321/");
        setDataShow(response.data);
        setFilteredData(response.data);
      } catch (error) {
        console.error(error);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const handleFilter = (type) => {
    if (type === 'all') {
      setFilteredData(dataShow);
    } else {
      const filteredData = dataShow.filter(item => item.statement_type === type);
      setFilteredData(filteredData);
    }
    setSelectedType(type);
  };

  const columns = [
    {
      name: "date",
      label: "Date",
      options: {
        filter: true,
        sort: true,
      }
    },
    {
      name: "amount",
      label: "Amount",
      options: {
        filter: true,
        sort: false,
      }
    },
    {
      name: "balance",
      label: "Balance",
      options: {
        filter: true,
        sort: false,
      }
    },
  ];

  const options = {
    filterType: 'checkbox',
    filter: true,
    customToolbar: () => {
      return (
        <div style={{ display: 'flex', alignItems: 'center' }}>
          <select value={selectedType} onChange={(e) => handleFilter(e.target.value)}>
            <option value="all">All filteredData</option>
            <option value="withdrawal">Withdrawal</option>
            <option value="deposit">Deposit</option>
            <option value="transfer">Transfer</option>
          </select>
        </div>
      );
    },
  };

  return (
    <div className='container' style={{ marginLeft: "300px" }}>
      {loading ? (
        <p>Loading...</p>
      ) : (
        <MUIDataTable
          data={filteredData.slice().reverse()}
          columns={columns}
          options={options}
        />
      )}
    </div>
  );
};

export default Showdata;