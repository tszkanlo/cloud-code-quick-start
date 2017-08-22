import skygear
import logging
from urllib import request, parse
from skygear.utils.user import reset_password_by_username

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

# # cron job that runs every 2 minutes
# @skygear.every('@every 2m')
# def meow_for_food():
#     # Skygear Portal Console Log will show 'Meow Meow!' every 2 minutes
#     log.info('Meow Meow!')
#
#
# # custom logic to be invoked from SDK, e.g.
# # skygear.lambda('food:buy', {'food': 'salmon'}) for JS
# @skygear.op('food:buy', user_required=False)
# def buy_food(food):
#     # TODO: call API about online shopping
#     # return an object to the SDK
#     return {
#         'success': True,
#         'food': food,
#     }
#
#
# # accepting HTTP GET request to /cat/feed
# @skygear.handler('cat:feed', method=['GET'])
# def feed(request):
#     # TODO: handle the request such as logging the request to database
#     return 'Meow! Thanks!\n'
