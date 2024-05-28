from transbank.webpay.webpay_plus.transaction import Transaction

def crear_transaccion(buy_order, session_id, amount, return_url):
    transaction = Transaction()

    response = transaction.create(
        buy_order=buy_order,
        session_id=session_id,
        amount=amount,
        return_url=return_url
    )

    return response