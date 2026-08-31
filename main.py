from fastapi import FastAPI, Depends, Request, Form as FastAPIForm, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database import engine, get_db, Base
from models import Form, Question, Response, Answer
from schemas import FormCreate

# Creates tables on startup if they don't exist yet (fine for a small app;
# use Alembic migrations if this grows).
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Forms App")
templates = Jinja2Templates(directory="templates")


# ---------- JSON API: create a form ----------
@app.post("/api/forms")
def create_form(payload: FormCreate, db: Session = Depends(get_db)):
    form = Form(title=payload.title, description=payload.description or "")
    db.add(form)
    db.flush()  # get form.id before adding questions

    for i, q in enumerate(payload.questions):
        db.add(Question(
            form_id=form.id,
            label=q.label,
            field_type=q.field_type,
            options=q.options or "",
            required=q.required,
            position=i,
        ))
    db.commit()
    db.refresh(form)
    return {"id": form.id, "share_url": f"/f/{form.id}"}


# ---------- Simple builder page ----------
@app.get("/", response_class=HTMLResponse)
def builder_page(request: Request):
    return templates.TemplateResponse("create.html", {"request": request})


# ---------- Public shareable form page ----------
@app.get("/f/{form_id}", response_class=HTMLResponse)
def view_form(form_id: str, request: Request, db: Session = Depends(get_db)):
    form = db.query(Form).filter(Form.id == form_id).first()
    if not form:
        raise HTTPException(status_code=404, detail="Form not found")
    return templates.TemplateResponse(
        "form.html", {"request": request, "form": form}
    )


# ---------- Submit a response (plain HTML form POST) ----------
@app.post("/f/{form_id}/submit")
async def submit_form(form_id: str, request: Request, db: Session = Depends(get_db)):
    form = db.query(Form).filter(Form.id == form_id).first()
    if not form:
        raise HTTPException(status_code=404, detail="Form not found")

    form_data = await request.form()
    response = Response(form_id=form.id)
    db.add(response)
    db.flush()

    for question in form.questions:
        key = f"q_{question.id}"
        if question.field_type == "checkbox":
            values = form_data.getlist(key)
            value = ", ".join(values)
        else:
            value = form_data.get(key, "")
        db.add(Answer(response_id=response.id, question_id=question.id, value=value))

    db.commit()
    return RedirectResponse(url=f"/f/{form_id}/thanks", status_code=303)


@app.get("/f/{form_id}/thanks", response_class=HTMLResponse)
def thanks(form_id: str, request: Request):
    return templates.TemplateResponse(
        "thanks.html", {"request": request, "form_id": form_id}
    )


# ---------- Results (would add auth in a real deployment) ----------
@app.get("/f/{form_id}/results", response_class=HTMLResponse)
def results(form_id: str, request: Request, db: Session = Depends(get_db)):
    form = db.query(Form).filter(Form.id == form_id).first()
    if not form:
        raise HTTPException(status_code=404, detail="Form not found")
    responses = db.query(Response).filter(Response.form_id == form_id).all()
    return templates.TemplateResponse(
        "results.html", {"request": request, "form": form, "responses": responses}
    )
