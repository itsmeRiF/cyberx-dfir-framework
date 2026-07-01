from flask import Blueprint, render_template
from flask_login import login_required

from models.event import Event
from modules.analysis.severity import get_severity

events_bp = Blueprint("events", __name__)


@events_bp.route("/events/<int:case_id>")
@login_required
def view_events(case_id):

    events = Event.query.filter_by(case_id=case_id).all()

    enriched = []

    for e in events:

        enriched.append({
            "event_id": e.event_id,
            "provider": e.provider,
            "level": e.level,
            "message": e.message,
            "severity": get_severity(e.event_id)
        })

    return render_template("events.html", events=enriched, case_id=case_id)