
import flask
from flask import render_template, url_for, flash, redirect, request, abort
from myblog import app, ndb, bcrypt
from myblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from myblog.models import Admin, Intern, Mentor, Post, Task
from flask_login import login_user, current_user, logout_user, login_required
from google.cloud import ndb

client = ndb.Client()


@app.route('/home')
@app.route('/')
def home():
    post_list = []
    with client.context():
        posts = Post.query().order(-Post.posted_at).fetch()
        for each_post in posts:
            post_dict = dict()
            # print(each_post.key.id())
            post_dict['post_id'] = each_post.key.id()
            post_dict['title'] = each_post.title
            post_dict['content'] = each_post.content
            post_dict['posted_at'] = each_post.posted_at
            author = ndb.Key(Intern, each_post.posted_by.id()).get().username
            post_dict['posted_by'] = author
            post_dict['author_id'] = each_post.posted_by.id()
            post_list.append(post_dict)
    return render_template('home.html', posts=post_list)


# For Mentor - Home page
@app.route('/home-mentor')
@login_required
def mentor_home():
    if current_user.get_user_type() == 'Mentor':
        post_list = []
        with client.context():
            posts = Post.query().order(-Post.posted_at).fetch()
            for each_post in posts:
                post_dict = dict()
                post_dict['post_id'] = each_post.key.id()
                post_dict['title'] = each_post.title
                post_dict['content'] = each_post.content
                post_dict['posted_at'] = each_post.posted_at
                author = ndb.Key(Intern, each_post.posted_by.id()).get().username
                post_dict['posted_by'] = author
                post_dict['author_id'] = each_post.posted_by.id()
                post_list.append(post_dict)
        return render_template('mentor-home.html', title="Mentor-Home", posts=post_list)
    else:
        logout_user()
        flash(f'Access denied !! You are logged out, Please access using authorised credentials', 'danger')
        return render_template('home.html')


# For Admin - Home page
@app.route('/home-admin', methods=['GET', 'POST'])
@login_required
def admin_home():
    if current_user.get_user_type() == 'Admin':
        post_list = []
        with client.context():
            posts = Post.query().order(-Post.posted_at).fetch()
            for each_post in posts:
                post_dict = dict()
                post_dict['post_id'] = each_post.key.id()
                post_dict['title'] = each_post.title
                post_dict['content'] = each_post.content
                post_dict['posted_at'] = each_post.posted_at
                author = ndb.Key(Intern, each_post.posted_by.id()).get().username
                post_dict['posted_by'] = author
                post_dict['author_id'] = each_post.posted_by.id()
                post_list.append(post_dict)
        return render_template('admin-home.html', title="Admin-Home", posts=post_list)
    else:
        logout_user()
        flash(f'Access denied !! You are logged out, Please access using authorised credentials', 'danger')
        return render_template('home.html')


# FIX IT    FIX IT  FIX IT      FIX IT      FIX IT      FIX IT
@app.route('/about')
def about():
    return render_template('about.html', title="About")


# For Admin
# Existing Admin can create another admin account
@app.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    if current_user.is_authenticated and current_user.get_user_type() == "Admin":
        sign_up_form = RegistrationForm()
        if sign_up_form.validate_on_submit():
            with client.context():
                admin_data_for_username = Admin.query().filter(Admin.username == sign_up_form.username.data).fetch()
                if len(admin_data_for_username) == 0:
                    admin_data_for_email = Admin.query().filter(Admin.email == sign_up_form.email.data).fetch()
                    if len(admin_data_for_email) == 0:
                        hashed_password = bcrypt.generate_password_hash(sign_up_form.password.data).decode('utf-8')
                        admin = Admin(username=sign_up_form.username.data, email=sign_up_form.email.data,
                                      password=sign_up_form.password.data)
                        new_admin = admin.put()
                        created_admin = Admin.query().filter(Admin.key == new_admin).get()
                        flash(f"{created_admin} Account created successfully", 'success')
                        return redirect(url_for('admin_home'))
                    else:
                        flash("Admin Account already exists with Email, Please choose another", 'danger')
                    return redirect(url_for('register'))
                else:
                    flash("Admin Account already exists with Username, Please choose another", 'danger')
                    return redirect(url_for('register'))
        return render_template('signup.html', title="Sign Up", form=sign_up_form)
    else:
        logout_user()
        flash(f'Access denied !! You are logged out, Please access using authorised credentials', 'danger')
        return render_template('home.html')


# For intern, mentor, admin
# login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    login_form = LoginForm()
    if login_form.validate_on_submit():
        is_not_intern = request.form.get('notIntern')
        if is_not_intern == 'M':
            with client.context():
                mentor = Mentor.query().filter(Mentor.email == login_form.email.data).get()
            if mentor and bcrypt.check_password_hash(mentor.password, login_form.password.data):
                login_user(mentor, remember=login_form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('mentor_home'))
            else:
                flash(f" :( Login failed! Please check details you entered", 'danger')
        elif is_not_intern == 'A':
            with client.context():
                admin = Admin.query().filter(Admin.email == login_form.email.data).get()
            if admin and (admin.password == login_form.password.data):
                login_user(admin, remember=login_form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('admin_home'))
            else:
                flash(f" :( Login failed! Please check details you entered", 'danger')
        else:
            with client.context():
                intern = Intern.query().filter(Intern.email == login_form.email.data).get()
            if intern and bcrypt.check_password_hash(intern.password, login_form.password.data):
                login_user(intern, remember=login_form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('home'))
            else:
                flash(f" :(  Login failed! Please check details you entered", 'danger')
    return render_template('login.html', title="Login", form=login_form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


# For Admin
# Act as per Admin choice
@app.route('/admin-choice', methods=['GET', 'POST'])
@login_required
def do_admin_choice():
    if current_user.get_user_type() == 'Admin':
        admin_choice = request.form.get('admin-choice')
        if admin_choice == 'createIntern':
            return redirect(url_for('create_intern'))
        elif admin_choice == 'createMentor':
            return redirect(url_for('create_mentor'))
        elif admin_choice == 'updateIntern':
            return redirect(url_for('update_intern'))
        # elif admin_choice == 'tasksByMentor':
        #    return redirect(url_for('display_tasks_by_mentor'))
        elif admin_choice == 'displayMap':
            return redirect(url_for('display_map'))
        elif admin_choice == 'displayTasks':
            return redirect(url_for('display_tasks'))
        else:
            return redirect(url_for('admin_home'))
    else:
        logout_user()
        flash(f'Access denied !! You are logged out, Please access using authorised credentials', 'danger')
        return render_template('home.html')


# For Admin
# create intern account
@app.route('/create/intern', methods=['GET', 'POST'])
@login_required
def create_intern():
    if current_user.get_user_type() == 'Admin':
        with client.context():
            current_mentor_list = Mentor.query().fetch()
        if request.method == 'POST':
            intern_username = request.form.get('username')
            intern_email = request.form.get('email')
            intern_hashed_password = bcrypt.generate_password_hash(request.form.get('password')).decode('utf-8')
            mentor = request.form.get('mentor')

            raw_list = mentor.split("'")
            requested_mentor_email = [item for item in raw_list if "@gmail.com" in item]
            requested_mentor_email = requested_mentor_email[0]
            with client.context():
                requested_mentor = Mentor.query().filter(Mentor.email == requested_mentor_email).get()
                requested_mentor_key = requested_mentor.key
                # print(requested_mentor.key)
                intern_data_for_username = Intern.query().filter(Intern.username == intern_username).fetch()
                if len(intern_data_for_username) == 0:
                    intern_data_for_email = Intern.query().filter(Intern.email == intern_email).fetch()
                    if len(intern_data_for_email) == 0:
                        intern = Intern(username=intern_username, email=intern_email, password=intern_hashed_password,
                                        mentors=[requested_mentor_key])
                        new_intern = intern.put()
                        created_intern = Intern.query().filter(Intern.key == new_intern).get()
                        # print(created_intern)
                        requested_mentor.interns.append(new_intern)
                        requested_mentor.put()
                        flash(f'{created_intern} Account created and assigned to {requested_mentor}', 'success')
                    else:
                        flash("Intern Account already exists with Email, Please choose another", 'danger')
                        return render_template('create-intern.html', mentors=current_mentor_list)
                else:
                    flash("Intern Account already exists with Username, Please choose another", 'danger')
                    return render_template('create-intern.html', mentors=current_mentor_list)
            return render_template('create-intern.html', mentors=current_mentor_list)
        else:
            return render_template('create-intern.html', mentors=current_mentor_list)
    else:
        logout_user()
        flash(f'Access denied !! You are logged out, Please access using authorised credentials', 'danger')
        return render_template('home.html')


# For Admin
# create mentor account
@app.route('/create/mentor', methods=['GET', 'POST'])
@login_required
def create_mentor():
    if current_user.get_user_type() == 'Admin':
        if request.method == 'POST':
            mentor_username = request.form.get('username')
            mentor_email = request.form.get('email')
            mentor_hashed_password = bcrypt.generate_password_hash(request.form.get('password')).decode('utf-8')
            with client.context():
                mentor_data_for_username = Mentor.query().filter(Mentor.username == mentor_username).fetch()
                if len(mentor_data_for_username) == 0:
                    mentor_data_for_email = Mentor.query().filter(Mentor.email == mentor_email).fetch()
                    if len(mentor_data_for_email) == 0:
                        mentor = Mentor(username=mentor_username, email=mentor_email, password=mentor_hashed_password)
                        new_mentor = mentor.put()
                        created_mentor = Mentor.query().filter(Mentor.key == new_mentor).get()
                        flash(f"{created_mentor} Account created successfully", 'success')
                    else:
                        flash("Mentor Account already exists with Email, Please choose another", 'danger')
                    return render_template('create-mentor.html')
                else:
                    flash("Mentor Account already exists with Username, Please choose another", 'danger')
                    return render_template('create-mentor.html')
        else:
            return render_template('create-mentor.html')
    else:
        logout_user()
        flash(f'Access denied !! You are logged out, Please access using authorised credentials', 'danger')
        return render_template('home.html')


# FIX IT        FIX IT      FIX IT      FIX IT      FIX IT      FIX IT
@app.route('/update/intern', methods=['GET', 'POST'])
@login_required
def update_intern():
    return render_template('update-intern.html')


# 8888888888888888888888888888888888888888888888888888888888888888888888888 FOR JS BASED CODE
@app.route('/interns-mentors', methods=['GET'])
@login_required
def get_interns_and_mentors():
    with client.context():
        interns = Intern.query().fetch()
        interns_dict = dict()
        for i in range(len(interns)):
            interns_dict[i] = str(interns[i])
        mentors = Mentor.query().fetch()
        mentors_dict = dict()
        for j in range(len(mentors)):
            mentors_dict[j] = str(mentors[j])
        result_dict = {"interns_dict": interns_dict, "mentors_dict": mentors_dict}
    return result_dict


#<<<<<<<<<<<<<<< FIX IT >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# For Admin
# Add Mentor to Intern
@app.route('/add-mentor', methods=['POST'])
@login_required
def add_mentor():
    admin_data = request.get_json()
    requested_intern = admin_data.get('intern')
    requested_mentor = admin_data.get('mentor')
    print(requested_mentor)
    print(requested_intern)
    if requested_intern == "Select Intern" or requested_mentor == "Select Mentor":
       flash('Please Enter all values', 'info')
       return flask.Response(status=404,);
    return f'{requested_intern} assigned to {requested_mentor} successfully'


# For Mentor
# display tasks assigned by mentor to interns - personalized
@app.route('/tasks-assigned/by-mentor', methods=['GET', 'POST'])
@login_required
def display_tasks_by_mentor():
    if current_user.get_user_type() == 'Mentor':
        with client.context():
            current_mentor = current_user
            interns_of_current_mentor = current_mentor.interns
            if interns_of_current_mentor:
                available_interns = []
                for each_intern in interns_of_current_mentor:
                    intern = Intern.query().filter(Intern.key == each_intern).get()
                    available_interns.append(intern)
            else:
                available_interns = []
        if request.method == 'POST':
            if len(available_interns) == 0:
                flash(f'No Interns mapped to you yet, Please contact Admin', 'danger')
                return render_template('mentor-home.html')
            selected_intern = request.form.get('intern')
            if selected_intern == "Select Intern":
                flash('Please select Intern', 'info')
                return render_template('tasks-by-mentor.html', interns=available_interns)
            else:
                raw_list = selected_intern.split("'")
                requested_intern_email = [item for item in raw_list if "@gmail.com" in item]
                requested_intern_email = requested_intern_email[0]

                with client.context():
                    requested_intern = Intern.query().filter(Intern.email == requested_intern_email).get()
                    requested_intern_key = requested_intern.key
                    requested_tasks = Task.query().filter(Task.assigned_to == requested_intern_key).fetch()
                    # print(requested_tasks)
                    if len(requested_tasks) == 0:
                        flash(f'Currently No tasks are assigned to {requested_intern}', 'info')
                        return render_template('tasks-by-mentor.html', interns=available_interns)
                    else:
                        task_dict_keys = ['Assigned By', 'Assigned To', 'Title', 'Assigned At', 'Content']
                        required_tasks_data = []
                        required_tasks_count = 0
                        required_tasks = [required_tasks_count, required_tasks_data]
                        for each_task in requested_tasks:
                            required_tasks_count += 1
                            each_task_id = each_task.key.id()
                            each_task_details = Task.get_by_id(each_task_id)

                            task_dict = dict.fromkeys(task_dict_keys)
                            each_task_assigned_by = Mentor.query().filter(Mentor.key == each_task_details.assigned_by).get()
                            task_dict['Assigned By'] = each_task_assigned_by
                            each_task_assigned_to = Intern.query().filter(Intern.key == each_task_details.assigned_to).get()
                            task_dict['Assigned To'] = each_task_assigned_to
                            task_dict['Title'] = each_task_details.title
                            task_dict['Assigned At'] = each_task_details.posted_at
                            task_dict['Content'] = each_task_details.content
                            task_dict['task_id'] = each_task_id
                            required_tasks_data.append(task_dict)
                        flash(f'Total {required_tasks_count} tasks were assigned to {requested_intern}', 'info')
                        return render_template('tasks-by-mentor.html', interns=available_interns, tasks=required_tasks, colNames=task_dict_keys)
        else:
            if len(available_interns) == 0:
                flash(f'No Interns mapped to you yet, Please contact Admin', 'danger')
                return render_template('mentor-home.html')
            return render_template('tasks-by-mentor.html', interns=available_interns)
    else:
        logout_user()
        flash(f'Access denied !! You are logged out, Please access using authorised credentials', 'danger')
        return render_template('home.html')


# For Mentor
# display posts by interns for mentor under his mentorship
@app.route('/mentor/posts/by-intern', methods=['GET', 'POST'])
@login_required
def display_posts_by_intern():
    if current_user.get_user_type() == 'Mentor':
        with client.context():
            current_mentor = current_user
            interns_of_current_mentor = current_mentor.interns
            if interns_of_current_mentor:
                available_interns = []
                for each_intern in interns_of_current_mentor:
                    intern = Intern.query().filter(Intern.key == each_intern).get()
                    available_interns.append(intern)
            else:
                available_interns = []
        if request.method == 'POST':
            if len(available_interns) == 0:
                flash(f'No Interns mapped to you yet, Please contact Admin', 'danger')
                return render_template('mentor-home.html')
            selected_intern = request.form.get('intern')
            if selected_intern == "Select Intern":
                flash('Please select Intern', 'info')
                return render_template('view-posts.html', interns=available_interns)
            else:
                raw_list = selected_intern.split("'")
                requested_intern_email = [item for item in raw_list if "@gmail.com" in item]
                requested_intern_email = requested_intern_email[0]

                with client.context():
                    requested_intern = Intern.query().filter(Intern.email == requested_intern_email).get()
                    requested_intern_key = requested_intern.key
                    requested_posts = Post.query().filter(Post.posted_by == requested_intern_key).fetch()
                    if len(requested_posts) == 0:
                        flash(f'Currently No posts are posted by {requested_intern}', 'info')
                        return render_template('view-posts.html', interns=available_interns)
                    else:
                        post_list = []
                        for each_post in requested_posts:
                            post_dict = dict()
                            post_dict['post_id'] = each_post.key.id()
                            post_dict['title'] = each_post.title
                            post_dict['content'] = each_post.content
                            post_dict['posted_at'] = each_post.posted_at
                            author = ndb.Key(Intern, each_post.posted_by.id()).get().username
                            post_dict['posted_by'] = author
                            post_dict['author_id'] = each_post.posted_by.id()
                            post_list.append(post_dict)
                        flash(f'{len(post_list)} posts by {requested_intern}', 'info')
                        return render_template('view-posts.html', posts=post_list)
        else:
            if len(available_interns) == 0:
                flash(f'No Interns mapped to you yet, Please contact Admin', 'danger')
                return render_template('mentor-home.html')
            return render_template('view-posts.html', title='My Intern Posts', interns=available_interns)
    else:
        logout_user()
        flash(f'Access denied !! You are logged out, Please access using authorised credentials', 'danger')
        return render_template('home.html')


# FIX IT        FIX IT              FIX IT              FIX IT              FIX IT
@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    update_form = UpdateAccountForm()
    if update_form.validate_on_submit():
        with client.context():
            intern = Intern.query().filter(Intern.username == current_user.username).get()
            intern.username = update_form.username.data
            intern.email = update_form.email.data
            intern.put()
        flash('Account details updated successfully', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        update_form.username.data = current_user.username
        update_form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', titile='Account', image_file=image_file, form=update_form)


# For Admin
# display-personalized-tasks-of-Intern-Mentor for Admin
@app.route("/tasks", methods=['GET', 'POST'])
@login_required
def display_tasks():
    if current_user.get_user_type() == "Admin":
        with client.context():
            current_interns_list = Intern.query().order(Intern.username).fetch()
            current_mentors_list = Mentor.query().order(Mentor.username).fetch()
        if request.method == 'POST':
            mentor = request.form.get('mentor')
            intern = request.form.get('intern')
            if intern == "Select Intern" or mentor == "Select Mentor":
                flash('Please choose Intern and Mentor to view Tasks', "info")
                return render_template('display-tasks.html', mentors=current_mentors_list, interns=current_interns_list)
            # Do write a function for this  *****************SCOPE FOR IMPROVEMENT
            raw_list = mentor.split("'")
            requested_mentor_email = [item for item in raw_list if "@gmail.com" in item]
            requested_mentor_email = requested_mentor_email[0]
            raw_list = intern.split("'")
            requested_intern_email = [item for item in raw_list if "@gmail.com" in item]
            requested_intern_email = requested_intern_email[0]
            with client.context():
                requested_mentor = Mentor.query().filter(Mentor.email == requested_mentor_email).get()
                requested_mentor_key = requested_mentor.key
                requested_intern = Intern.query().filter(Intern.email == requested_intern_email).get()
                requested_intern_key = requested_intern.key
                # print(requested_intern)
                # print(requested_intern_key)
                # print(requested_mentor.interns)
                if requested_intern_key not in requested_mentor.interns:
                    flash(f'Incorrect selection !!! {requested_mentor} does not mentors {requested_intern}', 'danger')
                    return render_template('display-tasks.html', mentors=current_mentors_list,
                                           interns=current_interns_list)
                requested_tasks = Task.query(ndb.AND(Task.assigned_by == requested_mentor_key, Task.assigned_to == requested_intern_key)).fetch()
                # print(requested_tasks)
                if len(requested_tasks) == 0:
                    flash('Currently No tasks to display', 'info')
                    return render_template('display-tasks.html', mentors=current_mentors_list,
                                           interns=current_interns_list)
                else:
                    task_dict_keys = ['Assigned By', 'Assigned To', 'Title', 'Assigned At', 'Content']
                    required_tasks_data = []
                    required_tasks_count = 0
                    required_tasks = [required_tasks_count, required_tasks_data]
                    for each_task in requested_tasks:
                        required_tasks_count += 1
                        each_task_id = each_task.key.id()
                        each_task_details = Task.get_by_id(each_task_id)

                        task_dict = dict.fromkeys(task_dict_keys)
                        each_task_assigned_by = Mentor.query().filter(Mentor.key == each_task_details.assigned_by).get()
                        task_dict['Assigned By'] = each_task_assigned_by
                        each_task_assigned_to = Intern.query().filter(Intern.key == each_task_details.assigned_to).get()
                        task_dict['Assigned To'] = each_task_assigned_to
                        task_dict['Title'] = each_task_details.title
                        task_dict['Assigned At'] = each_task_details.posted_at
                        task_dict['Content'] = each_task_details.content
                        required_tasks_data.append(task_dict)
                    flash(f'Total {required_tasks_count} tasks were assigned by {requested_mentor} to {requested_intern}', 'info')

            return render_template('display-tasks.html', mentors=current_mentors_list,
                                   interns=current_interns_list, tasks=required_tasks, colNames=task_dict_keys)
        else:
            return render_template('display-tasks.html', mentors=current_mentors_list, interns=current_interns_list)
    else:
        logout_user()
        flash(f'Access denied !! You are logged out, Please access using authorised credentials', 'danger')
        return render_template('home.html')


# For Admin
# display intern and mentor mapping for Admin
@app.route("/map", methods=['GET', 'POST'])
@login_required
def display_map():
    if current_user.get_user_type() == "Admin":
        if request.method == 'POST':
            display_mode = request.form.get('mode')
            if display_mode == "Select Mode":
                flash('Please select Mode', "info")
                return render_template('map.html')
            elif display_mode == "Intern":
                with client.context():
                    interns = Intern.query().fetch()
                    mapped_count = 0
                    mapped_dict = dict()
                    for intern in interns:
                        mapped_count += 1
                        if intern.mentors:
                            mentor_list = []
                            for mentor_key in intern.mentors:
                                mentor_id = mentor_key.id()
                                mentor = Mentor.get_by_id(mentor_id)
                                mentor_list.append(mentor)
                            mapped_dict[str(intern)] = mentor_list
                        else:
                            mapped_dict[str(intern)] = ["Mentor Not Assigned"]
                    mapped_interns = list(mapped_dict.keys())
                    mapped_mentors = list(mapped_dict.values())
                flash(f'Total {mapped_count} Interns Exist', 'info')
                return render_template('map.html', interns=mapped_interns, mentors=mapped_mentors, count=mapped_count,
                                       mode="Intern")
            elif display_mode == "Mentor":
                with client.context():
                    mentors = Mentor.query().fetch()
                    mapped_count = 0
                    mapped_dict = dict()
                    for mentor in mentors:
                        mapped_count += 1
                        if mentor.interns:
                            intern_list = []
                            for intern_key in mentor.interns:
                                intern_id = intern_key.id()
                                intern = Intern.get_by_id(intern_id)
                                intern_list.append(intern)
                            mapped_dict[str(mentor)] = intern_list
                        else:
                            mapped_dict[str(mentor)] = ["Intern Not Assigned"]
                    mapped_interns = list(mapped_dict.values())
                    mapped_mentors = list(mapped_dict.keys())
                flash(f'Total {mapped_count} Mentors Exist', 'info')
                return render_template('map.html', interns=mapped_interns, mentors=mapped_mentors, count=mapped_count,
                                       mode="Mentor")
            else:
                return render_template('map.html')
        else:
            return render_template('map.html')
    else:
        logout_user()
        flash(f'Access denied !! You are logged out, Please access using authorised credentials', 'danger')
        return render_template('home.html')


# For Mentor
# do as per mentor choice
@app.route("/mentor-choice", methods=['GET', 'POST'])
@login_required
def do_mentor_choice():
    if current_user.get_user_type() == "Mentor":
        mentor_choice = request.form.get('mentor-choice')
        if mentor_choice == 'assignTask':
            return redirect(url_for('new_task'))
        elif mentor_choice == 'viewInternPosts':
            return redirect(url_for('display_posts_by_intern'))
        elif mentor_choice == 'tasksByMentor':
            return redirect(url_for('display_tasks_by_mentor'))
        else:
            return redirect(url_for('mentor_home'))
    else:
        logout_user()
        flash(f'Access denied !! You are logged out, Please access using authorised credentials', 'danger')
        return render_template('home.html')


# For Mentor
# Assign new task to intern by mentor
@app.route("/")
@app.route("/assign-task", methods=['GET', 'POST'])
@login_required
def new_task():
    if current_user.get_user_type() == "Mentor":
        with client.context():
            current_mentor = current_user
            interns_of_current_mentor = current_mentor.interns
            if interns_of_current_mentor:
                available_interns = []
                for each_intern in interns_of_current_mentor:
                    intern = Intern.query().filter(Intern.key == each_intern).get()
                    available_interns.append(intern)
            else:
                available_interns = []
        if request.method == 'POST':
            if len(available_interns) == 0:
                flash(f'No Interns mapped to you yet, Please contact Admin', 'danger')
                return render_template('mentor-home.html')
            title = request.form.get('title')
            content = request.form.get('content')
            intern = request.form.get('intern')
            if intern == "Select Intern":
                flash(f'Please select intern', 'info')
                return render_template('assign-task.html', title="New Task", interns=available_interns)
            print(intern)
            raw_list = intern.split("'")
            requested_intern_email = [item for item in raw_list if "@gmail.com" in item]
            requested_intern_email = requested_intern_email[0]
            with client.context():
                requested_intern = Intern.query().filter(Intern.email == requested_intern_email).get()
                requested_intern_key = requested_intern.key
                task = Task(title=title, content=content, assigned_by=current_mentor.key, assigned_to=requested_intern_key)
                t = task.put()
            flash(f'Task assigned to {requested_intern} successfully', 'success')
            return render_template('assign-task.html', title="New Task", interns=available_interns)
        else:
            if len(available_interns) == 0:
                flash(f'No Interns mapped to you yet, Please contact Admin', 'danger')
                return render_template('mentor-home.html')
            return render_template('assign-task.html', title="New Task", interns=available_interns)
    else:
        logout_user()
        flash(f'Access denied !! You are logged out, Please access using authorised credentials', 'danger')
        return render_template('home.html')


# For Intern
# creating new post by intern
@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    if current_user.get_user_type() == "Intern":
        post_form = PostForm()
        if post_form.validate_on_submit():
            with client.context():
                current_user_key = current_user.key
                intern_post = Post(title=post_form.title.data, content=post_form.content.data, posted_by=current_user_key)
                intern_post.put()
            flash('You successfully shared your learnings, Keep it up :)', 'success')
            return redirect(url_for('home'))
        return render_template('create_post.html', title="New Post",
                               form=post_form, legend="Share your Learnings")
    else:
        logout_user()
        flash(f'Access denied !! You are logged out, Please access using authorised credentials', 'danger')
        return render_template('home.html')


# For Intern
# Intern can check his tasks
@app.route("/intern/tasks", methods=['GET', 'POST'])
@login_required
def my_tasks():
    if current_user.get_user_type() == "Intern":
        task_list = []
        with client.context():
            current_user_key = current_user.key
            tasks = Task.query().filter(Task.assigned_to == current_user_key).fetch()
            if len(tasks) == 0:
                flash('Currently No tasks are assigned to you', 'info')
                return render_template('home.html')
            for each_task in tasks:
                task_dict = dict()
                task_dict['title'] = each_task.title
                task_dict['content'] = each_task.content
                task_dict['posted_at'] = each_task.posted_at
                author = ndb.Key(Mentor, each_task.assigned_by.id()).get().username
                task_dict['posted_by'] = author
                task_list.append(task_dict)
        return render_template('tasks.html', tasks=task_list)
    else:
        logout_user()
        flash(f'Access denied !! You are logged out, Please access using authorised credentials', 'danger')
        return render_template('home.html')


# For Intern
# intern can check his posts
@app.route("/intern/posts", methods=['GET', 'POST'])
@login_required
def my_posts():
    if current_user.get_user_type() == "Intern":
        post_list = []
        with client.context():
            current_user_key = current_user.key
            current_user_id = current_user_key.id()
            posts = Post.query().filter(Post.posted_by == current_user_key).fetch()
            if len(posts) == 0:
                flash('Start sharing your learnings, Create a Post', 'info')
                return redirect(url_for("new_post"))
            for each_post in posts:
                post_dict = dict()
                # print(each_post.key.id())
                post_dict['post_id'] = each_post.key.id()
                post_dict['title'] = each_post.title
                post_dict['content'] = each_post.content
                post_dict['posted_at'] = each_post.posted_at
                author = ndb.Key(Intern, each_post.posted_by.id()).get().username
                post_dict['posted_by'] = author
                post_dict['author_id'] = each_post.posted_by.id()
                # print(each_post.posted_by.id())
                post_list.append(post_dict)
        flash(f'Your shared your learnings through {len(post_list)} posts', 'info')
        return render_template('home.html', posts=post_list, current_user_id=current_user_id)
    else:
        logout_user()
        flash(f'Access denied !! You are logged out, Please access using authorised credentials', 'danger')
        return render_template('home.html')


# For intern, mentor, admin
# Opens the desired post in new tab
@app.route("/post/<int:post_id>")
@login_required
def post(post_id):
    with client.context():
        requested_post = ndb.Key(Post, post_id).get()
        if requested_post:
            post_dict = dict()
            post_dict['post_id'] = requested_post.key.id()
            post_dict['title'] = requested_post.title
            post_dict['content'] = requested_post.content
            post_dict['posted_at'] = requested_post.posted_at
            author = ndb.Key(Intern, requested_post.posted_by.id()).get().username
            post_dict['posted_by'] = author
        else:
            abort(404)
    return render_template('page.html', title=requested_post.title, item=post_dict)


# For Intern
# Intern can update his post
@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    with client.context():
        requested_post = ndb.Key(Post, post_id).get()
        if requested_post:
            if requested_post.posted_by != current_user.key:
                abort(403)
            form = PostForm()
            if form.validate_on_submit():
                requested_post.title = form.title.data
                requested_post.content = form.content.data
                requested_post.put()
                flash('Your Post is updated successfully', 'success')
                return redirect(url_for('post', post_id=post_id))
            elif request.method == 'GET':
                form.title.data = requested_post.title
                form.content.data = requested_post.content
        else:
            abort(404)
    return render_template('create_post.html', title="Update Post",
                           form=form, legend='Update Post')


# For mentor
# To update assigned task to his interns
@app.route("/task/<int:task_id>/update", methods=['GET', 'POST'])
@login_required
def update_task(task_id):
    with client.context():
        requested_task = Task.get_by_id(task_id)
        if requested_task:
            if requested_task.assigned_by != current_user.key:
                abort(403)
            if request.method == "POST":
                requested_task.title = request.form.get('title')
                requested_task.content = request.form.get('content')
                requested_task.put()
                flash('Task updated successfully', 'success')
                return redirect(url_for('display_tasks_by_mentor'))
            elif request.method == 'GET':
                title = requested_task.title
                content = requested_task.content
        else:
            abort(404)
    return render_template('update-task.html', task_title=title, task_content=content, task_id=task_id)


# For intern
# delete his existing post
@app.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    with client.context():
        requested_post = ndb.Key(Post, post_id).get()
        if requested_post:
            if requested_post.posted_by != current_user.key:
                abort(403)
            ndb.Key(Post, post_id).delete()
            flash('Post deleted successfully', 'success')
        else:
            abort(404)
    return redirect(url_for('home'))


# For mentor
# To delete assigned tasks to his interns
@app.route('/task/<int:task_id>/delete')
def delete_task(task_id):
    with client.context():
        requested_task = ndb.Key(Task, task_id).get()
    if requested_task:
        if requested_task.assigned_by != current_user.key:
            abort(403)
        else:
            with client.context():
                ndb.Key(Task, task_id).delete()
            flash('Task deleted successfully', 'success')
    else:
        abort(404)
    return redirect(url_for('display_tasks_by_mentor'))


# For Intern, Mentor, Admin
# To view all the posts by author upon clicking on name in any post
@app.route('/user/<int:author_id>')
@login_required
def user_posts(author_id):
    with client.context():
        author = ndb.Key(Intern, author_id).get()
        if author:
            requested_author_posts = Post.query().filter(Post.posted_by == author.key).fetch()
            author_posts_list = []
            for each_post in requested_author_posts:
                post_dict = dict()
                post_dict['post_id'] = each_post.key.id()
                post_dict['title'] = each_post.title
                post_dict['content'] = each_post.content
                post_dict['posted_at'] = each_post.posted_at
                author = ndb.Key(Intern, each_post.posted_by.id()).get().username
                post_dict['posted_by'] = author
                post_dict['author_id'] = each_post.posted_by.id()
                author_posts_list.append(post_dict)
        else:
            abort(404)
        total_posts = len(author_posts_list)
    return render_template('user_posts.html', title=f"{author} posts", author=f"{author}", posts=author_posts_list, posts_count=total_posts)

