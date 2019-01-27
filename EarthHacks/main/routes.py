from flask import render_template, url_for, flash, redirect
from main import app, db, bcrypt
from main.models import User, Receipt, Item, Material, Method
from main.forms import RegistrationForm, LoginForm
from flask_login import login_user, current_user, logout_user, login_required
from flask_table import Table, Col, LinkCol

class ReceiptList(Table):
    id = Col('Id', show=False)
    date = Col('Date')
    store = Col('Store')
    location = Col('Location')
    items = LinkCol('Items', 'receipt', url_kwargs=dict(id='id'))


class ItemList(Table):
    id = Col('Id', show=False)
    name = Col('Name')
    materials = LinkCol('Materials', 'item', url_kwargs=dict(id='id'))

class MaterialList(Table):
    id = Col('Id', show=False)
    name = Col('Name')
    # method = Col('Method')
    
    
    

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', title='Sort It Out!')


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))
    
@app.route("/account")
@login_required
def account():
    receipts = current_user.receipt
    
    if not receipts:
        flash('No receipts found')
        return redirect('/home')
    else:
        table = ReceiptList(receipts)
        table.border = True
    return render_template('account.html', title='Account', table=table)
    
@app.route('/account/receipt/<int:id>', methods=['GET', 'POST'])
@login_required
def receipt(id):
    receipt = Receipt.query.get(id)
    items = receipt.item
    table = ItemList(items)
    table.border = True
    return render_template('receipt.html', title='Receipts', table=table)
    
@app.route('/account/receipt/<int:receipt_id>/<int:item_id>', methods=['GET', 'POST'])
@login_required
def item(receipt_id, item_id):
    receipt = Receipt.query.get(id)
    items = receipt.item
    materials = items.material
    table = MaterialList(materials)
    table.border = True
    return render_template('item.html', title='Items', table=table)
