model = "gpt-3.5-turbo"
temperature = 0.25

returnOption = '' # No, Paid, Free, empty
refundOption = '' # No, Partial, Full, empty
exchangeOption = '' # No, Paid, Free, empty
deliveryStatus = '' # Not Shipped, Delayed, Shipped, Delviered, Rescheduled
coupon = '' # Yes, empty
couponCode = ''  # can be empty

buyerName = ''  # can be empty
clientName = 'Sarthak'  # Cant be empty
compnayName = 'indiancultura'  # Cant be empty
productTitle = 'Vintage Patchwork Kantha Bedspread Indian Handmade Quilt Throw Cotton Blanket'

promptMessage = 'Yes, you can choose. we will send pictures'
buyerMail = "Hello" \
            "\n" \
            "They all look different...Can i pick which one i like best? Thank you"

wordLength = '150' # cant be empty


apiKey = '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'

mailTypeList = ['Product Enquiry', 'Product Complaint',
                'Order placement', 'Order Detail Request', 'Order Return', 'Order Exchange', 'Order Refund',
                'Order Repair', 'Order Cancellation',
                'Delivery Address Change', 'Delivery Information Change', 'Delivery Status Request', 'Delivery Tracking Request',
                'Enquiry Cancellation Policy', 'Enquiry Refund Policy', 'Enquiry Return Policy', 'Enquiry Exchange Policy','Enquiry Delivery Options']

mailToneList = ['Formal', 'Assertive', 'Persuasive', 'Apologetic', 'Assuring']