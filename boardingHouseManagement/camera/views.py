from django.shortcuts import render
import subprocess
# Create your views here.
# def create_camera(request):
#     return render(request, 'cameras/list_file_image.html')

# def face_detection_view(request):
#     return render(request, 'cameras/list_file_image.html')

# def face_detection_view(request):
#     subprocess.Popen(['python', 'E:\\Workspace\\BoardingHouseManagement\\boardingHouseManagement\\camera\\model-building.py'])
#     return render(request, 'cameras/list_file_image.html')

def face_detection_view(request):
    if request.method == 'POST':
        # Xử lý sự kiện khi nhấn vào nút "Bắt đầu nhận diện"
        subprocess.Popen(['python', 'E:\\Workspace\\BoardingHouseManagement\\boardingHouseManagement\\camera\\formadd.py'])
        return render(request, 'cameras/list_file_image.html')  # Hoặc chuyển hướng đến một trang khác nếu cần

    return render(request, 'cameras/list_file_image.html')

