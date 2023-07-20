# Copyright 2020 Camptocamp SA
# Copyright 2023 Ooops404
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

WORKDAYS = list(range(5))


class PartnerDeliveryZone(models.Model):
    _name = "partner.delivery.zone"
    _inherit = ["partner.delivery.zone", "cutoff.preference.mixin"]

    delivery_time_preference = fields.Selection(
        [
            ("anytime", "Any time"),
            ("time_windows", "Fixed time windows"),
            ("workdays", "Weekdays (Monday to Friday)"),
        ],
        string="Delivery time schedule preference",
        default="anytime",
        required=True,
        help="Define the scheduling preference for delivery orders:\n\n"
        "* Any time: Do not postpone deliveries\n"
        "* Fixed time windows: Postpone deliveries to the next preferred "
        "time window\n"
        "* Weekdays: Postpone deliveries to the next weekday",
    )

    delivery_time_window_ids = fields.One2many(
        "zone.delivery.time.window",
        "delivery_zone_id",
        string="Delivery time windows",
    )

    @api.constrains("delivery_time_preference", "delivery_time_window_ids")
    def _check_delivery_time_preference(self):
        for zone in self:
            if (
                zone.delivery_time_preference == "time_windows"
                and not zone.delivery_time_window_ids
            ):
                raise ValidationError(
                    _(
                        "Please define at least one delivery time window or change"
                        " preference to Any time"
                    )
                )
