import React from 'react';

const AccountBox = ({ account }) => {
    const formatCurrency = (value = 0) => {
        return `$${value.toFixed(2)}`;
    };

    const getProfitColor = (value = 0) => {
        if (value > 0) return 'green';
        if (value < 0) return 'red';
        return 'white';
    };

    return (
        <div className='account-box'>
            <h3>Account Number: {account.account_number}</h3>
            <p>Strategy: {account.strategy_name}</p>
            <p>Balance: {formatCurrency(account.balance)}</p>
            <p>Equity(NLV): {formatCurrency(account.equity)}</p>
            <div>
                <span style={{ color: 'white' }}>Pos P/L: </span>
                <span style={{ color: getProfitColor(account.day_equity) }}>
                    {formatCurrency(account.day_equity)}
                </span>
            </div>
            <div>
                <span style={{ color: 'white' }}>Day Profit: </span>
                <span style={{ color: getProfitColor(account.day_profit) }}>
                    {formatCurrency(account.day_profit)}
                </span>
            </div>
            <div>
                <span style={{ color: 'white' }}>Week Profit: </span>
                <span style={{ color: getProfitColor(account.week_profit) }}>
                    {formatCurrency(account.week_profit)}
                </span>
            </div>
            <div>
                <span style={{ color: 'white' }}>Month Profit: </span>
                <span style={{ color: getProfitColor(account.month_profit) }}>
                    {formatCurrency(account.month_profit)}
                </span>
            </div>
        </div>
    );
};

export default AccountBox;
