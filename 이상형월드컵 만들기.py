import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import random

# 후보 리스트를 담을 변수
candidates = []
round_number = 1
total_candidates = 0

# 이미지 업로드 함수
def upload_image():
    file_path = filedialog.askopenfilename(title="이미지 파일 선택", filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
    if file_path:
        image = Image.open(file_path)
        image.thumbnail((200, 200))  # 이미지 크기 조정
        return ImageTk.PhotoImage(image)
    return None

# 후보 추가 함수
def add_candidate():
    name = name_entry.get()
    image = upload_image()
    if name and image:
        candidates.append((name, image))
        listbox.insert(tk.END, name)  # 후보 리스트 박스에 이름 추가
        name_entry.delete(0, tk.END)  # 이름 입력란 초기화

# 대진표 크기 설정 (8강, 16강, 32강, 64강)
def set_tournament_size():
    global total_candidates
    size = tournament_size_var.get()
    if size == 8:
        total_candidates = 8
    elif size == 16:
        total_candidates = 16
    elif size == 32:
        total_candidates = 32
    elif size == 64:
        total_candidates = 64
    candidates.clear()  # 후보 초기화
    listbox.delete(0, tk.END)  # 리스트 박스 초기화
    result_label.config(text="후보를 추가하세요.")

# 대진표 시작
def start_tournament():
    global round_number
    round_number = 1
    if len(candidates) < total_candidates:
        result_label.config(text=f"{total_candidates}명의 후보가 필요합니다!")
        return
    
    # 후보 수가 많으면 무작위로 8명만 추출
    if len(candidates) > total_candidates:
        candidates_selected = random.sample(candidates, total_candidates)
    else:
        candidates_selected = candidates

    random.shuffle(candidates_selected)  # 후보들을 무작위로 섞기
    next_round_candidates = [candidates_selected[i] for i in range(len(candidates_selected))]
    run_round(next_round_candidates)

# 라운드 진행 함수
def run_round(candidates_in_round):
    global round_number
    if len(candidates_in_round) == 1:
        result_label.config(text=f"최종 승자: {candidates_in_round[0][0]}")
        return
    if len(candidates_in_round) % 2 != 0:
        candidates_in_round.append(candidates_in_round[-1])  # 홀수일 때 자동 승자 처리

    # 1:1 대결
    round_display.config(text=f"{round_number}라운드")
    candidate1_name, candidate1_image = candidates_in_round[0]
    candidate2_name, candidate2_image = candidates_in_round[1]
    
    # 이미지 및 이름 표시
    candidate1_label.config(image=candidate1_image, text=candidate1_name, compound="top")
    candidate2_label.config(image=candidate2_image, text=candidate2_name, compound="top")
    
    # 버튼 클릭 시 승자 선택
    def select_winner(winner):
        nonlocal candidates_in_round
        if winner == 1:
            next_round_candidates = candidates_in_round[::2]  # 1번 승자
        else:
            next_round_candidates = candidates_in_round[1::2]  # 2번 승자
        round_number += 1
        run_round(next_round_candidates)

    button1 = tk.Button(window, text=f"{candidate1_name} 승자", command=lambda: select_winner(1))
    button2 = tk.Button(window, text=f"{candidate2_name} 승자", command=lambda: select_winner(2))
    
    button1.pack()
    button2.pack()

# GUI 설정
window = tk.Tk()
window.title("이상형 월드컵 소프트웨어")

# 라운드 크기 설정
tournament_size_label = tk.Label(window, text="대진표 크기 선택")
tournament_size_label.pack()

# 라운드 크기 선택 (8강, 16강, 32강, 64강)
tournament_size_var = tk.IntVar()
tournament_size_var.set(8)  # 기본값 8강
tournament_size_8 = tk.Radiobutton(window, text="8강", variable=tournament_size_var, value=8)
tournament_size_8.pack()
tournament_size_16 = tk.Radiobutton(window, text="16강", variable=tournament_size_var, value=16)
tournament_size_16.pack()
tournament_size_32 = tk.Radiobutton(window, text="32강", variable=tournament_size_var, value=32)
tournament_size_32.pack()
tournament_size_64 = tk.Radiobutton(window, text="64강", variable=tournament_size_var, value=64)
tournament_size_64.pack()

# 라운드 크기 설정 버튼
set_size_button = tk.Button(window, text="대진표 크기 설정", command=set_tournament_size)
set_size_button.pack()

# 후보 추가 UI
name_label = tk.Label(window, text="후보 이름 입력")
name_label.pack()
name_entry = tk.Entry(window)
name_entry.pack()

add_button = tk.Button(window, text="후보 추가", command=add_candidate)
add_button.pack()

# 후보 리스트
listbox = tk.Listbox(window)
listbox.pack()

# 대진표 시작
start_button = tk.Button(window, text="대진표 시작", command=start_tournament)
start_button.pack()

# 라운드 표시
round_display = tk.Label(window, text="0라운드")
round_display.pack()

# 결과 라벨
result_label = tk.Label(window, text="")
result_label.pack()

# 후보자 이미지 표시
candidate1_label = tk.Label(window)
candidate1_label.pack(side=tk.LEFT, padx=20)

candidate2_label = tk.Label(window)
candidate2_label.pack(side=tk.LEFT, padx=20)

window.mainloop()
