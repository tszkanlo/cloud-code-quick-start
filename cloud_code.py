import skygear
import logging
from urllib import request, parse
import bcrypt
from sqlalchemy.sql import text
from skygear.utils.db import conn

log = logging.getLogger(__name__)


# Reject empty 'name' before saving a cat to the database
@skygear.after_save('attendance', async=False)
def postRequest(record, original_record, db):
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
    log.info('New attendance: ' + record.get('name'))
    data = parse.urlencode({'name': record.get('name'), 'itsc': record.get('itsc'), 'eventid': record.get('event_id'), 'attendanceID': record.id.key}).encode()
    req =  request.Request('http://api.usthing.xyz/node/ems-email/send-email', data=data, headers=hdr) # this will make the method "POST"
    resp = request.urlopen(req)
    return record

@skygear.op('master:reset-password')
def custom_reset_password(username, new_password):
    # also need to check permission so that only admin can use this
    is_success = reset_password_by_username(username, new_password)
    return {
        'success': is_success,
    }

def hash_password(password):
    """
    Return a hased password of a plaintext password.
    """
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode("utf-8")


def reset_password_by_username(username, new_password):
    """
    Reset the user password with a new password.
    """
    if not (isinstance(username, str) and isinstance(new_password, str)):
        raise ValueError("username and new_password must be string")

    sql = text('''
        UPDATE \"_auth\"
        SET password = :new_password
        WHERE id = (SELECT \"_owner_id\"
                    FROM user
                    WHERE username = :username)
        ''')
    with conn() as db:
        result = db.execute(sql,
                            new_password=hash_password(new_password),
                            username=username)
    return result.rowcount > 0
