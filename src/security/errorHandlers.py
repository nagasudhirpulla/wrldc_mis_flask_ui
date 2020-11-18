from flask import render_template


def page_forbidden(err):
    return render_template('message.html.j2', title='403 Forbidden',
                           message='You must be logged in to access this content.'), 403


def page_unauthorized(err):
    return render_template('message.html.j2', title='401 Unauthorized',
                           message='You must be authorized in to access this content.'), 401


def page_not_found(err):
    return render_template('message.html.j2', title='404 Not Found',
                           message='The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.'), 404
