"""CRUD API for the possession collection."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.possession import Possession
from app.schemas.possession import PossessionCreate, PossessionRead, PossessionUpdate

router = APIRouter(prefix="/possessions", tags=["possessions"])


def find_possession(db: Session, possession_id: UUID) -> Possession:
    item = db.get(Possession, str(possession_id))
    if item is None:
        raise HTTPException(status_code=404, detail="Possession not found")
    return item


@router.post("", response_model=PossessionRead, status_code=status.HTTP_201_CREATED)
def create_possession(payload: PossessionCreate, db: Session = Depends(get_db)) -> Possession:
    item = Possession(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.get("", response_model=list[PossessionRead])
def list_possessions(
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
) -> list[Possession]:
    statement = select(Possession).order_by(Possession.created_at, Possession.id).limit(limit).offset(offset)
    return list(db.scalars(statement).all())


@router.get("/{possession_id}", response_model=PossessionRead)
def get_possession(possession_id: UUID, db: Session = Depends(get_db)) -> Possession:
    return find_possession(db, possession_id)


@router.patch("/{possession_id}", response_model=PossessionRead)
def update_possession(
    possession_id: UUID, payload: PossessionUpdate, db: Session = Depends(get_db)
) -> Possession:
    item = find_possession(db, possession_id)
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(item, key, value)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.delete("/{possession_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_possession(possession_id: UUID, db: Session = Depends(get_db)) -> Response:
    item = find_possession(db, possession_id)
    db.delete(item)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
