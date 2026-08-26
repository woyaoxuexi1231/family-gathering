"""Jinja2 页面 — 表单直接调 service，与 /api 共用 store。"""

from pathlib import Path
from urllib.parse import quote

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from family_gathering.errors import DomainError
from family_gathering.models import DishStatus, ParticipantStatus
from family_gathering.persistence.store import GatheringStore, get_store
from family_gathering.services import dishes as dish_service
from family_gathering.services import overview as overview_service
from family_gathering.services import participants as participant_service

TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

router = APIRouter(tags=["web"])

STATUS_LABELS = {
    ParticipantStatus.COMING: "来",
    ParticipantStatus.MAYBE: "待定",
    ParticipantStatus.DECLINED: "不来",
    DishStatus.OPEN: "待认领",
    DishStatus.CLAIMED: "已认领",
    DishStatus.DONE: "已完成",
}


def _redirect(msg: str | None = None, *, error: bool = False) -> RedirectResponse:
    if msg:
        key = "error" if error else "msg"
        return RedirectResponse(url=f"/?{key}={quote(msg)}", status_code=303)
    return RedirectResponse(url="/", status_code=303)


def _build_context(store: GatheringStore, request: Request) -> dict:
    gathering = store.load()
    stats, gathering = overview_service.build_overview(gathering)
    name_by_id = {p.id: p.name for p in gathering.participants}

    return {
        "request": request,
        "meta": gathering.meta,
        "stats": stats,
        "participants": gathering.participants,
        "dishes": gathering.dishes,
        "name_by_id": name_by_id,
        "status_labels": STATUS_LABELS,
        "participant_statuses": list(ParticipantStatus),
        "flash_msg": request.query_params.get("msg"),
        "flash_error": request.query_params.get("error"),
    }


@router.get("/", response_class=HTMLResponse)
def home(request: Request, store: GatheringStore = Depends(get_store)) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context=_build_context(store, request),
    )


@router.post("/participants")
def web_add_participant(
    store: GatheringStore = Depends(get_store),
    name: str = Form(...),
    headcount: int = Form(1),
    status: ParticipantStatus = Form(ParticipantStatus.COMING),
    note: str = Form(""),
) -> RedirectResponse:
    try:
        store.update(
            lambda g: participant_service.add_participant(
                g,
                name=name,
                headcount=headcount,
                status=status,
                note=note,
            )
        )
        return _redirect("报名成功")
    except DomainError as exc:
        return _redirect(str(exc), error=True)


@router.post("/participants/{participant_id}/delete")
def web_delete_participant(
    participant_id: str,
    store: GatheringStore = Depends(get_store),
) -> RedirectResponse:
    try:
        store.update(lambda g: participant_service.remove_participant(g, participant_id))
        return _redirect("已移除参与人")
    except DomainError as exc:
        return _redirect(str(exc), error=True)


@router.post("/dishes")
def web_add_dish(
    store: GatheringStore = Depends(get_store),
    name: str = Form(...),
    servings: str = Form(""),
) -> RedirectResponse:
    try:
        store.update(lambda g: dish_service.add_dish(g, name=name, servings=servings))
        return _redirect("已添加菜品")
    except DomainError as exc:
        return _redirect(str(exc), error=True)


@router.post("/dishes/{dish_id}/claim")
def web_claim_dish(
    dish_id: str,
    store: GatheringStore = Depends(get_store),
    participant_id: str = Form(...),
) -> RedirectResponse:
    try:
        store.update(lambda g: dish_service.claim_dish(g, dish_id, participant_id))
        return _redirect("认领成功")
    except DomainError as exc:
        return _redirect(str(exc), error=True)


@router.post("/dishes/{dish_id}/unclaim")
def web_unclaim_dish(
    dish_id: str,
    store: GatheringStore = Depends(get_store),
) -> RedirectResponse:
    try:
        store.update(lambda g: dish_service.unclaim_dish(g, dish_id))
        return _redirect("已取消认领")
    except DomainError as exc:
        return _redirect(str(exc), error=True)
