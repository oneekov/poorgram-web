from urllib.parse import urlencode
from quart import redirect

async def error_redirect(error):
    params = {'error': error}

    return redirect('/error?' + urlencode(params))

async def represent_dialog_as_str(dialog) -> str:
    result = dialog.date.strftime('%d.%m.%y')
    if dialog.pinned:
        result = 'закреплено | ' + result
    if dialog.unread_count != 0:
        result = f'{dialog.unread_count} непрочитанных | ' + result
    return result
