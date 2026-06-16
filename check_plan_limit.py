from enums import Plan
from sqlalchemy.orm import Session
import models
from fastapi import HTTPException,status

PLAN_LIMITS = {
Plan.free : 5,
Plan.basic :10,
Plan.premium : 20

}





def check_limit(db:Session,user:models.User):
    count = db.query(models.Business).filter(models.Business.owner_id == user.id).count()
    limit = PLAN_LIMITS.get(user.plan, 0)
    # if limit is None:
    #     return 

    if count >= limit:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Your {user.plan.value} plan allows {limit} business(es). Upgrade to add more."
        )
