document.addEventListener('DOMContentLoaded', function() {
    var stripe = Stripe(stripePublishableKey);
    var elements = stripe.elements();
    var cardElement = elements.create('card');
    cardElement.mount('#card-element');
    var buyButton = document.getElementById('buy-button');
    var message = document.getElementById('message');

    buyButton.addEventListener('click', function() {
        // Disable the button
        buyButton.disabled = true;
        fetch('/buy/order/' + orderId, {method: 'GET'})
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(function(data) {
            return stripe.confirmCardPayment(data.client_secret, {
                payment_method: {
                    card: cardElement,
                    billing_details: {
                        name: 'Your Customer Name',
                    },
                }
            });
        })
        .then(function(result) {
            if (result.error) {
                // Show error to your customer
                console.log(result.error.message);
                message.textContent = 'Payment failed: ' + result.error.message;
                // Enable the button
                buyButton.disabled = false;
            } else {
                if (result.paymentIntent.status === 'succeeded') {
                    // The payment has been processed!
                    console.log('Payment succeeded!');
                    message.textContent = 'Payment succeeded!';
                }
            }
        });
    });
});
