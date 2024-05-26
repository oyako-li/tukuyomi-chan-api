from fastapi import Request, APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import pyautogui as robot

router = APIRouter(
    prefix="/body",
    tags=["body"],
    responses={404: {"description": "Not found"}},
)


class Mouse(BaseModel):
    x: Optional[int] = 0
    y: Optional[int] = 0
    seconds: Optional[int] = 0
    button: Optional[str] = "left"
    clicks: Optional[int] = 1
    interval: Optional[float] = 0.2


class Key(BaseModel):
    text: Optional[str] = None
    press: Optional[str, List[str]] = "enter"
    interval: Optional[float] = 0.2


@router.get("/mouse")
async def get_mouse():
    return robot.position()


@router.get("/screen")
async def get_screen():
    return robot.size()


@router.post("/mouse/move")
async def post_mouse(move_to: Mouse):
    return robot.move(move_to.x, move_to.y, move_to.seconds)


@router.post("/mouse/move/to")
async def post_mouse_to(move_to: Mouse):
    return robot.moveTo(move_to.x, move_to.y, move_to.seconds)


@router.post("/mouse/drag")
async def post_mouse_drag(move_to: Mouse):
    return robot.drag(move_to.x, move_to.y, move_to.seconds, move_to.button)


@router.post("/mouse/drag/to")
async def post_mouse_drag_to(move_to: Mouse):
    return robot.dragTo(move_to.x, move_to.y, move_to.seconds, move_to.button)


@router.post("/mouse/click")
async def post_mouse_click(move_to: Mouse):
    return robot.click(move_to.x, move_to.y, move_to.seconds, move_to.button)


@router.post("/mouse/scroll")
async def post_mouse_scroll(move_to: Mouse):
    return robot.scroll(move_to.y)


@router.post("/keyboard/write")
async def post_keyboard_write(key_code: Key):
    return robot.write(key_code.text, key_code.interval)


@router.post("/keyboard/press")
async def post_keyboard_press(key_code: Key):
    return robot.press(key_code.press)


@router.post("/keyboard/down")
async def post_keyboard_down(key_code: Key):
    return robot.keyDown(key_code.press)


@router.post("/keyboard/up")
async def post_keyboard_up(key_code: Key):
    return robot.keyUp(key_code.press)
