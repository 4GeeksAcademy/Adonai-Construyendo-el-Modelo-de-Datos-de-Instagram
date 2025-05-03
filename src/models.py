from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

import enum
class MediaType(enum.Enum):
    photo = "photo"
    video = "video"

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    firstname = db.Column(db.String)
    lastname = db.Column(db.String)
    email = db.Column(db.String, nullable=False)

    posts = db.relationship("Post", back_populates="user")
    comments = db.relationship("Comment", back_populates="author")
    followers = db.relationship(
        "Follower",
        foreign_keys="Follower.user_to_id",
        back_populates="user_to"
    )
    following = db.relationship(
        "Follower",
        foreign_keys="Follower.user_from_id",
        back_populates="user_from"
    )


class Post(db.Model):
    __tablename__ = "post"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    
    user = db.relationship("User", back_populates="posts")
    comments = db.relationship("Comment", back_populates="post")
    media = db.relationship("Media", back_populates="post")


class Comment(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True)
    comment_text = db.Column(db.String, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=False)

    author = db.relationship("User", back_populates="comments")
    post = db.relationship("Post", back_populates="comments")


class Media(db.Model):
    __tablename__ = "media"
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Enum(MediaType), nullable=False)
    uri = db.Column(db.String, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=False)

    
    post = db.relationship("Post", back_populates="media")


class Follower(db.Model):
    __tablename__ = "follower"
    user_from_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    user_to_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)

    # Relaciones
    user_from = db.relationship("User", foreign_keys=[user_from_id], back_populates="following")
    user_to = db.relationship("User", foreign_keys=[user_to_id], back_populates="followers")


if __name__ == "__main__":
    print("Modelos definidos. Ejecuta este script para generar el diagrama.")

if __name__ == "__main__":
    from sqlalchemy_schemadisplay import create_schema_graph
    from sqlalchemy import MetaData

    
    graph = create_schema_graph(
        metadata=MetaData(),
        show_datatypes=True,
        show_indexes=True,
        rankdir='LR',  # Orientación del diagrama
        concentrate=False
    )
    graph.write_png('diagram.png')  # Guardar el diagrama como diagram.png
    print("Diagrama generado como diagram.png")