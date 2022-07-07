from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class SchoolStandard(models.Model):
    _name = "school.standard"
    _inherit = "school.standard"
    _rec_name = "event_ids"

    event_ids = fields.Many2many("event.event", "school_event_standard_rel",
        "event_id", "standard_id", "Events",
        help="Select events for the standard")


class EventEvent(models.Model):
    _inherit = "event.event"

    event_type = fields.Selection([("intra", "IntraSchool"),
        ("inter", "InterSchool")], "Event Type",
        help="Event is either IntraSchool or InterSchool")
    # organizer_id = fields.Many2one("hr.employee", string="Supervisor")
    employee_id = fields.Many2one("hr.employee", string="Contact Person",
        help="Contact Person for Eevnt")
    part_standard_ids = fields.Many2many("school.standard",
        "school_event_standard_rel", "standard_id",
        "event_id", "Participant Standards",
        help="The Participant is from which standard")


class EventRegistration(models.Model):
    _inherit = "event.registration"

    part_name_id = fields.Many2one("student.student",
        "Participant Name", required=True,
        help="Select Participant",
    )
    student_standard_id = fields.Many2one(
        "school.standard", "Student Std", help="Enter standard"
    )

    @api.onchange("part_name_id")
    def onchange_student_standard(self):
        """Onchange method for participant"""
        self.student_standard_id = self.part_name_id.standard_id.id

    def action_set_draft(self):
        for rec in self:
            if rec.event_id.stage_id.pipe_end:
                raise ValidationError(_(
"You can not set registration to Draft stage due to event is ended!"))
        return super(EventRegistration, self).action_set_draft()
