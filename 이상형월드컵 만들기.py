import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk

# 후보 리스트를 담을 변수
candidates = []

# 이미지 업로드 함수
def upload_images():
    file_paths = filedialog.askopenfilenames(title="여러 이미지 파일 선택", filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
    if file_paths:
        for file_path in file_paths:
            image = Image.open(file_path)
            image.thumbnail((200, 200))  # 이미지 크기 조정
            image_tk = ImageTk.PhotoImage(image)
            candidate_entry_frame(file_path, image_tk)

# 후보 이름과 이미지 미리보기 추가
def candidate_entry_frame(image_path, image_tk):
    # 이미지와 이름을 입력할 프레임
    frame = tk.Frame(scrollable_frame)
    frame.pack(pady=10)

    # 이미지 미리보기
    label_image = tk.Label(frame, image=image_tk)
    label_image.image = image_tk  # 이미지 참조를 유지
    label_image.pack(side=tk.LEFT)

    # 이름 입력란
    name_entry = tk.Entry(frame, font=("Arial", 12))
    name_entry.pack(side=tk.LEFT, padx=10)

    # 후보 추가 버튼
    add_button = tk.Button(frame, text="후보 추가", command=lambda: add_candidate(name_entry, image_path, image_tk))
    add_button.pack(side=tk.LEFT)

# 후보 추가 함수
def add_candidate(name_entry, image_path, image_tk):
    name = name_entry.get()
    if name:
        candidates.append({'name': name, 'image': image_tk, 'image_path': image_path})
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

# GUI 설정
window = tk.Tk()
window.title("이상형 월드컵 소프트웨어")
window.geometry("1200x800")

# 타이틀 입력란
title_label = tk.Label(window, text="대회 타이틀 입력", font=("Arial", 14))
title_label.pack(pady=10)
title_entry = tk.Entry(window, font=("Arial", 12))
title_entry.pack(pady=5)

# 후보 목록
listbox_label = tk.Label(window, text="후보 목록", font=("Arial", 14))
listbox_label.pack(pady=10)

# 후보 목록을 스크롤 가능하게 만들기 위해 Canvas와 Scrollbar 사용
canvas = tk.Canvas(window)
scrollbar = tk.Scrollbar(window, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas)

# Canvas와 Scrollbar 연결
canvas.configure(yscrollcommand=scrollbar.set)

# 스크롤 영역에 프레임 추가
scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

# 스크롤 가능한 영역에 프레임을 추가
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

# Canvas와 Scrollbar 배치
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# 이미지 미리보기
candidate_preview_label = tk.Label(window, text="이미지 미리보기", font=("Arial", 12))
candidate_preview_label.pack(pady=20)

# 후보 추가 버튼
add_button = tk.Button(window, text="여러 후보 이미지 추가", command=upload_images, font=("Arial", 14))
add_button.pack(pady=10)

# 대회 시작 버튼
start_button = tk.Button(window, text="대회 시작", command=start_tournament, font=("Arial", 14))
start_button.pack(pady=10)

# 결과 표시
result_label = tk.Label(window, text="", font=("Arial", 16))
result_label.pack(pady=20)

# 실행
window.mainloop()
