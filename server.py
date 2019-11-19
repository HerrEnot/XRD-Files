# coding: utf-8

from bottle import route, request, run
import uuid
import os
from datetime import datetime as dt

from bottle import static_file

@route('/')
def fileselect():
    return '''
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
</head>
<body>
<form action="/upload" method="post" enctype="multipart/form-data">
  Select a file: <input type="file" name="upload" multiple />
  <input type="submit" value="Start upload" />
</form>
</body>
</html>
    '''

def get_directory():
    now = dt.now()
    dirname = now.strftime("%Y-%b-%d")
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    return dirname

def get_output_directory():
    now = dt.now()
    dirname = now.strftime("%Y-%b-%dh%H")
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    return dirname


def process_file(filename):
    with open(filename, 'r') as fp:
        lines = fp.readlines()

    #THETA
    a = lines[1].split(' ')
    theta0 = float(a[3])
    theta1 = float(a[4])
    thetastep = float(a[5])
    round1 = len(str(thetastep))
    mas = []

    while theta0 <= theta1:
        theta0 = round(theta0, round1 - 2)
        mas.append(theta0)
        theta0 += thetastep
    mas.append(theta0)

    #OUTPUT FILE NAME
    output_filename = os.path.join(
        get_output_directory(),
        lines[0].split()[0] + ".txt"
    )

    with open(output_filename, 'w') as output:
        b = lines[2].split(' ')
        for i in range(len(b) - 2):
            output.write(f'{mas[i]}     {b[i+1]}\n')
            # f1.write(str(mas[i]) + '     ' + str(b[i+1]) + "\n")

    return output_filename

@route('/outfiles/<filename:path>')
def server_static(filename):
    return static_file(filename, root='.')

@route('/upload', method='POST')
def do_upload():
    # category   = request.forms.get('category')
    uploads     = request.files.getall('upload')
    print([upload.filename for upload in uploads])
    # print('yoba')

    outputs = []
    for upload in uploads:
        name, ext = os.path.splitext(upload.filename)
        save_path = os.path.join(get_directory(), uuid.uuid4().hex)
        upload.save(save_path, overwrite=True)
        outname = process_file(save_path)
        outputs.append(outname)

    outputs_str = '\n'.join(f'<li>{name}. <a href="/outfiles/{name}" download>Скачать</a></li>' for name in outputs)

    #shutil.make_archive()
    return '<ul>' + outputs_str + '</ul>'

run(host='localhost', port=8080)