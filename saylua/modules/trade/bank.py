from saylua import app
from saylua.models.user import User
from saylua.utils import get_from_request
from saylua.utils.form import flash_errors
from saylua.wrappers import login_required
from saylua.modules.messages.models.db import Notification

from flask import render_template, redirect, g, url_for, flash, request
from forms import BankTransferForm, recipient_check


@login_required
def bank_main():
    return render_template('bank/main.html')


@login_required
def bank_transfer():
    form = BankTransferForm(request.form)
    form.recipient.data = get_from_request(request, 'recipient', args_key='to')

    if request.method == 'POST' and form.validate():
        ss = form.star_shards.data or 0
        cc = form.cloud_coins.data or 0

        if not ss and not cc:
            flash('You must enter at least one currency to send. ', 'error')
        else:
            recipient = recipient_check.user
            try:
                User.transfer_currency(g.user.key, recipient.key, cc, ss)
            except User.InvalidCurrencyException:
                flash('You do not have enough funds to send the amount entered.', 'error')
            except:
                flash('Currency transfer failed for an unexpected reason. Try again later.',
                    'error')
            else:
                flash('You have successfully sent %d SS and %d CC to %s'
                    % (ss, cc, recipient.display_name))

                # Send a notification to the user who received the currency
                Notification.send(recipient.key, '%s sent you %d SS and %d CC'
                    % (g.user.display_name, ss, cc), '/bank/')
                return redirect(url_for('bank_transfer'))
    flash_errors(form)
    return render_template('bank/transfer.html', form=form)
