from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp

from helpers import *

# configure application
app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# custom filter
app.jinja_env.filters["usd"] = usd

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

@app.route("/")
@login_required
def index():

    #retrieve portfolio
    portfolio=db.execute("SELECT shares, symbol FROM portfolios WHERE id= :id", id=session["user_id"])

    grandTotal=0

    for stock in portfolio:

        #store elements
        shares=stock["shares"]
        symbol=stock["symbol"]

        #update price and total
        quote=lookup(symbol)
        newPrice=quote["price"]
        newTotal=round(shares*newPrice,2)
        db.execute("UPDATE portfolios SET price= :price, total= :total WHERE id= :id AND symbol= :symbol", price=newPrice, total=newTotal,
            id=session["user_id"], symbol=symbol)

        #add to grand total
        grandTotal+=newTotal

    #add cash
    userCash=db.execute("SELECT cash FROM users WHERE id= :id", id=session["user_id"])
    grandTotal+=round(userCash[0]["cash"],2)

    #retrieve new portfolio
    newPortfolio=db.execute("SELECT * FROM portfolios WHERE id= :id", id=session["user_id"])

    return render_template("index.html", portfolio=newPortfolio, cash=round(userCash[0]["cash"],2), total=round(grandTotal,2))

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock."""
    if request.method == "POST":
        #ensure there is a symbol for lookup
        if not request.form.get("symbol"):
            return apology("must enter symbol")
        #ensure that number of shares is filled
        if not request.form.get("shares"):
            return apology("must enter number of shares")

        shareTemp=int(request.form.get("shares"))

        #ensure that number of shares is nonnegative
        if shareTemp<=0:
            return apology("number of shares must be a positive integer")

        #ensure that the stock exists
        quote = lookup(request.form.get("symbol"))
        if quote == None:
            return apology("invalid symbol")

        #retrieve user's cash
        cash = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])

        #check if user has enough cash to buy
        if cash==None or cash[0]["cash"] < (quote["price"]*shareTemp):
            return apology("not enough cash")

        #update portfolios
        #find the entry in portfolios
        userShares=db.execute("SELECT shares FROM portfolios WHERE id= :id AND symbol= :symbol", id=session["user_id"], symbol=request.form.get("symbol"))
        #if entry does not already exist
        if not userShares:
            db.execute("INSERT INTO portfolios (id, symbol, name, shares, price, total) VALUES ( :id, :symbol, :name, :shares, :price, :total)",
                id=session["user_id"], symbol=request.form.get("symbol"), name=quote["name"], shares=shareTemp, price=quote["price"],
                total=(quote["price"]*shareTemp))
        #if entry already exists
        else:
            db.execute("UPDATE portfolios SET shares=shares+ :newShares WHERE id= :id AND symbol= :symbol",
                newShares=shareTemp, id=session["user_id"], symbol=request.form.get("symbol"))
            db.execute("UPDATE portfolios SET total=total+ :payment WHERE id= :id AND symbol= :symbol",
                payment=quote["price"]*shareTemp, id=session["user_id"], symbol=request.form.get("symbol"))

        #update transactions
        db.execute("INSERT INTO transactions (id, symbol, name, shares, price, payment) VALUES ( :id, :symbol, :name, :shares, :price, :payment)",
            id=session["user_id"], symbol=request.form.get("symbol"), name=quote["name"], shares=shareTemp, price=quote["price"],
            payment=(quote["price"]*shareTemp))

        #update cash
        db.execute("UPDATE users SET cash=cash- :payment WHERE id= :id", payment=(quote["price"]*shareTemp), id=session["user_id"])


        return redirect(url_for("index"))

    else:
        return render_template("buy.html")

@app.route("/history")
@login_required
def history():
    """Show history of transactions."""
    transactions=db.execute("SELECT * FROM transactions WHERE id= :id", id=session["user_id"])

    return render_template("history.html", transactions=transactions)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            return apology("invalid username and/or password")

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("login"))

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    if request.method == "POST":
        #ensure there is a symbol for lookup
        if not request.form.get("symbol"):
            return apology("must enter symbol")

        quote = lookup(request.form.get("symbol"))
        if quote == None:
            return apology("invalid symbol")

        return render_template("quoteResult.html", name=quote["name"], symbol=quote["symbol"], price=quote["price"])

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("quote.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""

    if request.method == "POST":
        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # ensure password was retyped
        elif not request.form.get("passwordConfirmation"):
            return apology("must retype password")

        #ensure password equals retyped password
        elif request.form.get("password")!=request.form.get("passwordConfirmation"):
            return apology("passwords don't match")

        #hash password
        password=pwd_context.hash(request.form.get("password"));

        result=db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)", username=request.form.get("username"), hash=password)
        if not result:
            return apology("username already exists")

        session["user_id"] = result

        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock."""

    if request.method == "POST":
        #ensure there is a symbol for lookup
        if not request.form.get("symbol"):
            return apology("must enter symbol")
        #ensure that number of shares is filled
        if not request.form.get("shares"):
            return apology("must enter number of shares")

        shareTemp=int(request.form.get("shares"))

        #ensure that the stock exists
        quote = lookup(request.form.get("symbol"))
        if quote == None:
            return apology("invalid symbol")

        #ensure that number of shares is nonnegative
        if shareTemp<=0:
            return apology("number of shares must be a positive integer")

        #retrieve user's shares
        userPort = db.execute("SELECT shares FROM portfolios WHERE id = :id AND symbol= :symbol", id=session["user_id"], symbol=request.form.get("symbol"))

        #check if user is selling more than they have
        if not userPort:
            return apology("nothing to sell")
        elif shareTemp>userPort[0]["shares"]:
            return apology("cannot sell more than you have")

        #update portfolios
        if (userPort[0]["shares"]>shareTemp):
            db.execute("UPDATE portfolios SET shares=shares- :soldShares WHERE id= :id AND symbol= :symbol",
                soldShares=shareTemp, id=session["user_id"], symbol=request.form.get("symbol"))
            db.execute("UPDATE portfolios SET total=total- :payment WHERE id= :id AND symbol= :symbol",
                payment=quote["price"]*shareTemp, id=session["user_id"], symbol=request.form.get("symbol"))
        else:
            db.execute("DELETE FROM portfolios WHERE id= :id AND symbol= :symbol", id=session["user_id"], symbol=request.form.get("symbol"))

        #update transactions
        db.execute("INSERT INTO transactions (id, symbol, name, shares, price, payment) VALUES ( :id, :symbol, :name, :shares, :price, :payment)",
            id=session["user_id"], symbol=request.form.get("symbol"), name=quote["name"], shares=0-shareTemp, price=quote["price"],
            payment=0-(quote["price"]*shareTemp))

        #update cash
        db.execute("UPDATE users SET cash=cash+ :payment WHERE id= :id", payment=(quote["price"]*shareTemp), id=session["user_id"])

        return redirect(url_for("index"))


    else:
        return render_template("sell.html")

@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    """User settings"""

    if request.method == "POST":
        #https://stackoverflow.com/questions/43811779/use-many-submit-buttons-in-the-same-form

        #if it is submitted for password change
        if request.form['change']=='password':
            # ensure old password was submitted
            if not request.form.get("oldPassword"):
                return apology("must provide old password")

            # ensure new password was submitted
            elif not request.form.get("newPassword"):
                return apology("must provide new password")

            # ensure password was confirmed
            elif not request.form.get("passConfirm"):
                return apology("must confirm new password")

            else:
                #ensure olf password is correct
                passTemp=db.execute("SELECT hash FROM users WHERE id= :id", id=session["user_id"])
                if not pwd_context.verify(request.form.get("oldPassword"), passTemp[0]["hash"]):
                    return apology("incorrect old password")
                #ensure new passwords match
                elif request.form.get("newPassword")!=request.form.get("passConfirm"):
                    return apology("new passwords don't match")
                else:
                    passTemp=pwd_context.hash(request.form.get("newPassword"))
                    db.execute("UPDATE users SET hash= :newPassword WHERE id= :id", newPassword=passTemp, id= session["user_id"])
                    return success("success")

        #change for username
        elif request.form['change']=='username':
            if not request.form.get("newUsername"):
                return apology("must enter new username")

            #check if username already exists
            idTemp=db.execute("SELECT id from users WHERE username= :newUser", newUser=request.form.get("newUsername"))
            if idTemp and idTemp[0][id]!=session["user_id"]:
                return apology("username already exists")
            else:
                db.execute("UPDATE users SET username= :newUsername WHERE id= :id", newUsername=request.form.get("newUsername"), id= session["user_id"])

            return success("SUCCESS")

    else:
        user=db.execute("SELECT username FROM users WHERE id= :id", id=session["user_id"])
        return render_template("settings.html",username=user[0]["username"])

