# serialcomm/views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import serial
import threading

serial_lock = threading.Lock()

# Inisialisasi port COM6 (ubah jika berbeda)
try:
    arduino = serial.Serial('COM6', 9600, timeout=2)
except serial.SerialException as e:
    arduino = None
    print("ERROR: Tidak bisa membuka port COM6:", e)

@csrf_exempt
def send_to_serial(request):
    if request.method == "POST":
        if not arduino or not arduino.is_open:
            return JsonResponse({"status": "error", "error": "Serial port COM6 tidak tersedia"}, status=500)

        try:
            data = json.loads(request.body)
            message = data.get("message", "")

            if not message:
                return JsonResponse({"status": "error", "error": "Pesan kosong"}, status=400)

            with serial_lock:
                print("Kirim ke Arduino:", message)

                arduino.write((message + "\n").encode())
                arduino.flush()

                response = arduino.readline().decode().strip()
                print("Balasan dari Arduino:", response)


            return JsonResponse({
                "status": "ok",
                "message_sent": message,
                "arduino_response": response
            })

        except Exception as e:
            return JsonResponse({"status": "error", "error": str(e)}, status=500)

    return JsonResponse({"status": "error", "error": "Metode harus POST"}, status=405)
