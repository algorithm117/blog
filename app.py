from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)


def get_blog_data():
    file = open("blog_posts_data.json")
    blog_posts = json.load(file)

    return blog_posts

@app.route('/like/<int:post_id>')
def like(post_id):
    blog_posts = get_blog_data()
    blog_post = blog_posts['posts'][post_id - 1]
    new_amount_of_likes = blog_post['likes'] + 1

    new_blog_post_data = {"id": blog_post['id'], "author": blog_post['author'], "title": blog_post['title'], "content": blog_post['content'], "likes": new_amount_of_likes}

    blog_posts['posts'][blog_post['id'] - 1] = new_blog_post_data
    with open('blog_posts_data.json', "w") as file:
        json.dump(blog_posts, file)

    return redirect(url_for('index'))

@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    blog_posts = get_blog_data()
    blog_post = blog_posts['posts'][post_id - 1]
    if blog_post is None:
        return "Post not found", 404

    if request.method == 'POST':
        author = request.form['author']
        title = request.form['title']
        content = request.form['content']

        new_blog_post_data = {"id": blog_post['id'], "author": author, "title": title, "content": content}

        blog_posts['posts'][blog_post['id'] - 1] = new_blog_post_data
        with open('blog_posts_data.json', "w") as file:
            json.dump(blog_posts, file)

        return redirect(url_for('index'))

    # else it is a GET request
    return render_template('update.html', post=blog_post)

@app.route('/delete/<int:post_id>')
def delete(post_id):
    blog_posts = get_blog_data()
    blog_posts['posts'].pop(post_id - 1)
    new_blog_posts = blog_posts
    with open('blog_posts_data.json', "w") as file:
        json.dump(new_blog_posts, file)
    return redirect(url_for('index'))

@app.route("/add", methods=['GET', 'POST'])
def add():
    blog_posts = get_blog_data()
    if request.method == 'POST':
        author = request.form['author']
        title = request.form['title']
        content = request.form['content']
        last_id = None
        if len(blog_posts['posts']) == 0:
            last_id = 0
        else:
            last_id = blog_posts['posts'][-1]['id']
        new_id = last_id + 1
        new_blog_post_data = {"id": new_id, "author": author, "title": title, "content": content}

        blog_posts['posts'].append(new_blog_post_data)
        with open('blog_posts_data.json', "w") as file:
            json.dump(blog_posts, file)

        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/')
def index():
    blog_posts = get_blog_data()['posts']
    return render_template('index.html', posts=blog_posts)


if __name__ == '__main__':
    app.run()
