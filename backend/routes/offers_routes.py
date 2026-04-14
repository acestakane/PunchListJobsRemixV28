import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, Depends
from typing import Optional
from database import db
from auth import get_current_user
from models import OfferCreate, OfferCounter
from utils.notify import create_notification
from utils.activity_log import log_activity
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


def now_str():
    return datetime.now(timezone.utc).isoformat()


@router.get("")
async def list_offers(
    status: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    """List offers. Crew sees received offers, Contractor sees sent offers."""
    if current_user["role"] == "crew":
        query = {"crew_id": current_user["id"]}
    elif current_user["role"] == "contractor":
        query = {"contractor_id": current_user["id"]}
    else:
        query = {}  # Admin sees all
    
    if status:
        query["status"] = status
    
    offers = await db.offers.find(query, {"_id": 0}).sort("created_at", -1).to_list(100)
    return offers


@router.post("/{offer_id}/accept")
async def accept_offer(offer_id: str, current_user: dict = Depends(get_current_user)):
    """Crew accepts an offer. Auto-assigns crew to job and reduces open slots."""
    if current_user["role"] != "crew":
        raise HTTPException(status_code=403, detail="Only crew can accept offers")
    
    offer = await db.offers.find_one({"id": offer_id}, {"_id": 0})
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")
    
    if offer["crew_id"] != current_user["id"]:
        raise HTTPException(status_code=403, detail="Not your offer")
    
    if offer["status"] != "pending" and offer["status"] != "countered":
        raise HTTPException(status_code=400, detail=f"Offer is {offer['status']}, cannot accept")
    
    # Get job
    job = await db.jobs.find_one({"id": offer["job_id"]}, {"_id": 0})
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Check if already accepted
    if current_user["id"] in job.get("crew_accepted", []):
        raise HTTPException(status_code=400, detail="Already accepted for this job")
    
    # Check if job is full
    current_crew_count = len(job.get("crew_accepted", []))
    if current_crew_count >= job["crew_needed"]:
        raise HTTPException(status_code=400, detail="Job is already full")
    
    # Accept the offer: add crew to job
    await db.jobs.update_one(
        {"id": offer["job_id"]},
        {
            "$push": {"crew_accepted": current_user["id"]},
            "$pull": {"crew_pending": current_user["id"]},  # Remove from pending if exists
            "$set": {"updated_at": now_str()}
        }
    )
    
    # Update offer status
    await db.offers.update_one(
        {"id": offer_id},
        {"$set": {"status": "accepted", "updated_at": now_str()}}
    )
    
    # Check if job should be marked as fulfilled
    updated_job = await db.jobs.find_one({"id": offer["job_id"]}, {"_id": 0})
    if len(updated_job.get("crew_accepted", [])) >= updated_job["crew_needed"]:
        await db.jobs.update_one(
            {"id": offer["job_id"]},
            {"$set": {"status": "fulfilled", "status_changed_at": now_str()}}
        )
    
    # Notify contractor
    await create_notification(
        offer["contractor_id"],
        "offer_accepted",
        "Offer Accepted",
        f"{current_user['name']} accepted your offer for '{offer['job_title']}'"
    )
    
    await log_activity(
        actor=current_user,
        action="offer.accepted",
        category="offer",
        target_id=offer_id,
        target_type="offer",
        details={"job_id": offer["job_id"]}
    )
    
    return {"message": "Offer accepted", "job_status": updated_job.get("status")}


@router.post("/{offer_id}/counter")
async def counter_offer(offer_id: str, data: OfferCounter, current_user: dict = Depends(get_current_user)):
    """Crew counters an offer with a different pay rate."""
    if current_user["role"] != "crew":
        raise HTTPException(status_code=403, detail="Only crew can counter offers")
    
    offer = await db.offers.find_one({"id": offer_id}, {"_id": 0})
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")
    
    if offer["crew_id"] != current_user["id"]:
        raise HTTPException(status_code=403, detail="Not your offer")
    
    if offer["status"] != "pending":
        raise HTTPException(status_code=400, detail=f"Cannot counter {offer['status']} offer")
    
    if data.counter_rate <= 0:
        raise HTTPException(status_code=400, detail="Counter rate must be positive")
    
    # Update offer with counter
    await db.offers.update_one(
        {"id": offer_id},
        {
            "$set": {
                "status": "countered",
                "counter_rate": data.counter_rate,
                "counter_message": data.message or "",
                "updated_at": now_str()
            }
        }
    )
    
    # Notify contractor
    await create_notification(
        offer["contractor_id"],
        "offer_countered",
        "Offer Countered",
        f"{current_user['name']} countered your offer for '{offer['job_title']}' with ${data.counter_rate}/hr"
    )
    
    await log_activity(
        actor=current_user,
        action="offer.countered",
        category="offer",
        target_id=offer_id,
        target_type="offer",
        details={"counter_rate": data.counter_rate}
    )
    
    return {"message": "Counter offer sent", "counter_rate": data.counter_rate}


@router.post("/{offer_id}/decline")
async def decline_offer(offer_id: str, current_user: dict = Depends(get_current_user)):
    """Crew declines an offer."""
    if current_user["role"] != "crew":
        raise HTTPException(status_code=403, detail="Only crew can decline offers")
    
    offer = await db.offers.find_one({"id": offer_id}, {"_id": 0})
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")
    
    if offer["crew_id"] != current_user["id"]:
        raise HTTPException(status_code=403, detail="Not your offer")
    
    if offer["status"] not in ("pending", "countered"):
        raise HTTPException(status_code=400, detail=f"Cannot decline {offer['status']} offer")
    
    # Update offer status
    await db.offers.update_one(
        {"id": offer_id},
        {"$set": {"status": "declined", "updated_at": now_str()}}
    )
    
    # Notify contractor
    await create_notification(
        offer["contractor_id"],
        "offer_declined",
        "Offer Declined",
        f"{current_user['name']} declined your offer for '{offer['job_title']}'"
    )
    
    await log_activity(
        actor=current_user,
        action="offer.declined",
        category="offer",
        target_id=offer_id,
        target_type="offer",
        details={"job_id": offer["job_id"]}
    )
    
    return {"message": "Offer declined"}


@router.post("/{offer_id}/withdraw")
async def withdraw_offer(offer_id: str, current_user: dict = Depends(get_current_user)):
    """Contractor withdraws an offer."""
    if current_user["role"] != "contractor":
        raise HTTPException(status_code=403, detail="Only contractors can withdraw offers")
    
    offer = await db.offers.find_one({"id": offer_id}, {"_id": 0})
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")
    
    if offer["contractor_id"] != current_user["id"]:
        raise HTTPException(status_code=403, detail="Not your offer")
    
    if offer["status"] == "accepted":
        raise HTTPException(status_code=400, detail="Cannot withdraw accepted offer")
    
    # Update offer status
    await db.offers.update_one(
        {"id": offer_id},
        {"$set": {"status": "withdrawn", "updated_at": now_str()}}
    )
    
    # Notify crew
    await create_notification(
        offer["crew_id"],
        "offer_withdrawn",
        "Offer Withdrawn",
        f"The offer for '{offer['job_title']}' has been withdrawn"
    )
    
    await log_activity(
        actor=current_user,
        action="offer.withdrawn",
        category="offer",
        target_id=offer_id,
        target_type="offer",
        details={"job_id": offer["job_id"]}
    )
    
    return {"message": "Offer withdrawn"}
