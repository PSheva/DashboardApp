import React from 'react';

const AccountBox = ({ account }) => {
    const { account_number, balance, equity, day_profit, day_equity } = account;

    const formatCurrency = (value) => {
        return `$${value.toFixed(2)}`;
    };

    const getProfitColor = (value) => {
        return value >= 0 ? 'green' : 'red';
    };

    return (
        <div className="account-box">
            <h3>Account Number: {account_number}</h3>
            <p>Balance: {formatCurrency(balance)}</p>
            <p>Equity: {formatCurrency(equity)}</p>
            <p style={{ color: getProfitColor(day_profit) }}>Day Profit: {formatCurrency(day_profit)}</p>
            <p style={{ color: getProfitColor(day_equity) }}>Day Equity: {formatCurrency(day_equity)}</p>
        </div>
    );
};

export default AccountBox;
