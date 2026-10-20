from app import app, db, generate_invoice


def setup_ctf():
    invoices: list[dict[str, str]] = [
    {
        "customer": "Ramon Dino",
        "service": "Limpeza Completa do veículo",
        "amount": 500.0,
        "custom_message": "Obrigado pela preferência!"
    },
    {
        "customer": "Julio Balestrin",
        "service": "Polimento",
        "amount": 450.0,
        "custom_message": "Obrigado pela preferência!"
    },
    {
        "customer": "Dilera",
        "service": "Balinha",
        "amount": 0.50,
        "custom_message": None
    },
    {
        "customer": "Danilo Gentili",
        "service": "Bebida Sabor Energetico",
        "amount": 500.0,
        "custom_message": "Obrigado pela preferência!"
    },
    {
        "customer": "Renato Cariani",
        "service": "Caldo de Cana com Pastel",
        "amount": 67.0,
        "custom_message": "Obrigado pela preferência!"
    }
    ]

    for i in invoices:
        generate_invoice(i)


if __name__ == '__main__':
    with app.app_context():
        with db() as (conn, _):
            conn.executescript(open('schema.sql', 'r', encoding='utf-8').read())
        setup_ctf()

    app.run(host='0.0.0.0', port=5000)