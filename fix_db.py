from service.database import get_local_session
from service.database_schema import Interviews_table

with get_local_session() as db:
    interviews = db.query(Interviews_table).filter(Interviews_table.status == "Start").all()
    for i in interviews:
        db.delete(i)
    db.commit()
    print("Deleted active interviews")
