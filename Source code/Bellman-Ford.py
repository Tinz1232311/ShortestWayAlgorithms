import tkinter as tk
from tkinter import filedialog
import time


def read_edges_from_file(file_path):
    edges = []
    with open(file_path, 'r') as file:
        for i, line in enumerate(file):
            row = [float(x.strip()) if x.strip().lower() != 'inf' else float('inf') for x in line.replace(',', ' ').split()]
            for j, weight in enumerate(row):
                if weight != float('inf') and weight != 0:
                    edges.append((i, j, weight))
    return edges


def bellman_ford(vertices, edges, source):
    # Khởi tạo khoảng cách và predecessor
    distance = {v: float('inf') for v in vertices}
    predecessor = {v: None for v in vertices}
    distance[source] = 0

    print(f"Ban đầu, khoảng cách: {distance}")

    # Thực hiện thuật toán Bellman-Ford
    for i in range(len(vertices) - 1):
        print(f"\nVòng lặp {i + 1}:")
        for u, v, w in edges:
            if distance[u] + w < distance[v]:  # Cập nhật khoảng cách nếu có cải thiện
                print(f"Cập nhật khoảng cách từ {u} đến {v} với trọng số {w}.")
                print(f"Trước cập nhật: distance[{v}] = {distance[v]}")
                distance[v] = distance[u] + w
                predecessor[v] = u  # Cập nhật đỉnh trước đó
                print(f"Sau cập nhật: distance[{v}] = {distance[v]}")
        
        print(f"Tình trạng khoảng cách sau vòng lặp {i + 1}: {distance}")

    # Kiểm tra chu trình âm
    print("\nKiểm tra chu trình âm...")
    for u, v, w in edges:
        if distance[u] + w < distance[v]:
            print(f"Phát hiện chu trình âm qua cạnh ({u}, {v}, {w})")
            return False, distance, predecessor

    print("Không phát hiện chu trình âm.")
    return True, distance, predecessor


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


def main():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Chọn file TXT đầu vào", filetypes=[("Text files", "*.txt")])

    if not file_path:
        print("Không chọn file. Thoát chương trình.")
        return

    start_time = time.time()
    edges = read_edges_from_file(file_path)

    vertices = set()
    for u, v, _ in edges:
        vertices.add(u)
        vertices.add(v)
    max_vertex = max(vertices)
    for i in range(max_vertex + 1):
        vertices.add(i)
    vertices = list(vertices)

    try:
        start_vertex = int(input(f"Nhập đỉnh nguồn (các đỉnh hợp lệ: {vertices}): "))
    except ValueError:
        print("Nhập không hợp lệ.")
        return

    if start_vertex not in vertices:
        print("Đỉnh nguồn không hợp lệ.")
        return

    result, distances, predecessor = bellman_ford(vertices, edges, start_vertex)

    end_time = time.time()
    elapsed_time = end_time - start_time

    if result:
        print("Không phát hiện chu trình âm.")
    else:
        print("Phát hiện chu trình âm!")

    print("Khoảng cách và đường đi từ đỉnh nguồn đến các đỉnh:")
    for vertex in vertices:
        if distances[vertex] != float('inf'):
            path = print_path(predecessor, start_vertex, vertex)
            print(f"Đỉnh {vertex}: {int(distances[vertex])}, Đường đi: {path}")
        else:
            print(f"Đỉnh {vertex}: Không thể tới")

    print(f"Thời gian thực thi: {elapsed_time:.6f} giây")


if __name__ == "__main__":
    main()
