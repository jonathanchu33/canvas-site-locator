import os
import re
from flask import Flask, jsonify, render_template, request, redirect
from cs50 import SQL
import canvasapi
import urllib.error
import urllib.request as urlr
from bs4 import BeautifulSoup

db = SQL("sqlite:///courses.db")

# Canvas API URL
API_URL = "https://canvas.harvard.edu"

"""
Canvas API key required for search results to appear. User must generate their
own Canvas token, which can be done from a user's logged-in profile page. Application
functions with Harvard student account Canvas privileges.
https://canvas.instructure.com/doc/api/file.oauth.html#manual-token-generation
https://canvas.harvard.edu/profile/settings
"""
API_KEY = "1875~diJBahkEWtUCX1jte3j7lRCBLxQkpSsbnSss2jAjLpjS8k0NeDvjuUmBtcP6eC1N"

# Initialize a new Canvas object
canvas = canvasapi.Canvas(API_URL, API_KEY)

# Configure application
app = Flask(__name__)

# Returned sites of any given search
sites = []


# Home search page
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        del sites[:]
        locator_id = None

        # Check if query term is empty
        course = request.form.get("course")
        if not course:
            return render_template("invalid.html")

        # Search for course in catalog
        try:
            catalog_website = urlr.urlopen(
                "https://courses.harvard.edu/search?q={0}&sort=course_title+asc&start=0&rows=1000&submit=Search".format(course.replace(" ", "+")))
        except urllib.error.HTTPError:
            return render_template("invalid.html")

        # Parse catalog entries for the correct one
        soup = BeautifulSoup(catalog_website.read(), 'html.parser')
        course_title_tags = soup.find_all('span', class_="course_title")
        for tag in course_title_tags:
            if tag.get_text().lower().find(course.lower()) != -1:
                locator_id = re.search(r'[(](\d+)', tag.get_text()).group(1)
                break

        # Check if queried course number was not found
        if not locator_id:
            return render_template("invalid.html")

        # Parse Harvard course site locator
        canvas_locator_website = urlr.urlopen("https://locator.tlt.harvard.edu/course/colgsas-{0}".format(locator_id))
        soup2 = BeautifulSoup(canvas_locator_website.read(), 'html.parser')
        canvas_entry_tags = soup2.find_all('div', class_="course")

        # Collect available Canvas sites
        for tag in canvas_entry_tags:
            try:
                course_id = int(re.search(r'courses[/](\d+)', tag.a.get('href')).group(1))
                site = canvas.get_course(course_id)
                term = tag.h4.small.get_text()
                sites.append((site, tag.a.get('href'), term, course_id, site.name))
            except (AttributeError, canvasapi.exceptions.Unauthorized):
                pass

        # Check if no Canvas sites are accessible to user
        if not len(sites):
            return render_template("none.html")

        return render_template("results.html", sites=sites)

    else:
        # Render page
        return render_template("index.html")


# Favorite a course
@app.route("/favorite", methods=["POST"])
def favorite():
    button_id = int(request.get_json(True).get("button_id"))

    db.execute("INSERT INTO Favorites (course_id, course_link, course_term, course_title) VALUES (:id, :link, :term, :title)",
               id=sites[button_id][3], link=sites[button_id][1], term=sites[button_id][2], title=sites[button_id][4])

    return jsonify(coursename=sites[button_id][4], courseterm=sites[button_id][2])


# Unfavorite a course
@app.route("/unfavorite", methods=["POST"])
def unfavorite():
    db.execute("DELETE FROM Favorites WHERE course_id = :id", id=int(request.form.get("unfavorite")))

    return redirect("/favorites")


# Favorited courses page
@app.route("/favorites", methods=["GET"])
def favorites():
    favorites = db.execute("SELECT * FROM Favorites")

    return render_template("favorites.html", favorites=favorites)


# Button trigger (search results page): Download all of course's files
@app.route("/download", methods=["POST"])
def download():
    err_files = download_files(sites[int(request.get_json(True).get("button_id"))][0])
    if err_files == -1:
        status = "No root file folder for course."
    else:
        status = "Files downloaded with {} errors.".format(err_files)

    return jsonify(message=status)


# Button trigger (favorites page): Download all of course's files
@app.route("/download-favorites", methods=["POST"])
def download_favorites():
    course_entry = db.execute("SELECT * FROM Favorites WHERE course_id = :id",
                              id=int(request.get_json(True).get("button_id")))

    err_files = download_files(canvas.get_course(int(course_entry[0]["course_id"])))
    if err_files == -1:
        status = "No root file folder for course."
    else:
        status = "Files downloaded with {} errors.".format(err_files)

    return jsonify(message=status)


# Function: download all of course's files
def download_files(course):
    all_folders = course.get_folders()
    root_folder = None
    for folder in all_folders:
        if folder.full_name == "course files":
            root_folder = folder

    # Check if course Canvas site has no root folder
    if not root_folder:
        return -1

    def download_organized(folder, folder_str_name):
        errors = 0
        subfolders = folder.get_folders()
        subfiles = folder.get_files()

        for subfile in subfiles:
            try:
                subfile.download("./" + folder_str_name + "/" + subfile.display_name)
            except FileNotFoundError:
                errors += 1

        for subfolder in subfolders:
            os.system("cd '" + folder_str_name + "' && mkdir '" + subfolder.name.replace("'", "") + "'")
            errors += download_organized(subfolder, folder_str_name + "/" + subfolder.name.replace("'", ""))

        return errors

    os.system("mkdir " + str(course.id) + "_files")
    return download_organized(root_folder, str(course.id) + "_files")


    """
    all_files = course.get_files()
    os.system("mkdir " + str(course.id) + "_files")
    for file in all_files:
        file.download("./" + str(course.id) + "_files/" + file.filename)
    """

