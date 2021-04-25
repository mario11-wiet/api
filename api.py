from flask import Flask, redirect, render_template, request, url_for
import requests

token_users = "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"

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def main():
    try:
        if request.method == "POST":
            user = request.form["nm"]
            return redirect(url_for("users", nick=user))
        else:
            return render_template("main.html")
    except Exception as e:
        return render_template("error2.html", error=e)


@app.route('/users/<nick>', methods=["GET"])
def users(nick):
    try:
        user_data = url_git(nick)
        array = []
        photo = user_data[0]['owner']
        photo = photo['avatar_url']
        for i in user_data:
            array.append({
                'name': i['name'],
                'stars': i['stargazers_count'],
                'url': i['html_url']
            })
        return render_template("users.html", content=array, photo=photo, nick=nick)
    except Exception:
        return render_template("error.html", nick=nick)


@app.route('/users/<nick>/stars', methods=["GET"])
def stars(nick):
    try:
        user_data = url_git(nick)
        count = 0
        photo = user_data[0]['owner']
        photo = photo['avatar_url']
        for i in user_data:
            count += i['stargazers_count']
        return render_template("star.html", count=count, photo=photo, nick=nick)
    except Exception as e:
        return render_template("error2.html", error=e)


def url_git(nick):
    url = f"https://api.github.com/users/{nick}/repos"
    if token_users:
        autorization = f'token {token_users}'
        user_data = requests.get(url, headers={'Authorization': autorization}).json()
    else:
        user_data = requests.get(url)
    return user_data


if __name__ == "__main__":
    app.run()
