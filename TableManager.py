# -*- coding:utf-8 -*-
import sys
from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
import MySQLHooker as Hooker
import MySQLInjector as Injector
import MySQLEditor as Editor
import MySQLRemover as Remover

reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)

config = {
    'user': 'xxxx',
    'password': 'xxxx',
    'host': 'xxxx',
    'database': 'xxxx',
    'use_pure': True  # The default is True which means using pure Python rather than C extensions
}

increment_ID = 0


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/tablemanager', methods=['GET', 'POST'])
def info_printer():
    global increment_ID
    # Catch inserting request and do the insertion
    # ZCALERT：Do the MySQL connection again for security reason.
    if request.method == 'POST':
        if request.form['which'] == 'add_item':  # Add entry to the table
            print str(request.form['table_name'])
            increment_ID += 1
            table_data = (str(increment_ID), str(request.form['table_name']),
                          request.form['table_type'], request.form['data_level'],
                          str(request.form['proc_name']), request.form['note'],
                          request.form['input_man'], str(request.form['input_date']),
                          request.form['update_man'], str(request.form['update_date']))
            cnx = Injector.database_connection(config)
            if cnx != -1:  # Connection successful
                cursor = cnx.cursor()
                Injector.table_insertion(cursor, table_data)
                cnx.commit()
                cursor.close()
            cnx.close()
            table_list = grab_table_content()

            return jsonify({'new_content': table_list})

        elif request.form['which'] == 'edit_item':  # Modify existing item in the table
            row_to_edit = request.form['id_index']
            column_to_edit = request.form['item_index']
            content_to_replace = request.form['edit_content']
            table_list = grab_table_content()
            table_list[int(row_to_edit)][int(column_to_edit)] = content_to_replace
            data_for_tuple = table_list[int(row_to_edit)][1:]
            data_for_tuple.append(str(row_to_edit))
            print data_for_tuple
            data = tuple(data_for_tuple)
            print data
            cnx = Editor.database_connection(config)
            if cnx != -1:  # Connection successful
                cursor = cnx.cursor()
                Editor.database_edition(cursor, data)
                cnx.commit()
                cursor.close()
            cnx.close()
            table_list = grab_table_content()

            return jsonify({'new_content': table_list})

        elif request.form['which'] == 'remove_item':  # Remove a row in that table
            row_to_remove = request.form['id_index']
            table_list = grab_table_content()
            table_count = len(table_list) - 1
            cnx = Remover.database_connection(config)
            if cnx != -1:  # Connection successful
                cursor = cnx.cursor()
                Remover.database_removal(cursor, tuple(row_to_remove))
                cnx.commit()
                # Restructure table with updated IDs
                Remover.database_restructure(cursor, row_to_remove, table_count)
                cnx.commit()
                cursor.close()
            cnx.close()
            table_list = grab_table_content()
            return jsonify({'new_content': table_list})

    else:  # Just get table content
        table_list = grab_table_content()
        return render_template('table_manager.html', content=table_list)


def grab_table_content():
    global increment_ID
    table_content = [['tableManagerId', 'tableName', 'tableType',
                      'dataLevel', 'procName', 'note', 'inputMan',
                      'inputDate', 'updateMan', 'updateDate']]
    cnx = Hooker.database_connection(config)
    if cnx != -1:  # Connection successful
        cursor = cnx.cursor()
        # Initial load just do the rendering
        if Hooker.table_creation(cursor) == -1:  # TableManager exists or other errors
            query = ("SELECT tableManagerId, tableName, tableType, "
                     "dataLevel, procName, note, inputMan, inputDate, "
                     "updateMan, updateDate FROM TableManager")
            cursor.execute(query)
            for (tableManagerId, tableName, tableType,
                 dataLevel, procName, note, inputMan,
                 inputDate, updateMan, updateDate) in cursor:
                table_content.append([tableManagerId, tableName,
                                      tableType, dataLevel, procName,
                                      note, inputMan, str(inputDate),
                                      updateMan, str(updateDate)])
        cursor.close()
    cnx.close()
    increment_ID = int(table_content[-1][0])
    return table_content


if __name__ == '__main__':
    app.debug = True
    app.run(host='localhost', port=5000)
    # app.run(host='10.7.13.108', port=5000)
