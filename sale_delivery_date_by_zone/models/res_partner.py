# Copyright 2023 Ooops404
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    use_custom_delivery_preferences = fields.Boolean(
        help="If not set, the delivery zone's settings will be used for shipping"
        "instead of the partner's",
    )
