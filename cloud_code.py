import skygear
import logging
from urllib import request, parse

log = logging.getLogger(__name__)


# Reject empty 'name' before saving a cat to the database
@skygear.after_save('attendance', async=False)
def postRequest(record, original_record, db):
    log.info('New attendance: ' + record.get('name'))
    data = parse.urlencode({'name': record.get('name'), 'itsc': record.get('itsc'), 'eventid': record.get('event_id'), 'attendanceID': record.id.key}).encode()
    req =  request.Request('http://d7e1084b.ngrok.io', data=data) # this will make the method "POST"
    resp = request.urlopen(req)
    return record


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
