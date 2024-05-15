from datetime import datetime
from fastapi import HTTPException

from pymongo import DESCENDING

from app.models.user_action import User_Action
from app.services.db_service import users_action
async def Create_user_action(new_user_action:User_Action):
    new_user_action.id = await set_id()
    users_action.insert_one({
        "id": new_user_action.id,
        "user_id": new_user_action.user_id,
        "type": new_user_action.type,
        "amount": new_user_action.amount,
        "datetime": datetime.now()
    })
    return new_user_action
async def update_user_action(user_action: User_Action):
    filter = {"id": user_action.id}
    new_values = {"$set": {"type": user_action.type,
                            "amount": user_action.amount,
                            "datetime":user_action.datetime}}
    result=users_action.update_one(filter, new_values)
    if result.raw_result.get('n') == 0:
        raise HTTPException(status_code=404, detail="invalid user action")
    return user_action

async def delete_user_action(user_action_id:int):
     result=users_action.delete_one({"id": user_action_id})
     if result.raw_result.get('n')==0:
         raise HTTPException(status_code=404, detail="invalid user action")


async def set_id():
   max_id_document = users_action.find_one({}, sort=[("id", DESCENDING)])
   if max_id_document:
    return(max_id_document["id"]+1)
   else:
    return 0