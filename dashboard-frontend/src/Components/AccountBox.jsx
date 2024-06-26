import React from 'react';

const AccountBox = ({ account }) => {
    const formatCurrency = (value = 0) => {
        return `$${value.toFixed(2)}`;
    };

    const getProfitColor = (value=0) => {
        return value >= 0 ? 'green' : 'red';
    };

    return (
        <div className='account-box'>
            <h3>Account Number: {account.account_number}</h3>
            <p>Strategy: {account.strategy_name}</p>
            <p>Balance: {formatCurrency(account.balance)}</p>
            <p>Equity(NLV): {formatCurrency(account.equity)}</p>
            <p style={{ color: getProfitColor(account.day_equity) }}>Pos P/L: {formatCurrency(account.day_equity)}</p>
            <p style={{ color: getProfitColor(account.day_profit) }}>Day Profit: {formatCurrency(account.day_profit)}</p>
            <p style={{ color: getProfitColor(account.week_profit) }}>Week Profit: {formatCurrency(account.week_profit)}</p>
            <p style={{ color: getProfitColor(account.month_profit) }}>Month Profit: {formatCurrency(account.month_profit)}</p>
            {account.message && <p className="warning">{account.message}</p>}
        </div>
    );
}

export default AccountBox;
