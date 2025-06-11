from django.shortcuts import render
from django.http import JsonResponse
from pymodbus.client import ModbusTcpClient
import json

def modbus_data(request): 
    if request.method == "POST" and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
    # Modbus 통신 코드 실행
        receiveData = json.loads(request.body)
        mod = receiveData.get("mod")
        ipAddress = receiveData.get("ipAddress")
        ipAddress = ipAddress.strip()

        client = ModbusTcpClient(ipAddress)
        client.connect()

        result = None
        response_data = {}

        if mod == "writeRegister":
            registerAddress = receiveData.get("registerAddress")
            registerValue = receiveData.get("registerValue")

            client.write_register(int(registerAddress)-1, int(registerValue))

        elif mod == "readRegister":
            registerAddress = receiveData.get("registerAddress")

            result = client.read_holding_registers(int(registerAddress)-1, count=1)
            if not result.isError():
                response_data["register"] = str(result.registers[0])

        elif mod == "writeCoil":
            coilAddress = receiveData.get("coilAddress")
            coilValue = receiveData.get("coilValue")

            client.write_coil(int(coilAddress)-1, coilValue=="True")

        elif mod == "readCoil":
            firstAddress = receiveData.get("firstAddress")
            lastAddress = receiveData.get("lastAddress")
            readCount = int(lastAddress)-int(firstAddress)+1

            result = client.read_coils(int(firstAddress)-1, count=readCount)
            if not result.isError():
                resultCoils = ", ".join(list(map(str, result.bits[:readCount])))
                response_data["coils"] = resultCoils

        client.close()
        #응답 데이터 반환
        response_data["message"] = "Modbus 통신 완료."
        return JsonResponse(response_data)
    else:
        #AJAX 요청이 아니거나 POST 메소드가 아닌 경우
        return JsonResponse({"error": "잘못된 요청."}, status=400)

# Create your views here.
def modbus(request):
    return render(
        request,
        'modbus/modbus.html'
    )