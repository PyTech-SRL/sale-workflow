# Copyright 2023 Ooops404
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    use_custom_delivery_preferences = fields.Boolean(
        help="If not set, the delivery zone's settings will be used for shipping"
        "instead of the partner's"
    )

    @api.onchange("partner_shipping_id")
    def _onchange_partner_shipping_id(self):
        super()._onchange_partner_shipping_id()
        if self.partner_shipping_id:
            self.use_custom_delivery_preferences = (
                self.partner_shipping_id.use_custom_delivery_preferences
            )

    @api.depends(
        "partner_shipping_id.use_custom_delivery_preferences",
        "partner_shipping_id.delivery_zone_id.delivery_time_preference",
        "partner_shipping_id.delivery_zone_id.delivery_time_window_ids",
        "partner_shipping_id.delivery_zone_id.delivery_time_window_ids.time_window_start",
        "partner_shipping_id.delivery_zone_id.delivery_time_window_ids.time_window_end",
        "partner_shipping_id.delivery_zone_id.delivery_time_window_ids.time_window_weekday_ids",
        "partner_shipping_id.delivery_zone_id.order_delivery_cutoff_preference",
        "partner_shipping_id.delivery_zone_id.cutoff_time",
    )
    def _compute_expected_date(self):
        """Add dependencies to consider fixed delivery windows"""
        return super()._compute_expected_date()

    def _get_delivery_preferences_source(self):
        """
        Retrieves the correct field for delivery preferences.
        If use_custom_delivery_preferences is False, use the
        Delivery Zone
        """
        self.ensure_one()
        if self.use_custom_delivery_preferences:
            return super()._get_delivery_preferences_source()
        return self.delivery_zone_id
