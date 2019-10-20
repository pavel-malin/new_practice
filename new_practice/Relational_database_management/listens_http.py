import flask
import psycopg2
import psycopg2.extensions
import select


app = flask.Flask(__name__)


def stream_messages(channel):
    conn = psycopg2.connect(database='mydatabase', user='mydatabase',
                            password='mydatabase', host='localhost')
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    curs = conn.cursor()
    curs.execute('LISTEN channel_%d;' % int(channel))

    while True:
        select.select([conn], [], [])
        conn.poll()
        while conn.notifies:
            notify = conn.notifies.pop()
            yield 'data: ' + notify.payload + '\n\n'


@app.route("/message/<channel>", methods=['GET'])
def get_messages(channel):
    return flask.Response(stream_messages(channel),
                          mimetype='text/event-stream')


if __name__ == '__main__':
    app.run()
