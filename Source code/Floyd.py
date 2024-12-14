import tkinter as tk
from tkinter import filedialog
import time  # Thêm time để tính thời gian


# Hàm đọc dữ liệu từ file TXT
def read_graph_from_file(file_path):
    graph = []
    with open(file_path, 'r') as file:
        for line in file:
            # Dùng thay thế dấu ',' hoặc khoảng trắng và đọc dữ liệu
            row = [float(x.strip()) if x.strip() and x.strip().lower() != 'inf' else float('inf') for x in line.replace(',', ' ').split()]
            graph.append(row)
    return graph


# Hàm Floyd-Warshall để tìm đường đi ngắn nhất và phát hiện chu trình âm
def floyd(graph, num_vertices):
    # Sao chép ma trận trọng số
    dist = [[float('inf')] * num_vertices for _ in range(num_vertices)]

    for i in range(num_vertices):
        for j in range(num_vertices):
            if i == j:
                dist[i][j] = 0
            elif graph[i][j] != float('inf'):
                dist[i][j] = graph[i][j]

    # In ma trận trọng số ban đầu
    print("\nMa trận trọng số ban đầu:")
    for row in dist:
        print([float('inf') if x == float('inf') else int(x) for x in row])
    print("\nBắt đầu tính toán Floyd-Warshall...\n")

    # Duyệt qua mỗi đỉnh k và thử cập nhật đường đi ngắn nhất
    for k in range(num_vertices):
        print(f"Vòng lặp k = {k}:\n")
        for i in range(num_vertices):
            for j in range(num_vertices):
                # Tránh cập nhật khi không thể đi tới
                if dist[i][k] != float('inf') and dist[k][j] != float('inf'):
                    if dist[i][j] > dist[i][k] + dist[k][j]:
                        print(f"Cập nhật khoảng cách từ dist[{i}][{j}] = {dist[i][j]} thành dist[{i}][{k}] + dist[{k}][{j}] = {dist[i][k]} + {dist[k][j]} = {dist[i][k] + dist[k][j]}")
                        dist[i][j] = dist[i][k] + dist[k][j]

        # In thông tin ma trận sau mỗi vòng lặp
        print(f"Ma trận sau vòng lặp k = {k}:")
        for row in dist:
            print([float('inf') if x == float('inf') else int(x) for x in row])
        print("\n")

    # Kiểm tra chu trình âm
    for i in range(num_vertices):
        if dist[i][i] < 0:
            # Nếu phát hiện chu trình âm
            print("Phát hiện chu trình âm trong đồ thị!")
            return dist, True

    # Không phát hiện chu trình âm
    print("Không phát hiện chu trình âm trong đồ thị.")
    return dist, False


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

    # Thêm tính năng tính thời gian
    start_time = time.time()  # Thời điểm trước khi thuật toán chạy

    # Thêm thuật toán Floyd-Warshall và gọi hàm chính
    num_vertices = len(graph)
    result, has_negative_cycle = floyd(graph, num_vertices)

    end_time = time.time()  # Thời điểm sau khi thuật toán hoàn thành

    if has_negative_cycle:
        print("\nPhát hiện chu trình âm trong đồ thị.")
    else:
        print("\nKhông phát hiện chu trình âm trong đồ thị.")

    print("\nMa trận khoảng cách ngắn nhất giữa các đỉnh (inf biểu thị không thể tới):")
    for row in result:
        # Hiển thị thông tin mà không chuyển 'inf' thành 0
        print([float('inf') if x == float('inf') else int(x) for x in row])

    # Hiển thị thời gian thực thi
    print(f"\nThời gian xử lý: {end_time - start_time:.6f} giây")


if __name__ == "__main__":
    main()
