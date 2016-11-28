from saylua import app, login_required
from saylua.utils import get_from_request
from saylua.models.user import User
from saylua.models.notification import Notification
from flask import render_template, redirect, g, url_for, flash, request


@app.route('/bank/', methods=['GET', 'POST'])
@login_required
def bank_main():
    return render_template('bank/main.html')


@app.route('/bank/transfer/', methods=['GET', 'POST'])
@login_required
def bank_transfer():
    recipient = get_from_request(request, 'recipient', args_key='to')
    ss = request.form.get('star_shards')
    cc = request.form.get('cloud_coins')
    if request.method == 'POST':

        if not ss:
            ss = 0
        if not cc:
            cc = 0

        try:
            ss = int(ss)
            cc = int(cc)

            if ss < 0 or cc < 0:
                raise ValueError('You cannot send a negative amount of currency. ')
        except:
            flash('You have entered an invalid amount of currency!', 'error')
        else:
            if not ss and not cc:
                flash('You must enter at least one currency to send. ', 'error')
            else:
                recipient_key = User.key_by_username(recipient)
                if recipient_key:
                    try:
                        User.transfer_currency(g.user.key, recipient_key, cc, ss)
                    except User.InvalidCurrencyException:
                        flash('You do not have enough funds to send the amount entered.', 'error')
                    except:
                        flash('Currency transfer failed for an unexpected reason. Try again later.',
                            'error')
                    else:
                        flash('You have successfully sent %d SS and %d CC to %s'
                            % (ss, cc, recipient))
                        # Send a notification to the user who received the currency
                        Notification.send(recipient_key, '%s sent you %d SS and %d CC'
                            % (g.user.display_name, ss, cc), '/bank/')
                        return redirect(url_for('bank_transfer'))
                else:
                    flash('The user you are trying to send money to does not exist!', 'error')

    return render_template('bank/transfer.html', recipient=recipient, ss=ss, cc=cc)
