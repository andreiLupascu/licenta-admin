import datetime

import pymysql

from app.helpers.helpers_database import get_connection

valid_conference_fields = {'title', 'country', 'location', 'start_date', 'end_date', 'path_to_description',
                           'path_to_logo'}


def create_conference(conference):
    try:
        title = conference['title']
        location = conference['location']
        country = conference['country']
        start_date = datetime.datetime.fromtimestamp(conference['start_date'])
        end_date = datetime.datetime.fromtimestamp(conference['end_date'])
        conn = get_connection()
        with conn.cursor(pymysql.cursors.DictCursor) as cur:
            try:
                cur.execute(
                    'INSERT INTO conference(title, path_to_logo, location, path_to_description, country, start_date, '
                    'end_date) '
                    'VALUES(%s, %s, %s, %s, %s, %s, %s)', (title, "", location, "", country, start_date, end_date,))
                conn.commit()
                conn.close()
                return f'Conference {title} created successfully.', 200
            except Exception as e:
                print(e)
                conn.close()
                return f'Something went wrong while creating conference {title}.', 500
    except KeyError:
        return "Invalid fields for conference.", 400


def update_conference(conference):
    if not set(conference.keys()).issubset(valid_conference_fields):
        return "Request contains invalid fields for conference.", 400
    else:
        title = conference['title']
        path_to_description = conference['path_to_description']
        path_to_logo = conference['path_to_logo']
        location = conference['location']
        country = conference['country']
        start_date = datetime.datetime.fromtimestamp(conference['start_date'])
        end_date = datetime.datetime.fromtimestamp(conference['end_date'])
        conn = get_connection()
        with conn.cursor(pymysql.cursors.DictCursor) as cur:
            try:
                affected_rows = cur.execute('UPDATE conference '
                                            'set '
                                            'path_to_logo=%s,'
                                            'location=%s,'
                                            'path_to_description=%s,'
                                            'country=%s,'
                                            'start_date=%s,'
                                            'end_date=%s '
                                            'WHERE title=%s;',
                                            (path_to_logo, location, path_to_description, country, start_date, end_date,
                                             title,))
                if affected_rows > 0:
                    conn.commit()
                    conn.close()
                    return f'Conference {title} updated successfully.', 200
                else:
                    conn.close()
                    return f'Conference {title} either does not exist or it has not been modified.', 204
            except Exception as e:
                print(e)
                conn.close()
                return f'Something went wrong while updating conference {title}.', 500


def delete_conference(conference):
    title = conference['title']
    conn = get_connection()
    with conn.cursor(pymysql.cursors.DictCursor) as cur:
        try:
            affected_rows = cur.execute('DELETE FROM conference WHERE title=%s;', (title,))
            if affected_rows > 0:
                conn.commit()
            else:
                conn.close()
                return f'Conference {title} does not exist.', 404
            conn.close()
            return f'Conference {title} deleted successfully.', 200
        except Exception as e:
            print(e)
            conn.close()
            return f'Something went wrong while deleting conference {title}.', 500
