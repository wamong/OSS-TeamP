import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
import random

# 후보 리스트를 담을 변수
candidates = []
selected_images = []

# 이미지 업로드 함수
def upload_images():
    file_paths = filedialog.askopenfilenames(title="여러 이미지 파일 선택", filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
    if file_paths:
        for file_path in file_paths:
            image = Image.open(file_path)
            image.thumbnail((200, 200))  # 이미지 크기 조정
            image_tk = ImageTk.PhotoImage(image)
            selected_images.append({'image': image_tk, 'image_path': file_path})
        update_selected_images()

# 선택된 이미지 목록 업데이트
def update_selected_images():
    for widget in selected_image_frame.winfo_children():
        widget.destroy()
    
    for image in selected_images:
        frame = tk.Frame(selected_image_frame)
        frame.pack(pady=10)

        label_image = tk.Label(frame, image=image['image'])
        label_image.image = image['image']  # 이미지 참조 유지
        label_image.pack(side=tk.LEFT)

        name_entry = tk.Entry(frame, font=("Arial", 12))
        name_entry.pack(side=tk.LEFT, padx=10)

        add_button = tk.Button(frame, text="후보 추가", command=lambda img=image, entry=name_entry: add_candidate(img, entry))
        add_button.pack(side=tk.LEFT)

# 후보 추가 함수
def add_candidate(image, name_entry):
    name = name_entry.get()
    if name:
        candidates.append({'name': name, 'image': image['image'], 'image_path': image['image_path']})
        listbox.insert(tk.END, name)  # 후보 이름을 리스트 박스에 추가
        update_candidates_list()

# 후보 목록 업데이트
def update_candidates_list():
    listbox.delete(0, tk.END)
    for candidate in candidates:
        listbox.insert(tk.END, candidate['name'])

# 대회 시작 함수
def start_tournament():
    if len(candidates) < 2:
        result_label.config(text="최소 2명의 후보가 필요합니다.")
        return
    
    random.shuffle(candidates)
    run_round(candidates)

# 라운드 진행 함수
def run_round(candidates_in_round):
    if len(candidates_in_round) == 1:
        result_label.config(text=f"최종 승자: {candidates_in_round[0]['name']}")
        return
    if len(candidates_in_round) % 2 != 0:
        candidates_in_round.append(candidates_in_round[-1])  # 홀수일 때 자동 승자 처리

    # 1:1 대결
    candidate1 = candidates_in_round[0]
    candidate2 = candidates_in_round[1]

    candidate1_label.config(image=candidate1['image'], text=candidate1['name'], compound="top")
    candidate2_label.config(image=candidate2['image'], text=candidate2['name'], compound="top")

    # 버튼 클릭 시 승자 선택
    def select_winner(winner):
        if winner == 1:
            next_round_candidates = candidates_in_round[::2]
        else:
            next_round_candidates = candidates_in_round[1::2]
        run_round(next_round_candidates)

    button1 = tk.Button(window, text=f"{candidate1['name']} 승자", command=lambda: select_winner(1))
    button2 = tk.Button(window, text=f"{candidate2['name']} 승자", command=lambda: select_winner(2))

    button1.pack()
    button2.pack()

# 저장된 대회 목록 불러오기
def load_saved_tournaments():
    # 저장된 대회들 불러오기
    pass

# 대회 저장 함수
def save_tournament():
    # 대회 저장하기
    pass

# 사진 저장 함수
def save_image_to_left(image, name_entry):
    name = name_entry.get()
    if name:
        # 이름을 왼쪽 하단에 표시
        left_listbox.insert(tk.END, name)
        selected_images.clear()  # 오른쪽 구역 이미지 비우기
        update_selected_images()

# GUI 설정
window = tk.Tk()
window.title("이상형 월드컵 소프트웨어")
window.geometry("1200x800")

# 화면을 3개 구역으로 나누기 위한 프레임들
left_frame = tk.Frame(window, width=300, height=800, bg="lightgray")
left_frame.pack(side="left", fill="y")

center_frame = tk.Frame(window, width=600, height=800)
center_frame.pack(side="left", fill="y")

right_frame = tk.Frame(window, width=300, height=800)
right_frame.pack(side="left", fill="y")

# 왼쪽 구역 상단: 저장된 이상형 월드컵 목록
saved_label = tk.Label(left_frame, text="저장된 이상형 월드컵 목록", font=("Arial", 14))
saved_label.pack(pady=10)

left_listbox = tk.Listbox(left_frame, height=10, width=25, font=("Arial", 12))
left_listbox.pack(padx=20, pady=10)

# 왼쪽 구역 하단: 사진 이름
photo_label = tk.Label(left_frame, text="저장된 사진 이름", font=("Arial", 14))
photo_label.pack(pady=10)

# 중앙 구역
title_label = tk.Label(center_frame, text="대회 타이틀 입력", font=("Arial", 14))
title_label.pack(pady=10)

title_entry = tk.Entry(center_frame, font=("Arial", 12))
title_entry.pack(pady=5)

# 후보 이미지 추가
add_button = tk.Button(center_frame, text="여러 후보 이미지 추가", command=upload_images, font=("Arial", 14))
add_button.pack(pady=10)

# 라운드 선택 (라디오버튼)
round_label = tk.Label(center_frame, text="라운드 선택", font=("Arial", 12))
round_label.pack(pady=5)

round_var = tk.StringVar(value="8")
round_4_button = tk.Radiobutton(center_frame, text="4강", variable=round_var, value="4")
round_4_button.pack(anchor="w")
round_8_button = tk.Radiobutton(center_frame, text="8강", variable=round_var, value="8")
round_8_button.pack(anchor="w")
round_16_button = tk.Radiobutton(center_frame, text="16강", variable=round_var, value="16")
round_16_button.pack(anchor="w")
round_32_button = tk.Radiobutton(center_frame, text="32강", variable=round_var, value="32")
round_32_button.pack(anchor="w")
round_64_button = tk.Radiobutton(center_frame, text="64강", variable=round_var, value="64")
round_64_button.pack(anchor="w")

# 대회 시작 버튼
start_button = tk.Button(center_frame, text="대회 시작", command=start_tournament, font=("Arial", 14))
start_button.pack(pady=10)

# 대회 저장 버튼
save_button = tk.Button(center_frame, text="대회 저장", command=save_tournament, font=("Arial", 14))
save_button.pack(pady=10)

# 오른쪽 구역: 선택한 후보 이미지들 및 이름 입력
right_label = tk.Label(right_frame, text="선택된 후보", font=("Arial", 14))
right_label.pack(pady=10)

selected_image_frame = tk.Frame(right_frame)
selected_image_frame.pack(pady=10)

# 사진 저장 버튼
save_image_button = tk.Button(right_frame, text="사진 저장", command=lambda: save_image_to_left(selected_images[0], name_entry), font=("Arial", 14))
save_image_button.pack(pady=10)

# 실행
window.mainloop()
