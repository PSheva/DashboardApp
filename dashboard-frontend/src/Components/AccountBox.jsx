import React from 'react';

const AccountBox = ({ account }) => {
    const formatCurrency = (value) => {
        return `$${value.toFixed(2)}`;
    };

    const getProfitColor = (value) => {
        return value >= 0 ? 'green' : 'red';
    };

    return (
        <div className='account-box'>
            <h3>Account Number: {account.account_number}</h3>
            <p>Strategy: {account.strategy_name}</p>
            <p>Balance: {formatCurrency(account.balance)}</p>
            <p>Equity(NLV): {formatCurrency(account.equity)}</p>
            <p style={{ color: getProfitColor(account.day_profit) }}>Day Profit: {formatCurrency(account.day_profit)}</p>
            <p style={{ color: getProfitColor(account.day_equity) }}>Pos P/L: {formatCurrency(account.day_equity)}</p>
        </div>
    );
}

export default AccountBox;
