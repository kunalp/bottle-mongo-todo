import pymongo
from bottle import route, run, debug, template, request, validate, static_file, error, redirect
from bson.objectid import ObjectId


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


@route('/edit/<id:re:[0-9a-z]+>', method='GET')
def edit_item(id):

    if request.GET.get('save','').strip():
        edit = request.GET.get('task','').strip()
        status = request.GET.get('status','').strip()

        connection = pymongo.Connection("mongodb://localhost", safe=True)
        db = connection.todo
        db.todo_items.update({"_id": ObjectId(id)}, {'task': edit, 'status': status})

        redirect('/todo')

    else:
        connection = pymongo.Connection("mongodb://localhost", safe=True)
        db = connection.todo
        cur_data = db.todo_items.find_one({"_id": ObjectId(id)})

        return template('edit_task', old=cur_data, no=id)


@route('/item/<id:re:[0-9a-z]+>')
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


@route('/json/<id:re:[0-9a-z]+>')
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


