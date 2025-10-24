from django import forms
import re
from .models import *

#Room
class AddRoom(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['house', 'roomsNumber', 'acreage', 'quantity', 'price', 'interior']

    def clean_roomsNumber(self):
        house=self.cleaned_data['house']
        roomsNumber = self.cleaned_data['roomsNumber']
        if roomsNumber and house:
            existing_room = Room.objects.filter(house=house, roomsNumber=roomsNumber).exists()
            if existing_room:
                raise forms.ValidationError('Nhà này đã có số phòng này rồi, vui lòng chọn số phòng khác.')
        return roomsNumber

    
    def clean_acreage(self):
        acreage = self.cleaned_data['acreage']
        if acreage <= 0:
            raise forms.ValidationError('Diện tích không thể bằng 0')
        return acreage
    
    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        if quantity < 0:
            raise forms.ValidationError('Số lượng không được âm')
        return quantity
    
    def clean_price(self):
        price = self.cleaned_data['price']
        if price < 0:
            raise forms.ValidationError('Giá phòng không được âm')
        return price
    
    
    def save(self):
        Room.objects.create(
            house=self.cleaned_data['house'],
            roomsNumber=self.cleaned_data['roomsNumber'],
            acreage=self.clean_acreage(),
            quantity=self.clean_quantity(),
            price=self.clean_price(),
            interior=self.cleaned_data['interior']
        )
        
class UpdateInformationRoom(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['roomsNumber', 'acreage', 'quantity', 'price', 'interior']
    
    def clean_acreage(self):
        acreage = self.cleaned_data['acreage']
        if acreage <= 0:
            raise forms.ValidationError('Diện tích không thể bằng 0')
        return acreage
    
    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        if quantity < 0:
            raise forms.ValidationError('Số lượng không được âm')
        return quantity
    
    def clean_price(self):
        price = self.cleaned_data['price']
        if price < 0:
            raise forms.ValidationError('Giá phòng không được âm')
        return price
    
    
class DeleteRoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['id']

    def deleteRoom(self, id):
        room = Room.objects.get(id=id)
        room.delete()

class SearchRoom(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['roomsNumber']


#House
class AddHouse(forms.ModelForm):
    class Meta:
        model = House
        fields = ['nameHouse', 'address', 'area', 'personnel']

    def clean_nameHouse(self):
        nameHouse = self.cleaned_data['nameHouse']
        if not re.search(r'^\w+$', nameHouse):
            raise forms.ValidationError("Tên nhà có kí tự đặc biệt")
        return nameHouse

    def clean_address(self):
        address = self.cleaned_data['address']
        if not re.search(r'^(([0-9A-Z]+|[0-9A-Z]+\/[0-9]+),\s((\w+\s\w+\s\w+\s\w+)|(\w+\s\w+\s\w+)|(\w+\s\w+)),\s(Phuong\s(([0-9]+)|([A-Z][a-z]+\s[A-Z][a-z]+\s[A-Z][a-z]+)|([A-Z][a-z]+\s[A-Z][a-z]+))),\s((Quan|Huyen)\s(([0-9]+)|([A-Z][a-z]+\s[A-Z][a-z]+))),\s(Thanh\spho\s(([A-Z][a-z]+\s[A-Z][a-z]+\s[A-Z][a-z]+)|([A-Z][a-z]+\s[A-Z][a-z]+)|([A-Z][a-z]+))))$', address):
            raise forms.ValidationError('Địa chỉ viết không dấu có dạng: số nhà, tên đường, Phường, Quận(Huyện), Thành phố')
        try:
            House.objects.get(address=address)
        except House.DoesNotExist:
            return address
        raise forms.ValidationError('Địa chỉ vừa nhập đã có nhà ròi, vui lòng nhập địa chỉ khác')
     

    def save(self):
        House.objects.create(nameHouse=self.cleaned_data['nameHouse'],
                             address=self.cleaned_data['address'],
                             area=self.cleaned_data['area'],
                             personnel=self.cleaned_data['personnel'])

class UpdateInformationHouse(forms.ModelForm):
    class Meta:
        model = House
        fields = ['nameHouse', 'address', 'area', 'personnel']

    def clean_nameHouse(self):
        nameHouse = self.cleaned_data['nameHouse']
        if not re.search(r'^\w+$', nameHouse):
            raise forms.ValidationError("Tên nhà có kí tự đặc biệt")
        return nameHouse
        
    def clean_address(self):
        address = self.cleaned_data['address']
        if not re.search(r'^(([0-9A-Z]+|[0-9A-Z]+\/[0-9]+),\s((\w+\s\w+\s\w+\s\w+)|(\w+\s\w+\s\w+)|(\w+\s\w+)),\s(Phuong\s(([0-9]+)|([A-Z][a-z]+\s[A-Z][a-z]+\s[A-Z][a-z]+)|([A-Z][a-z]+\s[A-Z][a-z]+))),\s((Quan|Huyen)\s(([0-9]+)|([A-Z][a-z]+\s[A-Z][a-z]+))),\s(Thanh\spho\s(([A-Z][a-z]+\s[A-Z][a-z]+\s[A-Z][a-z]+)|([A-Z][a-z]+\s[A-Z][a-z]+)|([A-Z][a-z]+))))$', address):
            raise forms.ValidationError('Địa chỉ viết không dấu có dạng: số nhà, tên đường, Phường, Quận(Huyện), Thành phố')
        try:
            House.objects.get(address=address)
        except House.DoesNotExist:
            return address
        raise forms.ValidationError('Địa chỉ vừa nhập đã có nhà ròi, vui lòng nhập địa chỉ khác')
    

    
    
class DeleteHouseForm(forms.ModelForm):
    class Meta:
        model = House
        fields = ['id']
    
    def deleteHouse(self, id):
        house = House.objects.get(id=id)
        house.delete()
       
class SearchHouse(forms.ModelForm):
    class Meta:
        model = House
        fields = ['nameHouse']

        

# Guest
class AddGuestForm(forms.ModelForm):
    class Meta:
        model = Guests
        fields = ['room','fullname', 'phone', 'date']
        
    def clean_fullname(self):
        fullname = self.cleaned_data['fullname']
        if not re.search(r'^[A-Z][a-z]+\s(?:[A-Z][a-z]+\s?){1,3}[A-Z][a-z]+$', fullname):
            raise forms.ValidationError('Tên không có dấu và viết hoa các kí tự đầu')
        return fullname

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not re.search(r'^(09|03)([0-9]{8})$', phone):
            raise forms.ValidationError('số điện thoại có 10 số và bắt đầu bằng 09 hoặc 03')
        try:
            Guests.objects.get(phone=phone)
        except Guests.DoesNotExist:
            return phone
        raise forms.ValidationError('số điện thoại bạn nhập đã tồn tại')
          
          
    def clean_room(self):
        room = self.cleaned_data['room']
        if room:
            num_guests = Guests.objects.filter(room=room).count()
            if num_guests >= room.quantity:
                raise forms.ValidationError('Số lượng khách đã đặt phòng đã đạt đến giới hạn')
        return room

              
    def save(self):
        Guests.objects.create(room=self.cleaned_data['room'],
                              fullname=self.clean_fullname(),
                              phone=self.clean_phone(),
                              date=self.cleaned_data['date'])


class UpdateGuestForm(forms.ModelForm):
    class Meta:
        model = Guests
        fields = ['room','fullname', 'phone', 'date']
        
    def clean_fullname(self):
        fullname = self.cleaned_data['fullname']
        if not re.search(r'^[A-Z][a-z]+\s(?:[A-Z][a-z]+\s?){1,3}[A-Z][a-z]+$', fullname):
            raise forms.ValidationError('Tên không có dấu và viết hoa các kí tự đầu')
        return fullname

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not re.search(r'^(09|03)([0-9]{8})$', phone):
            raise forms.ValidationError('số điện thoại có 10 số và bắt đầu bằng 09 hoặc 03')
        try:
            Guests.objects.get(phone=phone)
        except Guests.DoesNotExist:
            return phone
        raise forms.ValidationError('số điện thoại bạn nhập đã tồn tại')
                    
               
class DeleteGuestForm(forms.ModelForm):
    class Meta:
        model = Guests
        fields = ['id']
        
    def deleteGuest(self, id):
        guest = Guests.objects.get(id=id)
        guest.delete()
         
    
class SearchGuestByFullnameForm(forms.ModelForm): 
    class Meta:
        model = Guests
        fields = ['fullname'] 
        

    
#Personnel
class AddPersonnel(forms.ModelForm):
    class Meta:
        model = Personnel
        fields = ['id_personnel', 'fullname', 'phone']

    def clean_id(self):
        id_personnel = self.cleaned_data['id_personnel']
        if not re.search(r'^(NV)[0-9]+$', id_personnel):
            raise forms.ValidationError('Mã nhân viên có dạng NV"số". VD: NV1, NV42, ...')
        try:
            Personnel.objects.get(id_personnel=id_personnel)
        except Personnel.DoesNotExist:
            return id_personnel
        raise forms.ValidationError('Mã nhân viên này đã tồn tại, vui lòng nhập mã khác')

    def clean_fullname(self):
        fullname = self.cleaned_data['fullname']
        if not re.search(r'^[A-Z][a-z]+\s(?:[A-Z][a-z]+\s?){1,3}[A-Z][a-z]+$', fullname):
            raise forms.ValidationError('Tên bạn nhập không hợp lệ')
        return fullname

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not re.search(r'^(09|03)([0-9]{8})$', phone):
            raise forms.ValidationError('số điện thoại có 10 số và bắt đầu bằng 09 hoặc 03')
        try:
            Personnel.objects.get(phone=phone)
        except Personnel.DoesNotExist:
            return phone
        raise forms.ValidationError('số điện thoại bạn nhập đã tồn tại')
        
    def save(self):
        Personnel.objects.create(id_personnel=self.clean_id(), 
                                 fullname=self.clean_fullname(), 
                                 phone=self.clean_phone())

class UpdateInformationPersonnel(forms.ModelForm):
    class Meta:
        model = Personnel
        fields = ['fullname', 'phone']
        
    def clean_fullname(self):
        fullname = self.cleaned_data['fullname']
        if not re.search(r'^[A-Z][a-z]+\s(?:[A-Z][a-z]+\s?){1,3}[A-Z][a-z]+$', fullname):
            raise forms.ValidationError('Tên bạn nhập không hợp lệ')
        return fullname

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not re.search(r'^(09|03)([0-9]{8})$', phone):
            raise forms.ValidationError('số điện thoại có 10 số và bắt đầu bằng 09 hoặc 03')
        try:
            Personnel.objects.get(phone=phone)
        except Personnel.DoesNotExist:
            return phone
        raise forms.ValidationError('số điện thoại bạn nhập đã tồn tại')

class DeletePersonnel(forms.ModelForm):
    class Meta:
        model = Personnel
        fields = ['id_personnel']

    def deletePersonnel(self, id):
        personnel = Personnel.objects.get(id_personnel=id)
        personnel.delete()

class SearchPersonnel(forms.ModelForm):
    class Meta:
        model = Personnel
        fields = ['fullname']

        
#Area
class AddArea(forms.ModelForm):
    class Meta:
        model = Area
        fields = ['nameDistrict']
    
    def clean_nameDistrict(self):
        discrict = self.cleaned_data['nameDistrict']
        if not re.search(r'^((Quan|Huyen)\s(([0-9]+)|([A-Z][a-z]+\s[A-Z][a-z]+)))$', discrict):
            raise forms.ValidationError('Khu vực có định dạng: Quan Abc Cde, Quan 1, Huyen 1, Huyen Abc Cde')
        try:
            Area.objects.get(nameDistrict=discrict)
        except Area.DoesNotExist:
            return discrict
        raise forms.ValidationError('Khu vực bạn nhập đã có rồi')
    
    def save(self):
        Area.objects.create(nameDistrict=self.cleaned_data['nameDistrict'])
    
class UpdateArea(forms.ModelForm):
    class Meta:
        model = Area
        fields = ['nameDistrict']
    
    def clean_nameDistrict(self):
        discrict = self.cleaned_data['nameDistrict']
        if not re.search(r'^((Quan|Huyen)\s(([0-9]+)|([A-Z][a-z]+\s[A-Z][a-z]+)))$', discrict):
            raise forms.ValidationError('Khu vực có định dạng: Quan Tan Phu, Quan 1, Huyen 1, Huyen Binh Chanh')
        try:
            Area.objects.get(nameDistrict=discrict)
        except Area.DoesNotExist:
            return discrict
        raise forms.ValidationError('Khu vực bạn nhập đã có rồi')
    
class DeleteArea(forms.ModelForm):
    class Meta:
        model = Area
        fields = ['id']
    
    def deleteArea(self, id):
        area = Area.objects.get(id=id)
        area.delete()

class SearchArea(forms.ModelForm):
    class Meta:
        model = Area
        fields = ['nameDistrict']

#statistical
class StatisticalGuest(forms.ModelForm):
    class Meta:
        model = Guests
        fields = ['date']

class StatisticalElectricity(forms.ModelForm):
    class Meta:
        model = Electricity
        fields = ['date']

#Electricity
class ElectricityForm(forms.ModelForm):
    class Meta:
        model = Electricity
        fields = ['date', 'index_electricity','room']

    def clean_index_electricity(self):
        index_electricity = self.cleaned_data['index_electricity']
        if index_electricity <= 0:
            raise forms.ValidationError('Chỉ số điện không được âm')

        return index_electricity

    def save(self):
        Electricity.objects.create(room=self.cleaned_data['room'],
                              index_electricity=self.clean_index_electricity(),
                              date=self.cleaned_data['date'])
        
class UpdateElectricity(forms.ModelForm):
    class Meta:
        model = Electricity
        fields = ['index_electricity', 'date']
    
    def clean_index_electricity(self):
        index_electricity = self.cleaned_data['index_electricity']
        if index_electricity <= 0:
            raise forms.ValidationError('Chỉ số điện không được âm')
        return index_electricity
    
    

class DeleteElectricity(forms.ModelForm):
    class Meta:
        model = Electricity
        fields = ['id']
    
    def deleteElectricity(self, id):
        index_electricity = Electricity.objects.get(id=id)
        index_electricity.delete()


    
