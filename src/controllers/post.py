from flask import Blueprint, request, jsonify
from src.app import Post, db
from http import HTTPStatus


bp = Blueprint('post',__name__,url_prefix='/posts')


def create_post():
    data = request.json
    post = Post(title=data["title"], body=data["body"], author_id=data['author_id'])
    db.session.add(post)
    db.session.commit()


def list_posts():
    query = db.select(Post)
    posts = db.session.execute(query).scalars()

    return [
        {
            "id": post.id,
            "title": post.title,
            "body": post.body,
            "author_id": post.author_id
        }
        for post in posts
    ]


@bp.route('/', methods = ['GET', 'POST'])
def get_or_create_post():
    if request.method == 'GET':
        return {
            "Post": list_posts()
        }
    else:
        create_post()
        return {
            'message':'Post added!'

        }, HTTPStatus.CREATED


@bp.route("/<int:author_id>", methods=["DELETE"])
def delete_post(author_id):
    # Realizing DELETE with using a foreign key instead of a primary key
    # Realizando DELETE usando uma chave estrangeira em vez de uma chave primária
    post = Post.query.filter_by(author_id=Post.author_id).first_or_404()
    db.session.delete(post)
    db.session.commit()

    return '', HTTPStatus.NO_CONTENT

@bp.route("/<int:id>", methods=["PATCH"])
def update_post(id):
    data = request.json
    post = db.get_or_404(Post, id)
    
    if 'title' and 'body' in data:
        post.title =  data["title"]
        post.body = data["body"]
        db.session.commit()

    return ''