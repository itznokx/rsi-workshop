from app.database import db
from flask import render_template_string
from werkzeug.utils import secure_filename
from uuid import uuid4

def generate_invoice(invoice):
    with db() as (_, cur): # Verificando se a fatura ja existe (Evita duplicar arquivos no app/invoices/)
        invoice_test = cur.execute('SELECT * FROM invoices WHERE service=?;', (invoice['service'],)).fetchone()
        if invoice_test:
            return

    base_model = open('app/invoices/base_model.html', 'r', encoding='utf-8').read()
    
    model = render_template_string(base_model, invoice=invoice)
    model_path: str = f'app/invoices/generated/{secure_filename(invoice['service'])}' + str(uuid4()) + '.html'

    open(model_path, 'w', encoding='utf-8').write(model)

    with db() as (_, cur):
        cur.execute(
            'INSERT OR IGNORE INTO invoices(customer, service, amount, custom_message, path) VALUES(?, ?, ?, ?, ?)'
            , (invoice['customer'], invoice['service'], invoice['amount'], invoice.get('custom_message'), model_path)
        )