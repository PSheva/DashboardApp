import React, { useEffect, useState } from 'react';
import AccountBox from './AccountBox';

const Dashboard = () => {
    const [dashboardData, setDashboardData] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchData = () => {
            fetch('http://127.0.0.1:8000/dashboard-data/')
                .then(response => response.json())
                .then(data => {
                    console.log("Dashboard Data:", data);
                    setDashboardData(data);
                    setLoading(false);
                })
                .catch(error => console.error('Error fetching data:', error));
        };

        fetchData(); // Initial fetch
        const interval = setInterval(fetchData, 60000); // Fetch data every minute

        return () => clearInterval(interval); // Cleanup interval on component unmount
    }, []);

    if (loading) {
        return <div>Loading...</div>;
    }

    const formatCurrency = (value) => {
        return `$${value.toFixed(2)}`;
    };

    const getProfitColor = (value) => {
        return value >= 0 ? 'green' : 'red';
    };

    return (
        <div className="dashboard">
            <h1>Dashboard</h1>
            <div className='account-box'>
                <h2>Total Balance</h2>
                <p>{formatCurrency(dashboardData.total_balance)}</p>
                <h2>Total Equity</h2>
                <p>{formatCurrency(dashboardData.total_equity)}</p>
                <h2>Day Profit</h2>
                <p style={{color: getProfitColor(dashboardData.total_day_profit)}}>
                    {formatCurrency(dashboardData.total_day_profit)}
                </p>
                <h2>Day Equity</h2>
                <p style={{color: getProfitColor(dashboardData.total_day_equity)}}>
                    {formatCurrency(dashboardData.total_day_equity)}
                </p>
                <h2>Last Export Time</h2>
                <p>{new Date(dashboardData.last_export_time).toLocaleString()}</p>
            </div>
            <div className="accounts">
                {dashboardData.accounts.map((account, index) => (
                    <AccountBox key={index} account={account} />
                ))}
            </div>
        </div>
    );
};

export default Dashboard;
