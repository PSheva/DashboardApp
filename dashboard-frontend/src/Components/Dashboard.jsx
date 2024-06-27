import React, { useEffect, useState } from 'react';
import AccountBox from './AccountBox';
import '/src/index.css';

const Dashboard = () => {
    const [dashboardData, setDashboardData] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchData = () => {
            // fetch('http://0.0.0.0:8000/')
            fetch('ws://ec2-3-16-217-246.us-east-2.compute.amazonaws.com:5175')
                .then(response => response.json())
                .then(data => {
                    console.log("Dashboard Data:", data);
                    setDashboardData(data);
                    setLoading(false);
                })
                .catch(error => console.error('Error fetching data:', error));
        };

        fetchData(); 
        const interval = setInterval(() => {
            fetchData();
        }, 30000); 
        return () => clearInterval(interval);
    }, []);

    if (loading) {
        return <div>Loading...</div>;
    }

    const formatCurrency = (value = 0) => {
        return `$${value.toFixed(2)}`;
    };

    const getProfitColor = (value = 0) => {
        return value >= 0 ? 'green' : 'red';
    };

    const formatDate = (dateString) => {
        if (!dateString) {
            return 'N/A';
        }
        const date = new Date(dateString);
        if (isNaN(date.getTime())) {
            return 'N/A';
        }
        const options = { year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit', second: '2-digit' };
        return date.toLocaleDateString(undefined, options);
    };

    const accountNumbersToAggregate = [250119, 24478858];
    const accountsToAggregate = dashboardData.accounts.filter(account => accountNumbersToAggregate.includes(account.account_number));

    const aggregatedAccount = accountsToAggregate.reduce((acc, account) => {
        acc.balance += account.balance;
        acc.equity += account.equity;
        acc.day_profit += account.day_profit;
        acc.day_equity += account.day_equity;
        acc.week_profit += account.week_profit;
        acc.month_profit += account.month_profit;

        return acc;
    }, {
        account_number: 'Aggregated Account',
        strategy_name: '(Swap+)+(Swap-)',
        balance: 0,
        equity: 0,
        day_profit: 0,
        week_profit: 0,
        month_profit: 0,
        day_equity: 0
    });

    return (
        <div className="dashboard">
            <h1>Dashboard</h1>
            <div className="boxes-total-container">
                <div className='account-box'>
                    <h2>Total Balance</h2>
                    <h2>{formatCurrency(dashboardData.total_balance)}</h2>
                    <h2>Total Equity</h2>
                    <h2>{formatCurrency(dashboardData.total_equity)}</h2>
                    <h2>Day Profit</h2>
                    <h2 style={{ color: getProfitColor(dashboardData.total_day_profit) }}>
                        {formatCurrency(dashboardData.total_day_profit)}
                    </h2>
                    <h2>Pos P/L</h2>
                    <h2 style={{ color: getProfitColor(dashboardData.total_day_equity) }}>
                        {formatCurrency(dashboardData.total_day_equity)}
                    </h2>
                    <h2>Last Export Time</h2>
                    <h2>{new Date(dashboardData.last_export_time).toLocaleString()}</h2>
                    <h2>Week Profit</h2>
                    <h2 style={{ color: getProfitColor(dashboardData.total_week_profit) }}>
                        {formatCurrency(dashboardData.total_week_profit)}
                    </h2>
                    <h2>Month Profit</h2>
                    <h2 style={{ color: getProfitColor(dashboardData.total_month_profit) }}>
                        {formatCurrency(dashboardData.total_month_profit)}
                    </h2>
                </div>

                <div className="accounts">
                    {dashboardData.accounts.map((account, index) => (
                        <AccountBox key={index} account={account} />
                    ))}
                    <AccountBox account={aggregatedAccount} />
                </div>
            </div>
            <div className="positions">
                <div className="open-closed-positions">
                    <h2>Recent Closed Positions</h2>
                    <table>
                        <thead>
                            <tr>
                                <th>Account</th>
                                <th>Ticket</th>
                                <th>Open DateTime</th>
                                <th>Close DateTime</th>
                                <th>Size</th>
                                <th>Symbol</th>
                                <th>Type</th>
                                <th>Price</th>
                                <th>T/P S/L</th>
                                <th>Pos P/L(Profit)</th>
                            </tr>
                        </thead>
                        <tbody>
                            {dashboardData.closed_positions.map((position, index) => (
                                <tr key={index}>
                                    <td>{position.account_number}</td>
                                    <td>{position.ticket}</td>
                                    <td>{formatDate(position.open_time)}</td>
                                    <td>{formatDate(position.close_time)}</td>
                                    <td>{position.size}</td>
                                    <td>{position.symbol}</td>
                                    <td>{position.type}</td>
                                    <td>{formatCurrency(position.price)}</td>
                                    <td>{position.tp_sl ? formatCurrency(position.tp_sl) : 'N/A'}</td>
                                    <td style={{ color: getProfitColor(position.profit) }}>
                                        {formatCurrency(position.profit)}
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
                <div className="open-closed-positions">
                    <h2>All Open Positions</h2>
                    <table>
                        <thead>
                            <tr>
                                <th>Account</th>
                                <th>Ticket</th>
                                <th>Open DateTime</th>
                                <th>Size</th>
                                <th>Symbol</th>
                                <th>Type</th>
                                <th>Price</th>
                                <th>T/P S/L</th>
                                <th>Pos P/L(Profit)</th>
                            </tr>
                        </thead>
                        <tbody>
                            {dashboardData.open_positions.map((position, index) => (
                                <tr key={index}>
                                    <td>{position.account_number}</td>
                                    <td>{position.ticket}</td>
                                    <td>{formatDate(position.open_time)}</td>
                                    <td>{position.size}</td>
                                    <td>{position.symbol}</td>
                                    <td>{position.type}</td>
                                    <td>{formatCurrency(position.price)}</td>
                                    <td>{position.tp_sl ? formatCurrency(position.tp_sl) : 'N/A'}</td>
                                    <td style={{ color: getProfitColor(position.profit) }}>
                                        {formatCurrency(position.profit)}
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
                <div className="balance-operations">
                    <h2>Balance Operations</h2>
                    <table>
                        <thead>
                            <tr>
                                <th>Account</th>
                                <th>Ticket</th>
                                <th>Export DateTime</th>
                                <th>Profit</th>
                                <th>Description</th>
                            </tr>
                        </thead>
                        <tbody>
                            {dashboardData.balance_operations.map((operation, index) => (
                                <tr key={index}>
                                    <td>{operation.account_number}</td>
                                    <td>{operation.ticket}</td>
                                    <td>{formatDate(operation.export_time)}</td>
                                    <td style={{ color: getProfitColor(operation.profit) }}>
                                        {formatCurrency(operation.profit)}
                                    </td>
                                    <td>{operation.comment}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
}

export default Dashboard;
