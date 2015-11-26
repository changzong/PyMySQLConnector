# -*- coding:utf-8 -*-
import sys
from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
import MySQLHooker as Hooker
import MySQLInjector as Injector
import MySQLEditor as Editor

reload(sys)
sys.setdefaultencoding('utf8')


table_list = [['tableManagerId', 'tableName', 'tableType',
               'dataLevel', 'procName', 'note', 'inputMan',
               'inputDate', 'updateMan', 'updateDate']]
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/tablemanager', methods=['GET', 'POST'])
def info_printer():
    global increment_ID
    global table_list
    # Catch inserting request and do the insertion
    # ZCALERT：Do the MySQL connection again for security reason.
    if request.method == 'POST':
        if request.form['which'] == 'add_item':
            print str(request.form['table_name'])
            increment_ID += 1
            table_list.append([str(increment_ID), str(request.form['table_name']),
                               request.form['table_type'], request.form['data_level'],
                               str(request.form['proc_name']), request.form['note'],
                               request.form['input_man'], str(request.form['input_date']),
                               request.form['update_man'], str(request.form['update_date'])])
            print table_list

            table_data = (str(increment_ID), str(request.form['table_name']),
                          request.form['table_type'], request.form['data_level'],
                          str(request.form['proc_name']), request.form['note'],
                          request.form['input_man'], str(request.form['input_date']),
                          request.form['update_man'], str(request.form['update_date']))
            cnx = Injector.database_connection(Injector.config)
            if cnx != -1:  # Connection successful
                cursor = cnx.cursor()
                Injector.table_insertion(cursor, table_data)
                cnx.commit()
                cursor.close()
            cnx.close()

            return jsonify({'new_content': table_list})

        elif request.form['which'] == 'edit_item':
            row_to_edit = request.form['id_index']
            column_to_edit = request.form['item_index']
            content_to_replace = request.form['edit_content']
            cnx = Editor.database_connection(Injector.config)
            if cnx != -1:  # Connection successful
                cursor = cnx.cursor()
                table_list = [['tableManagerId', 'tableName', 'tableType',
                               'dataLevel', 'procName', 'note', 'inputMan',
                               'inputDate', 'updateMan', 'updateDate']]
                query = ("SELECT tableManagerId, tableName, tableType, "
                         "dataLevel, procName, note, inputMan, inputDate, "
                         "updateMan, updateDate FROM TableManager")
                cursor.execute(query)
                for (tableManagerId, tableName, tableType,
                     dataLevel, procName, note, inputMan,
                     inputDate, updateMan, updateDate) in cursor:
                    table_list.append([tableManagerId, tableName,
                                      tableType, dataLevel, procName,
                                      note, inputMan, inputDate,
                                      updateMan, updateDate])
                table_list[int(row_to_edit)][int(column_to_edit)] = content_to_replace
                data_for_tuple = table_list[int(row_to_edit)][1:]
                data_for_tuple.append(str(row_to_edit))
                print data_for_tuple
                data = tuple(data_for_tuple)
                print data
                Editor.database_edition(cursor, data)
                cnx.commit()
                cursor.close()
            cnx.close()

            return jsonify({'new_content': table_list})

    else:
        table_list = [['tableManagerId', 'tableName', 'tableType',
                       'dataLevel', 'procName', 'note', 'inputMan',
                       'inputDate', 'updateMan', 'updateDate']]
        cnx = Hooker.database_connection(Hooker.config)
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
                    table_list.append([tableManagerId, tableName,
                                      tableType, dataLevel, procName,
                                      note, inputMan, inputDate,
                                      updateMan, updateDate])
                increment_ID = int(tableManagerId)
            cursor.close()
        cnx.close()
        return render_template('table_manager.html', content=table_list)


if __name__ == '__main__':
    app.debug = True
    app.run(host='192.168.56.1', port=5000)
