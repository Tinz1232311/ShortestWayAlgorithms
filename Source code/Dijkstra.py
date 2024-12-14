import tkinter as tk
from tkinter import filedialog
import time  # Thêm time để tính thời gian


# Hàm đọc dữ liệu từ file TXT
def read_graph_from_file(file_path):
    graph = {}
    with open(file_path, 'r') as file:
        for i, line in enumerate(file):
            row = [int(float(x.strip())) if x.strip() and x.strip().lower() != 'inf' else float('inf')
                   for x in line.replace(',', ' ').split()]
            graph[i] = {j: weight for j, weight in enumerate(row) if weight >= 0 and weight != float('inf')}
    return graph


# Dijkstra để tính đường đi ngắn nhất, loại bỏ các cạnh có trọng số âm
def dijkstra(graph, start):
    # Khởi tạo khoảng cách từ đỉnh nguồn đến các đỉnh khác
    distances = {vertex: float('inf') for vertex in graph}
    distances[start] = 0

    # Duyệt qua các đỉnh
    visited = set()

    print(f"Ban đầu khoảng cách: {distances}")
    
    while len(visited) < len(graph):
        # Chọn đỉnh gần nhất chưa được duyệt
        current_vertex = min(
            (v for v in graph if v not in visited),
            key=lambda v: distances[v]
        )
        
        print(f"\nĐỉnh được chọn trong vòng lặp: {current_vertex}")
        
        # Nếu khoảng cách là vô cực, kết thúc vòng lặp
        if distances[current_vertex] == float('inf'):
            break

        # Đánh dấu đã thăm
        visited.add(current_vertex)
        print(f"Đã thăm đỉnh: {current_vertex}")

        # Cập nhật khoảng cách đến các đỉnh lân cận
        for neighbor, weight in graph[current_vertex].items():
            if neighbor not in visited and distances[current_vertex] + weight < distances[neighbor]:
                print(f"Cập nhật khoảng cách từ {current_vertex} đến {neighbor} với trọng số {weight}.")
                print(f"Trước cập nhật: distance[{neighbor}] = {distances[neighbor]}")
                distances[neighbor] = distances[current_vertex] + weight
                print(f"Sau cập nhật: distance[{neighbor}] = {distances[neighbor]}")
        
        print(f"Tình trạng khoảng cách sau vòng lặp: {distances}")

    print("\nThuật toán Dijkstra hoàn thành.")
    return distances


# Giao diện chính và đọc file từ file chọn
def main():
    # Tạo giao diện ẩn để chọn file
    root = tk.Tk()
    root.withdraw()  # Ẩn giao diện chính của Tkinter
    file_path = filedialog.askopenfilename(title="Chọn file TXT đầu vào", filetypes=[("Text files", "*.txt")])

    if not file_path:
        print("Không chọn file. Thoát chương trình.")
        return

    # Đọc dữ liệu từ file đã chọn
    graph = read_graph_from_file(file_path)

    # Yêu cầu người dùng nhập đỉnh nguồn
    try:
        start_vertex = int(input("Nhập đỉnh nguồn: "))
        if start_vertex not in graph:
            print("Đỉnh nguồn không hợp lệ.")
            return

        # Ghi nhận thời gian bắt đầu
        start_time = time.time()  # Thời điểm trước khi chạy thuật toán

        # Chạy thuật toán Dijkstra
        result = dijkstra(graph, start_vertex)

        # Ghi nhận thời gian kết thúc
        end_time = time.time()  # Thời điểm sau khi thuật toán hoàn thành

        # Hiển thị kết quả
        print(f"\nKhoảng cách từ đỉnh {start_vertex} đến các đỉnh khác:")
        for vertex, distance in result.items():
            print(f"Đỉnh {vertex}: {distance if distance != float('inf') else 'Không thể tới'}")

        # Hiển thị thời gian thực thi
        print(f"Thời gian xử lý: {end_time - start_time:.6f} giây")

    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")


if __name__ == "__main__":
    main()
