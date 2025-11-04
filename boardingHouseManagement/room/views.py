from django.forms import ValidationError
from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.db.models import Sum
from .forms import *
from datetime import datetime
from django.contrib.humanize.templatetags.humanize import intcomma
# Create your views here.


#Room
def create_room(request):
    room = Room.objects.all().order_by('id')
    house = House.objects.all()
    form = AddRoom()
    if request.method == 'POST':
        form = AddRoom(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_room')
    return render(request, 'rooms/list_room.html', {'Room': room, 'House': house, 'new_room': form})


def edit_room(request, id):
    house = House.objects.all()
    room = get_object_or_404(Room, id=id)
    form = UpdateInformationRoom(instance=room)
    if request.method == 'POST':
        form = UpdateInformationRoom(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('list_room')
    return render(request, 'rooms/edit_room.html', {'update_room': form, 'inf_room': room, 'House': house})

def delete_room(request, id):
    room = get_object_or_404(Room, id=id)
    form = DeleteRoomForm(instance=room)
    if request.method == 'POST':
        form = DeleteRoomForm(request.POST, instance=room)
        if form.is_valid():
            form.deleteRoom(id)
            return redirect('list_room')
    return render(request, 'rooms/delete_room.html', {'delete_room': form ,'inf_room': room})

def search_roomsNumber(request):
    form = SearchRoom()
    if request.method == 'POST':
        form = SearchRoom(request.POST)
        if form.is_valid():
            roomsNumber = form.cleaned_data['roomsNumber']
            room = Room.objects.filter(roomsNumber=roomsNumber)
    return render(request, 'rooms/search_room.html', {'search_room': form, 'search_roomsNumber': room})


#House
def create_house(request):
    form = AddHouse()
    if request.method == 'POST':
        form = AddHouse(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_house')
    return render(request, 'rooms/list_house.html', {'new_house': form, 'House': House.objects.all().order_by('id'), 'Personnel': Personnel.objects.all(), 'Area': Area.objects.all()})


def get_rooms(request, id):
    house = House.objects.get(id=id)
    room = Room.objects.filter(house=house)
    return render(request, 'rooms/list_room_of_house.html', {'inf_house': house, 'room_of_house': room})


def edit_house(request, id):
    area = Area.objects.all()
    personnel = Personnel.objects.all()
    house = get_object_or_404(House, id=id)
    form = UpdateInformationHouse(instance=house)
    if request.method == 'POST':
        form = UpdateInformationHouse(request.POST, instance=house)
        if form.is_valid():
            form.save()
            return redirect('list_house')
    return render(request, 'rooms/edit_house.html', {'update_house': form, 'inf_house': house, 'Area': area, 'Personnel': personnel})

def delete_house(request, id):
    house = get_object_or_404(House, id=id)
    form = DeleteHouseForm(instance=house)
    if request.method == 'POST':
        form = DeleteHouseForm(request.POST, instance=house)
        if form.is_valid():
            form.deleteHouse(id)
            return redirect('list_house')
    return render(request, 'rooms/delete_house.html', {'delete_house': form, 'inf_house': house})

def search_nameHouse(request):
    form = SearchHouse()
    if request.method == 'POST':
        form = SearchHouse(request.POST)
        if form.is_valid():
            nameHouse = form.cleaned_data['nameHouse']
            house = House.objects.filter(nameHouse__icontains=nameHouse)
    return render(request, 'rooms/search_house.html', {'search_house': form, 'search_nameHouse': house})

#Electricity
def create_electricity(request):
    electricity = Electricity.objects.all().order_by('id')
    form = ElectricityForm()
    if request.method == 'POST':
        form = ElectricityForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_electricity')
    return render(request, 'rooms/list_electricity.html', {'new_electricity': form,'Electricity': electricity, 'House': House.objects.all(), 'Room': Room.objects.all()})

def edit_electricity(request, id):
    electricity = get_object_or_404(Electricity, id=id)
    room = Room.objects.all()
    form = UpdateElectricity(instance=electricity)
    if request.method == 'POST':
        form = UpdateElectricity(request.POST, instance=electricity)
        if form.is_valid():
            form.save()
            return redirect('list_electricity')
    return render(request, 'rooms/edit_electricity.html', {'update_electricity': form, 'inf_electricity': electricity, 'Room': room})

def delete_electricity(request, id):
    electricity = get_object_or_404(Electricity, id=id)
    form = DeleteElectricity(instance=electricity)
    if request.method == 'POST':
        form = DeleteElectricity(request.POST, instance=electricity)
        if form.is_valid():
            form.deleteElectricity(id)
            return redirect('list_electricity')
    return render(request, 'rooms/delete_electricity.html', {'delete_electricity': form, 'inf_electricity': electricity})

def calculate_bill(request, room_id):
    # Lấy 2 bản ghi chỉ số điện gần nhất theo ngày
    readings = Electricity.objects.filter(room_id=room_id).order_by('-date')[:2]

    start_date = None
    end_date = None
    electricity = 0

    # Nếu có đủ 2 bản ghi, thì mới tính được
    if len(readings) == 2:
        new_index = readings[0].index_electricity  # chỉ số mới
        old_index = readings[1].index_electricity  # chỉ số cũ

        end_date = readings[0].date   # ngày mới
        start_date = readings[1].date # ngày cũ

        electricity = (new_index - old_index) * 3500
        if electricity < 0:
            electricity *= -1
    else:
        message = "Chưa có đủ dữ liệu để tính tiền điện."
        room = Room.objects.get(pk=room_id)
        return render(request, 'rooms/calculate_bill.html', {
            'room_house': room.house,
            'room_number': room.roomsNumber,
            'message': message
        })

    # Các phần khác
    room = Room.objects.get(pk=room_id)
    water = room.quantity * 100_000
    wifi = 100_000
    room_price = int(room.price) * 1_000_000
    total_display = intcomma(int(electricity + water + wifi + room_price))

    return render(request, 'rooms/calculate_bill.html', {'room_house': room.house,'room_number': room.roomsNumber,'room_bill': room_price,'electricity_bill': electricity,'water_bill': water,'wifi_bill': wifi,'total_bill': total_display,'start_date': start_date,'end_date': end_date,})

#Guest
def create_guests(request):
    guest = Guests.objects.all().order_by('id')
    room = Room.objects.all()
    form = AddGuestForm()
    if request.method == 'POST':
        form = AddGuestForm(request.POST)
        if form.is_valid():
            try:
                form.clean_room()  # Kiểm tra số lượng khách trong phòng
                form.save()
                return redirect('list_guests')
            except ValidationError as e:
                form.add_error(None, e)  # Thêm lỗi vào form để hiển thị trên template
    
    return render(request, 'rooms/list_guests.html', {'Guests': guest, 'Room':room ,'new_guest': form})

def guests_in_room(request, id):
    room = Room.objects.get(id=id)
    guests = Guests.objects.filter(room=room)
    return render(request, 'rooms/guests_in_room.html', {'room': room, 'guests': guests})


def edit_guest(request, guest_id):
    room = Room.objects.all()                 
    guest = get_object_or_404(Guests, id=guest_id)
    form = UpdateGuestForm(instance=guest)
    if request.method == 'POST':
        form = UpdateGuestForm(request.POST, instance=guest)
        if form.is_valid():
            form.save()
            return redirect('list_guests')
    return render(request, 'rooms/edit_guest.html', {'Room':room,'update_guest': form, 'inf_guest': guest})



def delete_guest(request, guest_id): # gắn hàm delete
    guest = get_object_or_404(Guests, id=guest_id) 
    form = DeleteGuestForm(instance=guest)
    if request.method == 'POST':
        form = DeleteGuestForm(request.POST, instance=guest)
        if form.is_valid():
            form.deleteGuest(guest_id)
            return redirect('list_guests') 
    return render(request, 'rooms/delete_guest.html',{'delete_guest': form,'inf_guest': guest})

def get_guest(request, room_id): 
    # Lấy danh sách các khách hàng đang ở trong phòng
    guests = Guests.objects.filter(room_id=room_id)

    if request.method == 'POST':
        # Xử lý khi người dùng bấm nút trả phòng của một khách hàng cụ thể
        guest_id = request.POST.get('guest_id')
        try:
            guest = Guests.objects.get(id=guest_id)
            # Cập nhật room_id của khách hàng thành Null 
            guest.room_id = None # đặt là None thì room sẽ ko lấy đc room_id của khách nên sẽ ko hiện lại trên room
            guest.save()
        except Guests.DoesNotExist:
            pass  
        return redirect('guest_checkout', room_id = room_id)
    return render(request, 'rooms/list_guest_of_room.html', {'guests':guests,'room_id' : room_id,})

def search_guest(request):
    form = SearchGuestByFullnameForm()
    if request.method == 'POST':
        form = SearchGuestByFullnameForm(request.POST)
        if form.is_valid():
            fullname = form.cleaned_data['fullname'] 
            guest = Guests.objects.filter(fullname__icontains=fullname)
    return render(request, 'rooms/search_guest.html', {'search_guest': form, 'search_fullname': guest})

     

#Personnel
def create_personnel(request):
    personnel = Personnel.objects.all().order_by('id_personnel')
    form = AddPersonnel()
    if request.method == 'POST':
        form = AddPersonnel(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_personnel')
    return render(request, 'rooms/list_personnel.html', {'Personnel': personnel, 'new_personnel': form})

# lay id nhan vien
def id_personel(request):
    username = request.user.username  # ví dụ: NVVIP
    if username.startswith("NV"):
        nv_id = username  # lấy phần sau 'NV' -> 'VIP'
    else:
        nv_id = None

    return render(request, 'pages/list_house_of_personel.html', {'nv_ids': nv_id})

def get_house_of_personnel(request, id_personnel):
    personnel = Personnel.objects.get(id_personnel=id_personnel)
    houses = House.objects.filter(personnel=personnel)
    return render(request, 'rooms/list_house_of_personnel.html', {'inf_personnel': personnel, 'house_of_personnel': houses})

def edit_personnel(request, id_personnel):
    personnel = get_object_or_404(Personnel, id_personnel=id_personnel)
    form = UpdateInformationPersonnel(instance=personnel)
    if request.method == 'POST':
        form = UpdateInformationPersonnel(request.POST, instance=personnel)
        if form.is_valid():
            form.save()
            return redirect('list_personnel')
    return render(request, 'rooms/edit_personnel.html', {'update_personnel': form, 'inf_personnel': personnel})

def delete_personnel(request, id_personnel):
    personnel = get_object_or_404(Personnel, id_personnel=id_personnel)
    form = DeletePersonnel(instance=personnel)
    if request.method == 'POST':
        form = DeletePersonnel(request.POST, instance=personnel)
        if form.is_valid():
            form.deletePersonnel(id_personnel)
            return redirect('list_personnel')
    return render(request, 'rooms/delete_personnel.html', {'delete_personnel': form, 'inf_personnel': personnel})

def search_personnel(request):
    form = SearchPersonnel()
    if request.method == 'POST':
        form = SearchPersonnel(request.POST)
        if form.is_valid():
            lower_str = form.cleaned_data['fullname']
            personnel = Personnel.objects.filter(fullname__icontains=lower_str)
    return render(request, 'rooms/search_personnel.html', {'search_personnel': form, 'search_personnels': personnel})
    
       
#Area
def create_area(request):
    area = Area.objects.all().order_by('id')
    form = AddArea()
    if request.method == 'POST':
        form = AddArea(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_area')
    return render(request, 'rooms/list_area.html', {'Area': area, 'add_area': form})

def get_house_of_area(request, id):
    area = Area.objects.get(id=id)
    house = House.objects.filter(area=area)
    return render(request, 'rooms/list_house_of_area.html', {'inf_area': area, 'house_of_area': house})

def edit_area(request, id):
    area = get_object_or_404(Area, id=id)
    form = UpdateArea(instance=area)
    if request.method == 'POST':
        form = UpdateArea(request.POST, instance=area)
        if form.is_valid():
            form.save()
            return redirect('list_area')
    return render(request, 'rooms/edit_area.html', {'update_area': form, 'inf_area': area})

def delete_area(request, id):
    area = get_object_or_404(Area, id=id)
    form = DeleteArea(instance=area)
    if request.method == 'POST':
        form = DeleteArea(request.POST, instance=area)
        if form.is_valid():
            form.deleteArea(id)
            return redirect('list_area')
    return render(request, 'rooms/delete_area.html', {'delete_area': form, 'inf_area': area})

def search_area(request):
    form = SearchArea()
    if request.method == 'POST':
        form = SearchArea(request.POST)
        if form.is_valid():
            nameDistrict = form.cleaned_data['nameDistrict']
            area = Area.objects.filter(nameDistrict__icontains=nameDistrict)
    return render(request, 'rooms/search_area.html', {'search_area': form, 'search_nameDistrict': area})

# def calculate_percentage(from_month, to_month):
#     # Chuyển đổi chuỗi tháng thành datetime
#     from_date = datetime.strptime(from_month, '%Y-%m')
#     to_date = datetime.strptime(to_month, '%Y-%m')
#
#     # Tính số tháng giữa from_month và to_month
#     num_months = (to_date.year - from_date.year) * 12 + (to_date.month - from_date.month) + 1
#
#     # Lấy tổng số người từ CSDL từ from_month đến to_month
#     total_guests = Guests.objects.filter(date__month__range=[from_date.month, to_date.month]).count()
#
#     # Tính phần trăm của mỗi tháng
#     percentage = (total_guests / (num_months * 50)) * 100
#
#     return percentage
#
# def calculate_percentage_electricity(from_month_electricity):
#     # Chuyển đổi chuỗi tháng thành datetime
#     from_date = datetime.strptime(from_month_electricity, '%Y-%m')
#
#     # Lấy tổng lượng điện tiêu thụ của tháng trước
#     total_this_month = Electricity.objects.filter(date__month=from_date.month).aggregate(total=Sum('index_electricity'))
#
#     # print("Total this month:", total_this_month)  # Kiểm tra tổng lượng điện tiêu thụ của tháng này
#     # print("Total previous month:", total_previous_month)  # Kiểm tra tổng lượng điện tiêu thụ của tháng trước
#
#     if total_this_month['total'] is None :
#         # Handle case when no data is found
#         return None
#
#     total = total_this_month['total']
#
#     return total
