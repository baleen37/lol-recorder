import sys
from web.app import app

if len(sys.argv) < 2:
    raise Exception('require more than 2 args')

if sys.argv[1] == 'runserver':
    port = 5000
    if len(sys.argv) > 2:
        port = int(sys.argv[2])
    app.run(host='0.0.0.0', port=port)
else:
    raise Exception('not exists command')
