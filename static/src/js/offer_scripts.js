/** @odoo-module **/

odoo.define('food_ordering.offer_clicks', function (require) {
    'use strict';

    const publicWidget = require('web.public.widget');

    publicWidget.registry.OfferClick = publicWidget.Widget.extend({
        selector: '.section-offers',
        start: function () {
            this.$('.offer-card').on('click', function () {
                const offerName = this.dataset.offer;
                alert(`You clicked on ${offerName}`);
            });
            return this._super.apply(this, arguments);
        },
    });
});
