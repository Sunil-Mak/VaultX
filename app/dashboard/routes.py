from flask import render_template
from flask_login import login_required, current_user

from . import dashboard_bp
from ..models import Document


@dashboard_bp.route("/")
def index():
    return render_template("index.html")


@dashboard_bp.route("/dashboard")
@login_required
def dashboard():

    documents = (
        Document.query
        .filter_by(owner_id=current_user.id)
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
        stats=stats
    )