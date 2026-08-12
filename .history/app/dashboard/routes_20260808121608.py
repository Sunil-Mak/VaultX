from flask import render_template, request
from flask_login import current_user, login_required

from ..models import Document
from . import dashboard_bp


@dashboard_bp.route("/")
def index():
    return render_template("index.html")


@dashboard_bp.route("/dashboard")
@login_required
def dashboard():

    query = request.args.get("q", "").strip()

    documents_query = (
        Document.query
        .filter_by(owner_id=current_user.id)
    )

    if query:
        documents_query = documents_query.filter(
            db.or_(
                Document.original_name.ilike(f"%{query}%"),
                Document.extracted_text.ilike(f"%{query}%"),
                Document.ai_summary.ilike(f"%{query}%")
            )
        )

    documents = (
        documents_query
        .order_by(Document.uploaded_at.desc())
        .all()
    )

    stats = {
        "documents": len(documents),
        "shared": 0,
        "encrypted": len([d for d in documents if d.is_encrypted]),
        "storage": sum(d.file_size or 0 for d in documents)
    }

    return render_template(
        "dashboard/dashboard.html",
        documents=documents,
        stats=stats,
        query=query
    )