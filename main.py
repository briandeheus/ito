import datetime

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.exc import NoResultFound
from sqlmodel import Session, SQLModel, col, create_engine, select

from models.entries import Entry

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")
engine = create_engine("sqlite:///database.db")

SQLModel.metadata.create_all(engine)


@app.get("/", response_class=HTMLResponse)
async def landing(request: Request):
    return templates.TemplateResponse(request=request, name="base.html")


class CreateEntry(BaseModel):
    content: str


@app.get("/api/v1/entries")
async def create_entry(request: Request, before: str = None, limit: int = 50):
    with Session(engine) as session:
        count_query = select(func.count()).select_from(Entry)
        total_count = session.exec(count_query).one()

        entry_query = select(Entry).order_by(col(Entry.created_on).desc())

        if before:
            entry_query = entry_query.where(
                Entry.created_on < datetime.datetime.fromisoformat(before)
            )

        entries = session.exec(entry_query.limit(limit)).all()

        data = [
            {
                "content": entry.content,
                "created_on": entry.format_created_on(),
                "id": entry.id,
            }
            for entry in entries
        ]
        return JSONResponse({"entries": data, "count": total_count})


@app.post("/api/v1/entries")
async def create_entry(request: Request, entry: CreateEntry):
    with Session(engine) as session:
        new_entry = Entry(content=entry.content, created_on=datetime.datetime.utcnow())
        session.add(new_entry)
        session.commit()
        return JSONResponse(
            {
                "content": new_entry.content,
                "created_on": new_entry.format_created_on(),
                "id": new_entry.id,
            }
        )


@app.delete("/api/v1/entries/{entry_id}")
async def delete_entry(request: Request, entry_id: int):
    with Session(engine) as session:

        try:
            entry = session.exec(select(Entry).where(Entry.id == entry_id)).one()
        except NoResultFound:
            return JSONResponse({"delete": False})

        session.delete(entry)
        session.commit()

        return JSONResponse({"delete": True})
