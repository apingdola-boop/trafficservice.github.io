"""
네이버 지도 API를 활용한 최단 거리 및 유류비 계산 (Flask) — 레거시
실행: 이 폴더에서 NAVER_CLIENT_ID / NAVER_CLIENT_SECRET 설정 후 python app.py
"""
import os

from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

NAVER_CLIENT_ID = os.environ.get("NAVER_CLIENT_ID", "").strip()
NAVER_CLIENT_SECRET = os.environ.get("NAVER_CLIENT_SECRET", "").strip()

DEFAULT_FUEL_PRICE = 1650
DEFAULT_FUEL_EFFICIENCY = 12


def geocode_address(address):
    if not NAVER_CLIENT_ID or not NAVER_CLIENT_SECRET:
        return {"success": False, "error": "NAVER_CLIENT_ID / NAVER_CLIENT_SECRET 환경 변수를 설정하세요."}
    url = "https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode"
    headers = {
        "X-NCP-APIGW-API-KEY-ID": NAVER_CLIENT_ID,
        "X-NCP-APIGW-API-KEY": NAVER_CLIENT_SECRET,
    }
    params = {"query": address}

    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)
        print(f"[Geocode] 주소: {address}")
        print(f"[Geocode] 상태코드: {response.status_code}")
        print(f"[Geocode] 응답: {response.text[:500]}")

        data = response.json()

        if data.get("status") == "OK" and data.get("addresses"):
            addr = data["addresses"][0]
            return {
                "success": True,
                "x": addr["x"],
                "y": addr["y"],
                "address": addr["roadAddress"] or addr["jibunAddress"],
            }
        error_msg = data.get(
            "errorMessage",
            data.get("error", {}).get("message", "주소를 찾을 수 없습니다."),
        )
        return {"success": False, "error": f"{error_msg} (status: {data.get('status', 'unknown')})"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_directions(start_x, start_y, end_x, end_y):
    if not NAVER_CLIENT_ID or not NAVER_CLIENT_SECRET:
        return {"success": False, "error": "네이버 API 키가 설정되지 않았습니다."}
    url = "https://naveropenapi.apigw.ntruss.com/map-direction/v1/driving"
    headers = {
        "X-NCP-APIGW-API-KEY-ID": NAVER_CLIENT_ID,
        "X-NCP-APIGW-API-KEY": NAVER_CLIENT_SECRET,
    }
    params = {
        "start": f"{start_x},{start_y}",
        "goal": f"{end_x},{end_y}",
        "option": "trafast",
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)
        data = response.json()

        if data.get("code") == 0 and data.get("route"):
            route = data["route"]["trafast"][0]["summary"]
            return {
                "success": True,
                "distance": route["distance"],
                "duration": route["duration"],
                "tollFare": route.get("tollFare", 0),
                "fuelPrice": route.get("fuelPrice", 0),
            }
        return {"success": False, "error": data.get("message", "경로를 찾을 수 없습니다.")}
    except Exception as e:
        return {"success": False, "error": str(e)}


def calculate_fuel_cost(distance_m, fuel_price, fuel_efficiency):
    distance_km = distance_m / 1000
    fuel_needed = distance_km / fuel_efficiency
    fuel_cost = fuel_needed * fuel_price
    return {
        "distance_km": round(distance_km, 2),
        "fuel_needed": round(fuel_needed, 2),
        "fuel_cost": round(fuel_cost, 0),
    }


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/calculate", methods=["POST"])
def calculate_route():
    data = request.json
    start_address = data.get("start")
    end_address = data.get("end")
    fuel_price = data.get("fuel_price", DEFAULT_FUEL_PRICE)
    fuel_efficiency = data.get("fuel_efficiency", DEFAULT_FUEL_EFFICIENCY)

    if not start_address or not end_address:
        return jsonify({"success": False, "error": "출발지와 도착지를 입력해주세요."})

    start_geo = geocode_address(start_address)
    if not start_geo["success"]:
        return jsonify({"success": False, "error": f"출발지 오류: {start_geo['error']}"})

    end_geo = geocode_address(end_address)
    if not end_geo["success"]:
        return jsonify({"success": False, "error": f"도착지 오류: {end_geo['error']}"})

    route = get_directions(start_geo["x"], start_geo["y"], end_geo["x"], end_geo["y"])
    if not route["success"]:
        return jsonify({"success": False, "error": f"경로 탐색 오류: {route['error']}"})

    fuel_calc = calculate_fuel_cost(route["distance"], fuel_price, fuel_efficiency)

    duration_min = route["duration"] // 60000
    duration_hour = duration_min // 60
    duration_remaining_min = duration_min % 60

    if duration_hour > 0:
        duration_str = f"{duration_hour}시간 {duration_remaining_min}분"
    else:
        duration_str = f"{duration_remaining_min}분"

    return jsonify(
        {
            "success": True,
            "start_address": start_geo["address"],
            "end_address": end_geo["address"],
            "distance_km": fuel_calc["distance_km"],
            "duration": duration_str,
            "duration_min": duration_min,
            "toll_fare": route["tollFare"],
            "fuel_needed": fuel_calc["fuel_needed"],
            "fuel_cost": fuel_calc["fuel_cost"],
            "total_cost": fuel_calc["fuel_cost"] + route["tollFare"],
        }
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
