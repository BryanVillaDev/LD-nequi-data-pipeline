SELECT * 
FROM transactions 
WHERE DATE(transaction_date) = '{{ ds }}';
