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


# Hàm Dijkstra để tính đường đi ngắn nhất
def dijkstra(graph, start):
    # Khởi tạo khoảng cách và predecessor
    distances = {vertex: float('inf') for vertex in graph}
    predecessor = {vertex: None for vertex in graph}
    distances[start] = 0

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

        visited.add(current_vertex)
        print(f"Đã thăm đỉnh: {current_vertex}")

        # Cập nhật khoảng cách và predecessor
        for neighbor, weight in graph[current_vertex].items():
            if neighbor not in visited and distances[current_vertex] + weight < distances[neighbor]:
                print(f"Cập nhật khoảng cách từ {current_vertex} đến {neighbor} với trọng số {weight}.")
                print(f"Trước cập nhật: distance[{neighbor}] = {distances[neighbor]}")
                distances[neighbor] = distances[current_vertex] + weight
                predecessor[neighbor] = current_vertex
                print(f"Sau cập nhật: distance[{neighbor}] = {distances[neighbor]}")
        
        print(f"Tình trạng khoảng cách sau vòng lặp: {distances}")

    print("\nThuật toán Dijkstra hoàn thành.")
    return distances, predecessor


# Hàm in đường đi từ đỉnh nguồn đến đỉnh đích
def print_path(predecessor, source, target):
    path = []
    current = target
    while current is not None:
        path.append(current)
        if current == source:
            break
        current = predecessor[current]

    if current is None:
        return "Không có đường đi."
    else:
        path.reverse()
        return " -> ".join(map(str, path))


# Giao diện chính và đọc file từ file chọn
def main():
    root = tk.Tk()
    root.withdraw()  # Ẩn giao diện chính của Tkinter
    file_path = filedialog.askopenfilename(title="Chọn file TXT đầu vào", filetypes=[("Text files", "*.txt")])

    if not file_path:
        print("Không chọn file. Thoát chương trình.")
        return

    # Đọc dữ liệu từ file đã chọn
    graph = read_graph_from_file(file_path)

    try:
        start_vertex = int(input("Nhập đỉnh nguồn: "))
        if start_vertex not in graph:
            print("Đỉnh nguồn không hợp lệ.")
            return

        # Ghi nhận thời gian bắt đầu
        start_time = time.time()

        # Chạy thuật toán Dijkstra
        distances, predecessor = dijkstra(graph, start_vertex)

        # Ghi nhận thời gian kết thúc
        end_time = time.time()

        # Hiển thị kết quả
        print(f"\nKhoảng cách từ đỉnh {start_vertex} đến các đỉnh khác:")
        for vertex, distance in distances.items():
            if distance != float('inf'):
                path = print_path(predecessor, start_vertex, vertex)
                print(f"Đỉnh {vertex}: {distance}, Đường đi: {path}")
            else:
                print(f"Đỉnh {vertex}: Không thể tới")

        # Hiển thị thời gian thực thi
        print(f"Thời gian xử lý: {end_time - start_time:.6f} giây")

    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")


if __name__ == "__main__":
    main()
