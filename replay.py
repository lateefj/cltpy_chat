import model
model.setup_engine()

import handlers

from sqlalchemy import distinct



session = model.get_session()

sids = session.query(distinct(model.Error.session_id))
for r in sids:
    us = model.UserSession.by_id(r[0])
    for e in us.events:
        handlers.publish({'type':e.type, 'timestamp':e.timestamp, 'data':e.data})

