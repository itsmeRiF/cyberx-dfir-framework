import os
from flask import Blueprint, request, redirect, url_for, render_template
from flask_login import login_required
from werkzeug.utils import secure_filename

from models.evidence import Evidence
from database.db import db
#from modules.parser.evtx import run_evtxecmd
from modules.parser.hayabusa import run_hayabusa
from config import Config
from models.event import Event

evidence_bp = Blueprint("evidence", __name__)


@evidence_bp.route("/evidence/<int:case_id>")
@login_required
def evidence_page(case_id):

    return render_template("evidence.html", case_id=case_id)


@evidence_bp.route("/evidence/upload/<int:case_id>", methods=["POST"])
@login_required
def upload_evidence(case_id):

    file = request.files["file"]

    filename = secure_filename(file.filename)

    save_path = os.path.join(Config.UPLOAD_FOLDER, filename)

    file.save(save_path)

    # save evidence record
    evidence = Evidence(
        case_id=case_id,
        filename=filename,
        filepath=save_path
    )

    db.session.add(evidence)
    db.session.commit()

    # run parser
    output_dir = os.path.join(Config.OUTPUT_FOLDER, str(case_id))
    tool_path = os.path.join(Config.TOOL_FOLDER, "hayabusa.exe")

    events = run_hayabusa(save_path, output_dir, Config.TOOL_FOLDER + "/hayabusa.exe")

    event_objects = []

    for e in events:
        event_objects.append(
            Event(
                case_id=case_id,
                timestamp=e["timestamp"],
                computer=e["computer"],
                channel=e["channel"],
                event_id=e["event_id"],
                record_id=e["record_id"],
                rule_title=e["rule_title"],
                rule_id=e["rule_id"],
                severity=e["severity"],
                details=e["details"],
                extra_info=e["extra_info"]
            )
        )

    db.session.bulk_save_objects(event_objects)
    db.session.commit()

    return {
        "message": "Evidence processed",
        "events_count": len(event_objects)
    }