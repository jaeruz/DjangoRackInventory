from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from app1.models import items,itemsOnRack,rack
from django.db.models import F
# Create your views here.
class CF(F):
    ADD = '||'

def home(request):
    return render(request,"index.html")

def login(request):
    if request.method == 'POST':
        uname = request.POST['uname']
        pass1 = request.POST['pass1']

        log = auth.authenticate(username=uname,password=pass1)

        if log is not None:
            auth.login(request, log)
            print("logged in")
            return redirect("/")
        else:
            messages.info(request,'invalid')
            return redirect('login')
    else:
        return render(request,"login.html")

def logout(request):
    auth.logout(request)
    return redirect('/login')

def register(request):
    if request.method == 'POST':
        fname =request.POST['fname']
        lname =request.POST['lname']
        email =request.POST['email']
        uname =request.POST['uname']
        pass1 =request.POST['pass1']
        pass2 =request.POST['pass2']

        try:
            user = User.objects.get(username=uname)
            text = "Username exists"
        except User.DoesNotExist:

            if pass1==pass2:
                user = User.objects.create_user(username=uname, password=pass1, first_name=fname, last_name=lname, is_superuser=False, email=email)
                user.save()
                print('user created')

                return render(request,'login.html')
            else:
                text = "Password not match"
                print('password not match')
        return render(request,'registerUser.html',{'text': text})

    else:
        return render(request,"registerUser.html")

def adminPanel(request):

    return render(request,"adminIndex.html")

def adminRack(request):
    if request.method =='GET':
        rname = None
        occSlot = None
        rname = request.GET['rname']
        occSlot = request.GET['occSlot']

        print(rname)
        print(occSlot)
        if rname == '*':
            print("ala laman")
        else:
            rack.objects.filter(name=rname).update(occSlot=occSlot)
        returnMatch = rack.objects.raw("SELECT * from app1_rack")
        tresh = []
        for i in returnMatch:
            tresh.append(int(i.slots*0.5))
        print(tresh)

    return render(request,"adminRack.html",{'data':zip(returnMatch,tresh)})

def rackAddItem(request):
    if request.method =='GET':

        itemIDnRack = request.GET['itemID']
        print(itemIDnRack)
        itemID = itemIDnRack.split(',')[0]

        nRack = itemIDnRack.split(',')[1]
        slots = itemIDnRack.split(',')[2]
        oc = itemIDnRack.split(',')[3]

        #print(itemID)
        #print(nRack)
        #print(slots)
        #print(oc)

        returnMatch = items.objects.raw("SELECT * from app1_items")
        if int(oc) == 0:

            returnMatch = items.objects.raw("SELECT * from app1_items")
        elif int(oc) < int(slots):

            ior = itemsOnRack.objects.filter(rack=nRack)
            returnMatch = items.objects.raw("SELECT * from app1_items where itemID='"+ior[0].itemID+"'")

        else:

            returnMatch = items.objects.raw("SELECT * from app1_items")
        #items.objects.filter(itemID=itemID).update(quantity=F('quantity')-slots)
        #rack.objects.filter(name=nRack).update(occSlot=F('occSlot')+slots)
        nslots=int(slots)-int(oc)
        #print(nslots)
        if itemID != '*':
            try:

                ior = itemsOnRack.objects.filter(itemID=itemID)
                print("val")
                print(ior[0].rack)

                if ior[0].rack == 'o' or ior[0].rack ==nRack:
                    match = itemsOnRack.objects.filter(itemID=itemID,rack=nRack)
                    print(slots)
                        #rack.objects.filter(name=nRack).update(occSlot=F('occSlot')+slots)
                    q = items.objects.filter(itemID=itemID)
                    x = int(q[0].quantity) - nslots

                    if x < 0:
                        nslots = int(q[0].quantity)
                    ##########condition###############
                    y=rack.objects.filter(name=nRack)
                    if y[0].occSlot == 0:
                        itemsOnRack.objects.filter(itemID=itemID).update(rack='o')
                    #################################

                    items.objects.filter(itemID=itemID).update(quantity=F('quantity')-nslots)
                    if nslots == 0:
                        print("full")

                    else:
                        if not match:
                            itemsOnRack.objects.filter(itemID=itemID).update(rack=nRack)
                        rack.objects.filter(name=nRack).update(occSlot=F('occSlot')+nslots)
                        itemsOnRack.objects.filter(itemID=itemID).update(quantity=F('quantity')+nslots)

                else:
                    print("cant merge with different items")
            except:
                print('error')


        return render(request,"rackAddItem.html",{'data': returnMatch ,'rack':nRack, 'slot':slots,'oc':oc})

def userPanel(request):

    return render(request,"baseUser.html")

def racks(request):
    if request.method =='GET':
        rck = request.GET['rack']
        returnMatch = rack.objects.filter(name=rck)#raw("SELECT * from app1_rack where name='"+rck+"'")

        print(returnMatch[0].slots)
        print(returnMatch[0].occSlot)
        ior = itemsOnRack.objects.filter(rack=rck)
        if ior is None:
            print(ior[0].itemID)
            ret = items.objects.raw("SELECT * from app1_items where itemID='"+ior[0].itemID+"'")
        else:
            ret = []
        return render(request,"rack.html",{'rack': rck,'slot':returnMatch[0].slots,'oc':returnMatch[0].occSlot,'ret':ret})
    return render(request,"rack.html")

def addRack(request):
    if request.method == 'POST':
        rackName = request.POST['rackName']
        slots = request.POST['slots']
        desc = request.POST['desc']

        rck = rack()
        rck.name = rackName
        rck.slots= slots
        rck.occSlot = 0
        rck.description = desc

        rck.save()
        print("rack added")
        returnMatch = rack.objects.raw("SELECT * from app1_rack")
        return render(request,"adminRack.html",{'rck': returnMatch})
    return render(request,"addRack.html")

def inventory(request):
    if request.method =='GET':
        returnMatch = items.objects.raw("SELECT * from app1_items")
    return render(request,"inventory.html",{'data': returnMatch})

def addItem(request):
    if request.method =='GET':
        return render(request,"addItem.html")
    else:
        itemName =request.POST['itemName']
        itemID =request.POST['itemID']
        serialID =request.POST['serialID']
        quantity =request.POST['quantity']
        description =request.POST['description']

        item = items()
        item.name = itemName
        item.itemID= itemID
        item.seralID = serialID
        item.description = description
        item.quantity = quantity
        item.save()
        ior = itemsOnRack()
        ior.itemID = itemID
        ior.quantity = 0
        ior.rack ="o"
        ior.save()

        print("added")
        return redirect(inventory)

    return render(request,"addItem.html")

def editItem(request):

    if request.method == 'GET':
        itemID = request.GET['itemID']
        returnMatch = items.objects.raw("SELECT * from app1_items where itemID='"+itemID+"'")
        print(returnMatch)
    else:
        itemName = request.POST['itemName']
        itemID = request.POST['itemID']
        serialID = request.POST['serialID']
        quantity = request.POST['quantity']
        description = request.POST['description']
        items.objects.filter(itemID=itemID).update(name=itemName)
        items.objects.filter(itemID=itemID).update(seralID=serialID)
        items.objects.filter(itemID=itemID).update(quantity=quantity)
        items.objects.filter(itemID=itemID).update(description=description)
        returnMatch = items.objects.raw("SELECT * from app1_items")

        return render(request,"inventory.html",{'data': returnMatch})

    return render(request,"editItem.html",{'returnMatch' : returnMatch})

def deleteItem(request):
    if request.method == 'POST':
        itemID = request.POST['itemID']
        items.objects.filter(itemID=itemID).delete()
        print("deleteD!")

    returnMatch = items.objects.raw("SELECT * from app1_items")

    return render(request,"inventory.html",{'data': returnMatch})
