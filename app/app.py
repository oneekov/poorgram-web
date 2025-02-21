from quart import render_template, request, redirect
from config import *

from modules.auth import auth
from modules.chats import chats

app.register_blueprint(auth)
app.register_blueprint(chats)

@app.route('/healthz')
async def healthz():
    return {'status': 'ok'}

@app.route('/')
async def index():
    if 'auth_key' in request.cookies:
        return redirect('/chats')

    return await render_template('index.html')

@app.route('/error')
async def error():
    data = {'error': request.args.get('error', 'N/s')}

    return await render_template('error.html', **data)

@app.route('/proxy')
async def proxy():
    # TODO: запилить добавление proxy на этой странице. Прокси будут сохраняться в куки и использоваться,
    # если они там присутствуют. Если прокси нет, то выдавать предупреждение. Если пользователь согласен
    # пользоваться сервисом без куки, то вбить какой-нибудь placeholder
    return ''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
