from SmartDjango import Analyse
from django.views import View

from Article.models import ArticleP, Article, CommentP, Comment
from Base.auth import Auth
from User.models import MiniUser


class ArticleView(View):
    @staticmethod
    @Auth.require_login
    def get(r):
        user = r.user  # type: MiniUser
        return user.article_set.all().dict(Article.d_base)

    @staticmethod
    @Analyse.r([ArticleP.title, ArticleP.origin, ArticleP.author])
    @Auth.require_login
    def post(r):
        return Article.create(r.user, **r.d.dict()).d_create()


class ArticleIDView(View):
    @staticmethod
    @Analyse.r(a=[ArticleP.aid_getter])
    def get(r):
        article = r.d.article
        return article.d()


class CommentView(View):
    @staticmethod
    @Analyse.r(b=[CommentP.content, CommentP.reply_to_getter], a=[ArticleP.aid_getter])
    @Auth.require_login
    def post(r):
        article = r.d.article  # type: Article
        content = r.d.content
        reply_to = r.d.reply_to  # type: Comment

        if reply_to:
            return reply_to.reply(r.user, content).d()
        return article.comment(r.user, content).d()
