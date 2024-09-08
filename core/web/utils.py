from django.shortcuts import redirect
from urllib.parse import urlencode

async def errorRedirect(error):
    params = {'error': error}

    return redirect("/error/?" + urlencode(params))