from project import app, db
from flask import redirect, render_template, request
from project.models.UserModel import User
from project.models.CategoryModel import Category
from project.models.EntryModel import Entry


@app.route('/')
def home():
    cat = Category()
    cat_list = cat.get_all_cat()
    query_result = db.session.query(Entry).filter(Entry.published == 1).order_by(Entry.created.desc()).all()
    return render_template('front-end/_index.html', post_list=query_result, cat_list=cat_list)


@app.route('/entry/<entry_slug>-<id>.html')
def entry_detail(entry_slug, id):
    cat = Category()
    cat_list = cat.get_all_cat()
    if id is not None and id != '' and int(id) > 0:
        if Entry.get_entry(id, 1) is not None and Entry.get_entry(id, 1).slug.lower() == entry_slug.lower():
            entry = Entry.get_entry(id, 1)
            related_posts = Entry.get_related_entry(id, entry.category.id)
        else:
            return redirect('/')
    else:
        return redirect('/')
    return render_template('front-end/_detail.html', entry=entry, cat_list=cat_list, related_posts=related_posts)


@app.route('/category/<cat_code>.html')
def category(cat_code):
    cat = Category()
    cat_list = cat.get_all_cat()
    if cat_code is not None and cat_code != '':
        entry_category = Entry.get_entry_by_cat(cat_code, 1)
    else:
        return redirect('/')
    return render_template('front-end/_category.html', cat_list=cat_list, entry_category=entry_category)


@app.route('/create_tables/')
def create_tables():
    db.create_all()
    db.session.add(User())
    db.session.add(Category())
    db.session.add(Entry())
    db.session.commit()

    return redirect('/login/')