import model
#################### DEMO DISPATCH CODE (NOT FOR PRODUCTION!!!!!!!!!!!!) ########################

HANDLERS = {}
def reg(type, func):
    global HANDLERS
    HANDLERS[type] = func
def publish(event):
    if event.has_key('type') and HANDLERS.has_key(event['type']):
        return HANDLERS[event['type']](event)


################ EVENT HANDLER(s) #########################
def handle_message(event):
    """
    This is an example of an unexpected error so let see if we can handle
    this situation just by doing something other than raising an Exception.
    """
    if event['data']['text'].find('hipster') > -1:
        #print('Hipster really I mean we could do better no?')
        raise Exception('NO NO NO not a hipster') # Simulates exception in application
reg('message', handle_message)

def handle_error_count(e):
    ec = model.Error.count()
    evc = model.Event.count()
    return {'error_count':ec, 'event_count': evc}
reg('error_count', handle_error_count)
