import os
from uuid import uuid4

from flask import (
    render_template,
    request,
    redirect,
    flash,
    current_app,
    url_for,
    send_from_directory
)

from flask_login import (
    login_required,
    current_user
)

from sqlalchemy import text
from werkzeug.utils import secure_filename

from app.ai.analyzer import analyze_document

from . import documents_bp
from .utils import allowed_file

from ..extensions import db
from ..models import Document
from .ocr import extract_text

import json
from flask import send_from_directory



@documents_bp.route("/upload", methods=["GET", "POST"])
@login_required
def upload():

    if request.method == "POST":
        print("1. Upload started")
        if "document" not in request.files:

            flash("Select file.", "danger")
            return redirect(request.url)

        file = request.files["document"]

        if file.filename == "":

            flash("Select file.", "danger")
            return redirect(request.url)

        if not file.filename:
            flash("No filename provided.", "danger")
            return redirect(request.url)

        if not allowed_file(file.filename):

            flash("Unsupported file type.", "danger")
            return redirect(request.url)

        original_name = secure_filename(file.filename)

        unique_name = f"{uuid4().hex}_{original_name}"

        upload_path = os.path.join(
            current_app.config["UPLOAD_FOLDER"],
            unique_name
        )

        os.makedirs(
            current_app.config["UPLOAD_FOLDER"],
            exist_ok=True
        )

        file.save(upload_path)
        
        text = extract_text(upload_path)
        
        print("=" * 50)
        print(text)
        print("=" * 50)
        
        print("2. OCR done")
        
        print("2.5 Calling AI...")

        analysis = analyze_document(text)

        print("3. AI done")
        print(analysis)
        ai = analysis
       

        document = Document(
            filename=unique_name,
            original_name=original_name,
            category=analysis["category"],
            file_size=os.path.getsize(upload_path),
            owner_id=current_user.id,
            extracted_text=text,
            is_encrypted=True,
            ai_summary=analysis["summary"],
            ai_category=analysis["category"],
            ai_confidence=analysis["confidence"],
            ai_analysis=json.dumps(analysis, indent=2)
)           
        print("4. Creating document")
            
            

        db.session.add(document)
        print("5. Added")

        db.session.commit()
        print("6. Committed")
        
        flash("Document uploaded successfully.", "success")
        print("7. Redirect")
        return redirect(url_for("dashboard.dashboard"))

    return render_template("dashboard/upload.html")

@documents_bp.route("/download/<int:document_id>")
@login_required
def download(document_id):

    document = Document.query.filter_by(
        id=document_id,
        owner_id=current_user.id
    ).first_or_404()

    return send_from_directory(
        current_app.config["UPLOAD_FOLDER"],
        document.filename,
        as_attachment=True,
        download_name=document.original_name
    )
    
@documents_bp.route("/delete/<int:document_id>")
@login_required
def delete(document_id):
    document = Document.query.filter_by(
        id=document_id,
        owner_id=current_user.id
    ).first_or_404()

    file_path = document.filename

    if file_path and os.path.exists(file_path):
        os.remove(file_path)

    db.session.delete(document)
    db.session.commit()

    flash("Document deleted successfully.", "success")
    return redirect(url_for("dashboard.dashboard"))

@documents_bp.route("/edit/<int:document_id>", methods=["GET", "POST"])
@login_required
def edit(document_id):
    document = Document.query.filter_by(
        id=document_id,
        owner_id=current_user.id
    ).first_or_404()

    if request.method == "POST":
        document.original_name = request.form.get("name")
        document.category = request.form.get("category")

        db.session.commit()

        flash("Document updated successfully.", "success")
        return redirect(url_for("dashboard.dashboard"))

    return render_template(
        "dashboard/edit_document.html",
        document=document
    )
@documents_bp.route("/<int:document_id>")
@login_required
def view(document_id):
    document = Document.query.filter_by(
        id=document_id,
        owner_id=current_user.id
    ).first_or_404()

    return render_template(
        "dashboard/document_detail.html",
        document=document
    )    