from fastapi import FastAPI, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from repository import CommentsRepository

app = FastAPI()

templates = Jinja2Templates(directory="templates")
repository = CommentsRepository()

@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/comments")
def get_comments(request: Request, page: int = 1, limit: int = 5 ):
    comments = repository.get_all()
    comments = sorted(comments, key=lambda x: x['id'], reverse=True)
    length = [i+1 for i in range((len(comments)-1)//limit+1)]
    start = (page-1)*limit
    end = start + limit
    comments = comments[start:end]
    return templates.TemplateResponse(
        "comments/index.html",
        {"request": request, "comments": comments, 'length': length},
    )
    
@app.post('/comments')
def add_comment(request: Request, comment: str = Form(...), category: str = Form(...)):
    repository.save(
        {'text': comment,
         'category': category,}
    )
    return RedirectResponse('/comments', status_code = 303)
    
    
    