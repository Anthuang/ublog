from utils import *
from models.blogposts import *
from models.likes import *

class Blog(Handler):
    @login_required
    def get(self):
        entries = BlogPosts.all().order('-created')
        self.render('blog.html', entries=entries, name=self.user.username)

class NewPost(Handler):
    @login_required
    def get(self):
        self.render('newpost.html')

    @login_required
    def post(self):
        subject = self.request.get('subject')
        content = self.request.get('content')

        if subject and content:
            entry = BlogPosts(title=subject, body=content, owner=self.user.username, likes=0)
            entry.put()
            self.redirect('/newpost/' + str(entry.key().id()))
        else:
            self.render('newpost.html', error='Please fill out both fields!')

class NewPostID(Handler):
    @login_required
    def get(self, post_id):
        post = BlogPosts.get_by_id(int(post_id))
        if not post:
            self.error(404)
            return
        comments = post.comments.order('created')
        liked = Likes.all().ancestor(post).filter('owner', self.user.username).get()
        if liked:
            self.render('blogpost.html', entry=post, comments=comments, liked=True)
        else:
            self.render('blogpost.html', entry=post, comments=comments, liked=False)

class Edit(Handler):
    @login_required
    def get(self, post_id):
        post = BlogPosts.get_by_id(int(post_id))
        if not post:
            self.error(404)
            return
        if self.user.username == post.owner:
            self.render('editpost.html', entry=post, can_edit=True)
        else:
            error = 'You cannot change posts you do not own'
            self.render('editpost.html', entry=post, can_edit=False, error=error)

    @login_required
    def post(self, post_id):
        subject = self.request.get('subject')
        content = self.request.get('content')

        if subject and content:
            post = BlogPosts.get_by_id(int(post_id))
            if not post:
                self.error(404)
                return
            if self.user.username != post.owner:
                error = 'You cannot change comments you do not own'
                self.render('editpost.html', entry=comment.post, can_edit=False, error=error)
            post.title = subject
            post.body = content
            post.put()
            self.redirect('/newpost/' + str(post.key().id()))
        else:
            self.render('editpost.html', error='Please fill out both fields!')

class Delete(Handler):
    @login_required
    def get(self, post_id):
        post = BlogPosts.get_by_id(int(post_id))
        if not post:
            self.error(404)
            return
        if self.user.username == post.owner:
            post.delete()
            self.redirect('/')
        else:
            error = 'You cannot change posts you do not own'
            self.render('editpost.html', entry=post, can_edit=False, error=error)