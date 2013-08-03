import pymongo
import sys
from bottle import route, run, debug, template, request, validate, static_file, error, redirect
from bson.objectid import ObjectId


# only needed when you run Bottle on mod_wsgi
from bottle import default_app

@route('/todo')
def todo_list():
    connection = pymongo.Connection("mongodb://localhost", safe=True)
    db = connection.todo
    items = db.todo_items.find({'status': 'open'})

    output = template('make_table', rows=items)
    return output


@route('/new', method='GET')
def new_item():

    if request.GET.get('save','').strip():
        new = request.GET.get('task', '').strip()

        connection = pymongo.Connection("mongodb://localhost", safe=True)
        db = connection.todo
        db.todo_items.insert({'task': new, 'status': 'open'})

        return '<p>The new task was inserted into the database. <a href="/todo"> Return to list</a></p>'

    else:
        return template('new_task.tpl')


@route('/edit/:no', method='GET')
#@validate(no=int)
def edit_item(no):

    if request.GET.get('save','').strip():
        edit = request.GET.get('task','').strip()
        status = request.GET.get('status','').strip()

        connection = pymongo.Connection("mongodb://localhost", safe=True)
        db = connection.todo
        db.todo_items.update({"_id": ObjectId(no)}, {'task': edit, 'status': status})

        redirect('/todo')

    else:
        connection = pymongo.Connection("mongodb://localhost", safe=True)
        db = connection.todo
        cur_data = db.todo_items.find_one({"_id": ObjectId(no)})

        return template('edit_task', old = cur_data, no = no)


@route('/item/:id#[1-9a-z]+#')
def show_item(id):

        connection = pymongo.Connection("mongodb://localhost", safe=True)
        db = connection.todo
        result = db.todo_items.find_one({"_id": ObjectId(id)})

        if not result:
            return 'This item number does not exist!'
        else:
            return 'Task: %s' %result['task']


@route('/help')
def help():

    static_file('help.html', root='.')


@route('/json/:id#[1-9a-z]+#')
def show_json(id):

    connection = pymongo.Connection("mongodb://localhost", safe=True)
    db = connection.todo
    result = db.todo_items.find_one({"_id": ObjectId(id)})
    result['_id'] = id


    if not result:
        return {'_id': id, 'task': 'This item number does not exist!'}
    else:
        return result


@error(403)
def mistake403(code):
    return 'There is a mistake in your url!'


@error(404)
def mistake404(code):
    return 'Sorry, this page does not exist!'


debug(True)
run(reloader=True)
#remember to remove reloader=True and debug(True) when you move your application from development to a productive environment


