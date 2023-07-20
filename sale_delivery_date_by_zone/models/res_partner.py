# Copyright 2023 Ooops404
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    use_custom_delivery_preferences = fields.Boolean(
        help="If not set, the delivery zone's settings will be used for shipping"
        "instead of the partner's",
    )

    order_delivery_cutoff_preference = fields.Selection(
        compute="_compute_delivery_preferences",
        store=True,
        readonly=False,
    )

    delivery_time_preference = fields.Selection(
        compute="_compute_delivery_preferences",
        store=True,
        readonly=False,
    )
    delivery_time_window_ids = fields.One2many(
        compute="_compute_delivery_preferences",
        store=True,
        readonly=False,
    )
    cutoff_time = fields.Float(
        compute="_compute_delivery_preferences",
        store=True,
        readonly=False,
    )

    @api.depends(
        "use_custom_delivery_preferences",
        "delivery_zone_id.order_delivery_cutoff_preference",
        "delivery_zone_id.delivery_time_preference",
        "delivery_zone_id.delivery_time_window_ids",
        "delivery_zone_id.cutoff_time",
    )
    def _compute_delivery_preferences(self):
        for partner in self:
            if partner.use_custom_delivery_preferences:
                continue
            if not partner.delivery_zone_id:
                partner.write(
                    {
                        "order_delivery_cutoff_preference": False,
                        "delivery_time_preference": "anytime",
                        "delivery_time_window_ids": False,
                        "cutoff_time": False,
                    }
                )
                continue

            zone = partner.delivery_zone_id
            time_windows = [(5, 0, 0)]
            for tw in zone.delivery_time_window_ids:
                time_windows.append(
                    (
                        0,
                        0,
                        {
                            "time_window_start": tw.time_window_start,
                            "time_window_end": tw.time_window_end,
                            "time_window_weekday_ids": tw.time_window_weekday_ids.ids,
                            "tz": partner.tz,
                        },
                    )
                )

            partner.write(
                {
                    "order_delivery_cutoff_preference": zone.order_delivery_cutoff_preference,
                    "delivery_time_preference": zone.delivery_time_preference,
                    "delivery_time_window_ids": time_windows,
                    "cutoff_time": zone.cutoff_time,
                }
            )
