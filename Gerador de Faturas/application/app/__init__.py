from flask import Flask, render_template, redirect, url_for, request, render_template_string, abort
from urllib.parse import urlencode
from app.utils import generate_invoice
from app.database import db

app = Flask(__name__)

def blacklist(user_input: str):
    banned = ['{{', '}}', 'config']
    for b in banned:
        if b in user_input:
            return False
    return True

@app.route('/')
def index():
    invoice = request.args.to_dict()
    template = open('app/templates/index.html', 'r', encoding='utf-8').read()
    if invoice:
        custom_message = invoice.get('custom_message')
        if blacklist(custom_message):
            template = template.replace('$custom_message_input$', invoice.get('custom_message'))
        else:
            return render_template('blocked.html')

    return render_template_string(template, invoice=invoice)


@app.route('/generate', methods=['POST'])
def generate():
    invoice: dict = request.form.to_dict()

    generate_invoice(invoice)

    return redirect(f"{url_for('index')}?{urlencode(invoice)}")



@app.route('/templates')
def templates():
    template_id = request.args.get('template_id')
    template = None
    current_template_id = None
    current_customer = None

    if template_id:
        with db() as (_, cur):
            query = cur.execute('SELECT * FROM invoices WHERE id=?;', (template_id,)).fetchone()
            if not query:
                abort(404)

        template_infos = dict(query)
        template = render_template_string(open(template_infos['path'], 'r', encoding='utf-8').read())
        current_template_id = template_infos['id']
        current_customer = template_infos['customer']

    with db() as (_, cur):
        query = cur.execute('SELECT * FROM invoices;').fetchall()

    templates = [dict(row) for row in query]

    return render_template('templates.html', templates=templates, template=template, current_template_id=current_template_id, current_customer=current_customer)

@app.route('/templates/save', methods=['POST'])
def save_template():
    content = request.form.get('template_content')
    template_id = request.form.get('template_id')
    if not content or not template_id:
        print(template_id)
        abort(422)

    with db() as (_, cur):
        query = cur.execute('SELECT path FROM invoices WHERE id=?;', (template_id,)).fetchone()
        if not query:
            abort(404)

    path = dict(query)['path']
    open(path, 'w', encoding='utf-8').write(content)

    return redirect(f"{url_for('templates')}?template_id={template_id}")
    

    
    