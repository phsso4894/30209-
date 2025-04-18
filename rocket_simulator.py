
import json

class Rocket:
    def __init__(self, data):
        self.model = data["model"]
        self.destination = data["destination"]
        self.fuel = data["fuel"]
        self.mass = data["mass"]
        self.angle = data["angle"]
        self.time = data.get("time", 5)
        self.thrust_coeff = 50  # 단순 추력 계수
        self.g = 9.8

    def calculate_distance(self):
        thrust = self.fuel * self.thrust_coeff
        acceleration = thrust / self.mass
        velocity = acceleration * self.time
        angle_rad = self.angle * 3.14159 / 180
        distance = (velocity ** 2 * __import__('math').sin(2 * angle_rad)) / self.g
        return round(distance, 2)

    def interpret_result(self):
        if 40 <= self.angle <= 50:
            return "[해석] 이상적인 발사각으로 효율적인 비행이 예상됩니다."
        elif self.angle < 30:
            return "[해석] 발사각이 낮아 충분한 수평 거리를 얻기 어려울 수 있습니다."
        elif self.angle > 60:
            return "[해석] 각도가 너무 커서 상승 위주 비행으로 거리가 짧아질 수 있습니다."
        else:
            return "[해석] 일반적인 범위의 발사각입니다."

    def show_info(self):
        print(f"\n===== 로켓 상태 리포트 =====")
        print(f"모델: {self.model} | 목적지: {self.destination}")
        print(f"연료: {self.fuel}kg | 질량: {self.mass}kg | 각도: {self.angle}° | 가속 시간: {self.time}초")
        print(f"도달 거리: {self.calculate_distance()}m")
        print(self.interpret_result())

    def modify_data(self):
        try:
            fuel_input = input(f"현재 연료: {self.fuel}kg ➝ 새 연료 입력: ")
            if fuel_input.strip():
                self.fuel = float(fuel_input)

            mass_input = input(f"현재 질량: {self.mass}kg ➝ 새 질량 입력: ")
            if mass_input.strip():
                self.mass = float(mass_input)

            angle_input = input(f"현재 발사각: {self.angle}° ➝ 새 각도 입력: ")
            if angle_input.strip():
                self.angle = float(angle_input)

            print("[안내] 데이터가 성공적으로 수정되었습니다!")
        except Exception as e:
            print(f"[오류] 수정 중 문제 발생: {e}")


def load_rockets(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[오류] '{file_path}' 파일을 불러오는 데 실패했습니다: {e}")
        return []

# 로켓 데이터 로드 및 객체 생성
rocket_data = load_rockets("rocket_data.json")
rocket_db = {data["model"].upper(): Rocket(data) for data in rocket_data}

while True:
    user_input = input("\n로켓 모델명을 입력하세요 (예: FALCON 9) 또는 '종료': ").upper()
    if user_input == "종료":
        print("[안내] 프로그램을 종료합니다.")
        break
    elif user_input in rocket_db:
        rocket = rocket_db[user_input]
        rocket.show_info()

        if input("데이터를 수정하시겠습니까? (Y/N): ").upper() == "Y":
            rocket.modify_data()
            rocket.show_info()
    else:
        print("[경고] 해당 로켓은 데이터베이스에 없습니다. 정확한 모델명을 입력해주세요.")
