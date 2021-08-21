from django.shortcuts import render
from django.views.generic import TemplateView
from mainapp.models import Customer, Transaction
from django.db import connection

# Create your views here.

class IndexView(TemplateView):
    template_name = 'index.html'

def customerView(request):
    data = Customer.objects.raw('SELECT * FROM public.mainapp_customer ORDER BY acc_number ASC')
    mydict = {'customers':data}
    return render(request, 'customer.html', context=mydict)

def transactionView(request):
    data = Transaction.objects.raw('SELECT * FROM public.mainapp_transaction ORDER BY time DESC')
    mydict = {'transactions':data}
    return render(request, 'transactions.html', context=mydict)

def transferView(request):

    if request.method == 'POST':
        acc_number_1 = request.POST['acc_number_1']
        acc_number_2 = request.POST['acc_number_2']

        data_one = Customer.objects.filter(acc_number=acc_number_1)
        data_two = Customer.objects.filter(acc_number=acc_number_2)

        if data_one and data_two:
            request.session['acc_number_1'] = acc_number_1
            request.session['acc_number_2'] = acc_number_2

            s_data = Customer.objects.raw('SELECT * FROM public.mainapp_customer WHERE acc_number={}'.format(acc_number_1))
            r_data = Customer.objects.raw('SELECT * FROM public.mainapp_customer WHERE acc_number={}'.format(acc_number_2))

            my_dict = {'s_data':s_data, 'r_data':r_data}

            return render(request, 'confirm_transfer.html', context=my_dict)

        else:
            if not data_one:
                message = 'Invalid Sender A/C Number, Please Check'
            else:
                message = 'Invalid Receiver A/C Number, Please Check'

            my_msg_dict = {'message':message}
            return render(request, 'transfer.html', context=my_msg_dict)

    return render(request, 'transfer.html')


def confirmTransferView(request):
    acc_number_1 = request.session['acc_number_1']
    acc_number_2 = request.session['acc_number_2']

    data1 = Customer.objects.filter(acc_number=acc_number_1).values()

    print(data1)

    sender_bal = int(data1[0]['balance'])

    if request.method == 'POST':

        amount = int(request.POST['amount'])

        if amount > sender_bal:
            message = 'Insufficient Balance'
            
            my_error_dict = {'message':message}
            return render(request, 'transfer.html', context=my_error_dict)
        else:
            with connection.cursor() as c:
                c.execute('CALL public.stored_procedure({},{},{})'.format(acc_number_1,acc_number_2,amount))
            message = 'Transaction Successful'

            my_success_dict = {'message':message}
            return render(request, 'index.html', context=my_success_dict)
    return render(request, 'confirm_transfer.html')
