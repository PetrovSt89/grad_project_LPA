from fastapi import HTTPException

from src.models import Box, User


def box_by_name(boxname: str) -> Box | None:
    box = Box.query.filter(Box.boxname == boxname).first()
    if not box:
        raise HTTPException(
            status_code=400,
            detail='Такoй коробки нет'
        )
    return box


def check_creator(box: Box, user: User) -> None:
    if box.creator_id != user.id:
        raise HTTPException(
            status_code=400,
            detail='Вы не создавали такую коробку'
        )