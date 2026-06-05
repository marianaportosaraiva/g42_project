from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from classes.university import University
from classes.program import Program
from classes.faculty import Faculty
from classes.partnership import Partnership
from classes.userlogin import UserLogin
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import json
import plotly.graph_objects as go
import plotly.express as px

app = Flask(__name__)
app.secret_key = 'g42_secret_key'

# Load all data from the database
University.read('data/g42_database.sqlite')
Program.read('data/g42_database.sqlite')
Faculty.read('data/g42_database.sqlite')
Partnership.read('data/g42_database.sqlite')
UserLogin.read('data/g42_database.sqlite')

# HOME
@app.route("/")
@app.route("/home")
def home():
    stats = {
        'universities': len(University.lst),
        'programs':     len(Program.lst),
        'faculties':    len(Faculty.lst),
        'partnerships': len(Partnership.lst),
    }
    return render_template("index.html", stats=stats, ulogin=session.get("user"))


# LOGIN / LOGOFF
@app.route("/login")
def login():
    return render_template("login.html",
                           user="", password="",
                           ulogin=session.get("user"), resul="")

@app.route("/logoff")
def logoff():
    session.pop("user", None)
    return render_template("index.html", ulogin=session.get("user"),
                           stats={
                               'universities': len(University.lst),
                               'programs':     len(Program.lst),
                               'faculties':    len(Faculty.lst),
                               'partnerships': len(Partnership.lst),
                           })

@app.route("/chklogin", methods=["post", "get"])
def chklogin():
    user     = request.form["user"]
    password = request.form["password"]
    resul    = UserLogin.chk_password(user, password)
    if resul == "Valid":
        session["user"] = user
        stats = {
            'universities': len(University.lst),
            'programs':     len(Program.lst),
            'faculties':    len(Faculty.lst),
            'partnerships': len(Partnership.lst),
        }
        return render_template("index.html", ulogin=session.get("user"), stats=stats)
    return render_template("login.html", user=user, password=password,
                           ulogin=session.get("user"), resul=resul)


# UNIVERSITY
@app.route("/university", methods=["post", "get"])
def university():
    global prev_option_univ
    if not session.get("user"):
        return redirect(url_for("login"))
    butshow, butedit = "enabled", "disabled"
    option = request.args.get("option")

    if option == "edit":
        butshow, butedit = "disabled", "enabled"
    elif option == "delete":
        obj = University.current()
        if obj:
            University.remove(obj.id)
            if not University.previous():
                University.first()
    elif option == "insert":
        butshow, butedit = "disabled", "enabled"
    elif option == "cancel":
        pass
    elif prev_option_univ == "insert" and option == "save":
        strobj = str(University.get_id(0)) + ";" + request.form["name"] + ";" + request.form["created_date"]
        obj = University.from_string(strobj)
        University.insert(obj.id)
        University.last()
    elif prev_option_univ == "edit" and option == "save":
        obj = University.current()
        obj.name = request.form["name"]
        obj.created_date = request.form["created_date"]
        University.update(obj.id)
    elif option == "first":    University.first()
    elif option == "previous": University.previous()
    elif option == "next":     University.nextrec()
    elif option == "last":     University.last()

    prev_option_univ = option
    obj = University.current()
    if option == "insert" or len(University.lst) == 0:
        id, name, created_date = University.get_id(0), "", ""
    else:
        id, name, created_date = obj.id, obj.name, obj.created_date

    pos   = University.pos + 1
    total = len(University.lst)
    return render_template("university.html", butshow=butshow, butedit=butedit,
                           id=id, name=name, created_date=created_date,
                           pos=pos, total=total, ulogin=session.get("user"))

prev_option_univ = ""


# PROGRAM
@app.route("/program", methods=["post", "get"])
def program():
    global prev_option_prog
    if not session.get("user"):
        return redirect(url_for("login"))
    butshow, butedit = "enabled", "disabled"
    option = request.args.get("option")

    if option == "edit":
        butshow, butedit = "disabled", "enabled"
    elif option == "delete":
        obj = Program.current()
        if obj:
            Program.remove(obj.id)
            if not Program.previous():
                Program.first()
    elif option == "insert":
        butshow, butedit = "disabled", "enabled"
    elif option == "cancel":
        pass
    elif prev_option_prog == "insert" and option == "save":
        strobj = str(Program.get_id(0)) + ";" + request.form["title"] + ";" + request.form["category"]
        obj = Program.from_string(strobj)
        Program.insert(obj.id)
        Program.last()
    elif prev_option_prog == "edit" and option == "save":
        obj = Program.current()
        obj.title    = request.form["title"]
        obj.category = request.form["category"]
        Program.update(obj.id)
    elif option == "first":    Program.first()
    elif option == "previous": Program.previous()
    elif option == "next":     Program.nextrec()
    elif option == "last":     Program.last()

    prev_option_prog = option
    obj = Program.current()
    if option == "insert" or len(Program.lst) == 0:
        id, title, category = Program.get_id(0), "", ""
    else:
        id, title, category = obj.id, obj.title, obj.category

    pos   = Program.pos + 1
    total = len(Program.lst)
    return render_template("program.html", butshow=butshow, butedit=butedit,
                           id=id, title=title, category=category,
                           pos=pos, total=total, ulogin=session.get("user"))

prev_option_prog = ""


# FACULTY
@app.route("/faculty", methods=["post", "get"])
def faculty():
    global prev_option_fac
    if not session.get("user"):
        return redirect(url_for("login"))
    butshow, butedit = "enabled", "disabled"
    option = request.args.get("option")

    if option == "edit":
        butshow, butedit = "disabled", "enabled"
    elif option == "delete":
        obj = Faculty.current()
        if obj:
            Faculty.remove(obj.id)
            if not Faculty.previous():
                Faculty.first()
    elif option == "insert":
        butshow, butedit = "disabled", "enabled"
    elif option == "cancel":
        pass
    elif prev_option_fac == "insert" and option == "save":
        strobj = str(Faculty.get_id(0)) + ";" + request.form["info"] + ";" + request.form["university_id"]
        obj = Faculty.from_string(strobj)
        Faculty.insert(obj.id)
        Faculty.last()
    elif prev_option_fac == "edit" and option == "save":
        obj = Faculty.current()
        obj.info          = request.form["info"]
        obj.university_id = int(request.form["university_id"])
        Faculty.update(obj.id)
    elif option == "first":    Faculty.first()
    elif option == "previous": Faculty.previous()
    elif option == "next":     Faculty.nextrec()
    elif option == "last":     Faculty.last()

    prev_option_fac = option
    obj = Faculty.current()
    if option == "insert" or len(Faculty.lst) == 0:
        id, info, university_id = Faculty.get_id(0), "", ""
    else:
        id, info, university_id = obj.id, obj.info, obj.university_id

    univ_name = ""
    if university_id and university_id in University.obj:
        univ_name = University.obj[university_id].name

    pos   = Faculty.pos + 1
    total = len(Faculty.lst)
    return render_template("faculty.html", butshow=butshow, butedit=butedit,
                           id=id, info=info, university_id=university_id,
                           univ_name=univ_name, pos=pos, total=total,
                           ulogin=session.get("user"))

prev_option_fac = ""


# PARTNERSHIP
@app.route("/partnership", methods=["post", "get"])
def partnership():
    global prev_option_part
    if not session.get("user"):
        return redirect(url_for("login"))
    butshow, butedit = "enabled", "disabled"
    option = request.args.get("option")

    if option == "edit":
        butshow, butedit = "disabled", "enabled"
    elif option == "delete":
        obj = Partnership.current()
        if obj:
            Partnership.remove(obj.id)
            if not Partnership.previous():
                Partnership.first()
    elif option == "insert":
        butshow, butedit = "disabled", "enabled"
    elif option == "cancel":
        pass
    elif prev_option_part == "insert" and option == "save":
        new_id = Partnership.get_id(0)
        strobj = (str(new_id) + ";" + request.form["university_id"] + ";" +
                  request.form["program_id"] + ";" + request.form["course_start_date"] +
                  ";" + request.form["students_number"])
        obj = Partnership.from_string(strobj)
        Partnership.insert(obj.id)
        Partnership.last()
    elif prev_option_part == "edit" and option == "save":
        obj = Partnership.current()
        obj.university_id    = request.form["university_id"]
        obj.program_id       = request.form["program_id"]
        obj.course_start_date = request.form["course_start_date"]
        obj.students_number  = int(request.form["students_number"])
        Partnership.update(obj.id)
    elif option == "first":    Partnership.first()
    elif option == "previous": Partnership.previous()
    elif option == "next":     Partnership.nextrec()
    elif option == "last":     Partnership.last()

    prev_option_part = option
    obj = Partnership.current()
    if option == "insert" or len(Partnership.lst) == 0:
        id, university_id, program_id, course_start_date, students_number = Partnership.get_id(0), "", "", "", ""
    else:
        id              = obj.id
        university_id   = obj.university_id
        program_id      = obj.program_id
        course_start_date = obj.course_start_date
        students_number = obj.students_number

    univ_name  = University.obj[university_id].name if university_id in University.obj else ""
    prog_title = Program.obj[program_id].title       if program_id   in Program.obj    else ""

    pos   = Partnership.pos + 1
    total = len(Partnership.lst)
    return render_template("partnership.html", butshow=butshow, butedit=butedit,
                           id=id, university_id=university_id, program_id=program_id,
                           course_start_date=course_start_date, students_number=students_number,
                           univ_name=univ_name, prog_title=prog_title,
                           pos=pos, total=total, ulogin=session.get("user"))

prev_option_part = ""


# ANALYTICS (Pandas + Matplotlib)
@app.route("/analytics")
def analytics():
    if not session.get("user"):
        return redirect(url_for("login"))

    charts_dir = os.path.join(app.static_folder, "charts")
    os.makedirs(charts_dir, exist_ok=True)

    df_part = pd.DataFrame([{
        'university_id':   int(p.university_id),
        'program_id':      int(p.program_id),
        'course_start_date': p.course_start_date,
        'students_number': int(p.students_number)
    } for p in Partnership.obj.values()])

    df_univ = pd.DataFrame([{'id': int(u.id), 'name': u.name}
                             for u in University.obj.values()])

    df_prog = pd.DataFrame([{'id': int(p.id), 'category': p.category}
                             for p in Program.obj.values()])

    # Chart 1: Top 10 Universities by total students
    merged   = df_part.merge(df_univ, left_on='university_id', right_on='id')
    top_univ = merged.groupby('name')['students_number'].sum().nlargest(10)

    fig, ax = plt.subplots(figsize=(10, 5))
    top_univ.plot(kind='barh', ax=ax, color='#2d6a2d')
    ax.set_facecolor('#f0f8f0')
    fig.patch.set_facecolor('#ffffff')
    ax.tick_params(colors='#1a3a1a')
    ax.xaxis.label.set_color('#1a3a1a')
    ax.yaxis.label.set_color('#1a3a1a')
    ax.title.set_color('#1a3a1a')
    ax.set_title('Top 10 Universidades por Nr Total de Estudantes', fontsize=13, fontweight='bold')
    ax.set_xlabel('Total de Estudantes')
    ax.set_ylabel('Universidade')
    plt.tight_layout()
    fig.savefig(os.path.join(charts_dir, 'chart1.png'), facecolor=fig.get_facecolor())
    plt.close(fig)

    # Chart 2: Programs per Category (pie)
    cat_counts = df_prog['category'].value_counts()

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(cat_counts.values, labels=cat_counts.index, autopct='%1.1f%%',
           startangle=140, colors=plt.cm.Set3.colors)
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#1f2e17')
    ax.title.set_color('#1a3a1a')
    ax.set_title('Distribuicao de Programas por Categoria', fontsize=13, fontweight='bold')
    plt.tight_layout()
    fig.savefig(os.path.join(charts_dir, 'chart2.png'), facecolor=fig.get_facecolor())
    plt.close(fig)

    # Chart 3: Avg students per program category
    merged2 = df_part.merge(df_prog, left_on='program_id', right_on='id')
    avg_cat = merged2.groupby('category')['students_number'].mean().sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(10, 5))
    avg_cat.plot(kind='bar', ax=ax, color='#d4a030')
    ax.set_facecolor('#f0f8f0')
    fig.patch.set_facecolor('#ffffff')
    ax.tick_params(colors='#1a3a1a')
    ax.xaxis.label.set_color('#1a3a1a')
    ax.yaxis.label.set_color('#1a3a1a')
    ax.title.set_color('#1a3a1a')
    ax.set_title('Media de Estudantes por Categoria de Programa', fontsize=13, fontweight='bold')
    ax.set_xlabel('Categoria')
    ax.set_ylabel('Media de Estudantes')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    fig.savefig(os.path.join(charts_dir, 'chart3.png'), facecolor=fig.get_facecolor())
    plt.close(fig)

    stats = {
        'total_students': int(df_part['students_number'].sum()),
        'avg_students':   round(df_part['students_number'].mean(), 1),
        'max_students':   int(df_part['students_number'].max()),
        'num_categories': int(df_prog['category'].nunique()),
        'top_university': top_univ.index[0],
        'top_category':   cat_counts.index[0],
    }

    fig4 = go.Figure(go.Bar(
        x=top_univ.values.tolist(),
        y=top_univ.index.tolist(),
        orientation="h",
        marker_color="#2d6a2d",
        hovertemplate="%{y}: %{x} estudantes<extra></extra>",
    ))
    fig4.update_layout(
        title="Top 10 Universidades - Grafico Interativo",
        xaxis_title="Total de Estudantes",
        yaxis_title="Universidade",
        plot_bgcolor="#f0f8f0",
        paper_bgcolor="#ffffff",
        font=dict(color="#1a3a1a"),
        margin=dict(l=20, r=20, t=50, b=20),
    )
    plotly_chart4 = json.dumps(fig4.to_dict())

    # Plotly Chart 5: Avg students per category - bubble chart
    merged2 = df_part.merge(df_prog, left_on="program_id", right_on="id")
    avg_cat = merged2.groupby("category")["students_number"].mean().sort_values(ascending=False)
    counts  = merged2.groupby("category")["students_number"].count()

    sizes = [min(int(counts.get(c, 1)) * 6, 60) for c in avg_cat.index]
    fig5 = go.Figure()
    fig5.add_trace(go.Scatter(
        x=avg_cat.index.tolist(),
        y=avg_cat.values.tolist(),
        mode="markers+text",
        marker=dict(
            size=sizes,
            color=avg_cat.values.tolist(),
            colorscale="Greens",
            showscale=True,
            colorbar=dict(title="Media"),
        ),
        text=[f"{v:.1f}" for v in avg_cat.values],
        textposition="top center",
        hovertemplate="%{x}<br>Media: %{y:.1f} estudantes<extra></extra>",
    ))
    fig5.update_layout(
        title="Media de Estudantes por Categoria - Grafico de Bolhas",
        xaxis_title="Categoria",
        yaxis_title="Media de Estudantes",
        plot_bgcolor="#f0f8f0",
        paper_bgcolor="#ffffff",
        font=dict(color="#1a3a1a"),
        margin=dict(l=20, r=20, t=50, b=80),
    )
    plotly_chart5 = json.dumps(fig5.to_dict())

    return render_template("analytics.html", stats=stats,
                           plotly_chart4=plotly_chart4,
                           plotly_chart5=plotly_chart5,
                           ulogin=session.get("user"))


# USER LOGIN MANAGEMENT
prev_option_user = ""

@app.route("/Userlogin", methods=["post", "get"])
def userlogin():
    global prev_option_user
    if not session.get("user"):
        return redirect(url_for("login"))

    msg     = ""
    ulogin  = session.get("user")
    user_id = UserLogin.get_user_id(ulogin)
    group   = UserLogin.obj[user_id].usergroup if user_id != 0 else ""

    # Set cursor to the current user if admin navigated here
    if group == "admin":
        UserLogin.current(user_id)

    butshow, butedit = "enabled", "disabled"
    option = request.args.get("option")

    if option == "edit":
        butshow, butedit = "disabled", "enabled"

    elif option == "delete":
        obj = UserLogin.current()
        if obj.id != user_id:
            UserLogin.remove(obj.id)
            if not UserLogin.previous():
                UserLogin.first()
        else:
            msg = "You cannot delete the same user"

    elif option == "insert":
        butshow, butedit = "disabled", "enabled"

    elif option == "cancel":
        pass

    elif prev_option_user == "insert" and option == "save":
        user = request.form["user"]
        if len(UserLogin.find(user, "username")) == 0:
            usergroup = request.form["usergroup"]
            password  = request.form["password"]
            obj = UserLogin(0, user, UserLogin.set_password(password), usergroup)
            UserLogin.insert(obj.id)
            UserLogin.last()
        else:
            msg = "duplicate username"
            UserLogin.current()

    elif prev_option_user == "edit" and option == "save":
        obj = UserLogin.current()
        if group == "admin":
            obj.usergroup = request.form["usergroup"]
        if request.form["password"] != "":
            obj._password = UserLogin.set_password(request.form["password"])
        UserLogin.update(obj.id)

    elif option == "first":    UserLogin.first()
    elif option == "previous": UserLogin.previous()
    elif option == "next":     UserLogin.nextrec()
    elif option == "last":     UserLogin.last()
    elif option == "exit":
        return render_template("index.html", ulogin=ulogin,
                               stats={
                                   'universities': len(University.lst),
                                   'programs':     len(Program.lst),
                                   'faculties':    len(Faculty.lst),
                                   'partnerships': len(Partnership.lst),
                               })

    prev_option_user = option
    obj = UserLogin.current()

    if option == "insert" or len(UserLogin.lst) == 0:
        id, user, usergroup, password = UserLogin.get_id(0), "", "", ""
    else:
        id        = obj.id
        user      = obj.username
        usergroup = obj.usergroup
        password  = ""

    pos   = UserLogin.pos + 1
    total = len(UserLogin.lst)

    return render_template("userlogin.html",
                           butshow=butshow, butedit=butedit,
                           msg=msg, id=id, user=user,
                           usergroup=usergroup, password=password,
                           pos=pos, total=total,
                           ulogin=ulogin, group=group)


if __name__ == '__main__':
    app.run(debug=True)
