# Quaternion Visualizer

Program visualisasi 3D interaktif untuk memahami konsep quaternion dan rotasi objek dalam ruang tiga dimensi menggunakan PyQt5 dan OpenGL.

## 📋 Deskripsi Program & Fitur Program

### Deskripsi
Quaternion Visualizer adalah aplikasi desktop yang memungkinkan pengguna untuk:
- Memuat objek 3D dalam format .obj
- Menerapkan rotasi menggunakan quaternion dengan sumbu dan sudut yang dapat dikustomisasi
- Memvisualisasikan objek asli dan objek yang telah dirotasi secara bersamaan
- Mengontrol tampilan dengan berbagai opsi visualisasi
- Memahami konsep matematika quaternion melalui representasi visual

### Fitur Utama
- **📁 File Operations**: Memuat objek 3D format .obj dengan informasi vertex dan face count
- **🔄 Quaternion Rotation**: 
  - Input sumbu rotasi (X, Y, Z) dengan presisi tinggi
  - Kontrol sudut rotasi dalam derajat (-360° hingga 360°)
  - Penerapan rotasi real-time menggunakan quaternion
- **👁️ Visualization Options**:
  - Toggle tampilan objek asli dan objek yang dirotasi
  - Tampilan sumbu koordinat XYZ
  - Visualisasi sumbu rotasi
  - Label sudut rotasi
- **🎮 View Controls**:
  - Mouse drag untuk rotasi kamera
  - Mouse wheel untuk zoom in/out
  - Reset view ke posisi default
- **📊 Real-time Feedback**: Status bar dengan informasi operasi dan error handling

## 🛠️ Teknologi dan Framework

### Bahasa Pemrograman
- **Python 3.13**: Bahasa pemrograman utama

### Framework dan Library
- **PyQt5 5.15.11**: Framework GUI untuk interface pengguna
  - `QtWidgets`: Komponen GUI (window, button, layout, dll)
  - `QtOpenGL`: Integrasi OpenGL dengan Qt
  - `QtCore`: Functionality inti Qt
- **PyOpenGL 3.1.9**: Binding Python untuk OpenGL rendering
- **NumPy 2.3.1**: Komputasi numerik dan operasi array
- **Trimesh 4.7.1**: Library untuk manipulasi dan loading mesh 3D
- **Pillow 11.3.0**: Image processing library (dependency)

### Arsitektur Program
```
├── main.py                 # Entry point aplikasi
├── gui/                    # Modul interface pengguna
│   ├── main_window.py      # Main window dengan control panel
│   └── opengl_widget.py    # OpenGL rendering widget
├── math3d/                 # Modul matematika 3D
│   ├── quaternion.py       # Implementasi kelas Quaternion
│   └── vector3d.py         # Implementasi kelas Vector3D
├── graphics/               # Modul rendering graphics
    └── mesh_object.py      # Kelas untuk handling mesh 3D
```

## 🧮 Penjelasan Quaternion dan Kegunaannya

### Apa itu Quaternion?
Quaternion adalah sistem bilangan yang memperluas bilangan kompleks, ditemukan oleh William Rowan Hamilton pada tahun 1843. Quaternion terdiri dari satu komponen real (scalar) dan tiga komponen imaginer (vector).

**Representasi matematica:**
```
q = w + xi + yj + zk
```
Dimana:
- `w` = komponen real (scalar)
- `x, y, z` = komponen imaginer (vector)
- `i, j, k` = unit quaternion dengan sifat: i² = j² = k² = ijk = -1

### Quaternion untuk Rotasi 3D
Dalam program ini, quaternion digunakan untuk merepresentasikan rotasi 3D dengan keunggulan:

1. **Bebas Gimbal Lock**: Tidak seperti Euler angles, quaternion tidak mengalami gimbal lock
2. **Interpolasi Smooth**: Memungkinkan interpolasi rotasi yang halus
3. **Komputasi Efisien**: Lebih efisien daripada matrix rotasi untuk komposisi rotasi
4. **Representasi Kompak**: Hanya membutuhkan 4 komponen vs 9 komponen matrix

### Formula Rotasi dengan Quaternion
Untuk merotasi vector `v` dengan quaternion `q`:
```
v' = q * v * q⁻¹
```

Dimana:
- `v'` = vector hasil rotasi
- `q` = quaternion rotasi
- `q⁻¹` = konjugat quaternion

### Implementasi dalam Program
```python
class Quaternion:
    def rotate(self, vector: Vector3D):
        q_vector = Quaternion(0, vector)
        rotated_vector = self * q_vector * self.conjugate()
        result = Vector3D(rotated_vector.x, rotated_vector.y, rotated_vector.z)
        return result
```

### Kegunaan Quaternion dalam Aplikasi
- **Game Development**: Rotasi karakter, kamera, dan objek
- **Robotics**: Kontrol orientasi robot dan manipulator
- **Computer Graphics**: Animasi 3D dan rendering
- **Aerospace**: Navigasi pesawat dan satelit
- **VR/AR**: Tracking orientasi headset dan controller

## 📸 Screenshot Hasil Percobaan

![Hasil percobaan](images/Screenshot%202025-07-21%20at%2020.50.02.png)
![Hasil percobaan tanpa objek original](images/Screenshot%202025-07-21%20at%2020.50.08.png)

## 🚀 Cara Menjalankan Program

### Prasyarat Sistem
- **Operating System**: macOS, Windows, atau Linux
- **Python**: Version 3.8 atau lebih baru
- **OpenGL**: Support OpenGL (biasanya sudah ada di sistem modern)

### Langkah Instalasi

1. **Clone atau Download Repository**
   ```bash
   git clone <repository-url>
   cd Quaternion-Visualizer
   ```

2. **Buat Virtual Environment (Recommended)**
   ```bash
   python3 -m venv env
   source env/bin/activate  # macOS/Linux
   # atau
   env\Scripts\activate     # Windows
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

   **Manual installation jika diperlukan:**
   ```bash
   pip install PyQt5==5.15.11
   pip install PyOpenGL==3.1.9
   pip install numpy==2.3.1
   pip install trimesh==4.7.1
   pip install pillow==11.3.0
   ```

4. **Verifikasi Instalasi**
   ```bash
   python -c "import PyQt5; import OpenGL; print('Dependencies installed successfully')"
   ```

### Menjalankan Aplikasi

```bash
python main.py
```

### Cara Penggunaan

1. **Load Objek 3D**:
   - Klik tombol "Load 3D Object (.obj)"
   - Pilih file .obj dari dialog (gunakan sample di folder `obj/`)
   - Informasi objek akan ditampilkan di panel

2. **Mengatur Rotasi**:
   - Masukkan sumbu rotasi (X, Y, Z) - contoh: (1, 0, 0) untuk rotasi di sumbu X
   - Atur sudut rotasi dalam derajat
   - Klik "Apply Rotation" untuk menerapkan

3. **Kontrol Visualisasi**:
   - Gunakan checkbox untuk toggle tampilan berbagai elemen
   - Drag kiri mouse untuk rotasi kamera
   - Scroll wheel untuk zoom in/out
   - Klik "Reset View" untuk kembali ke posisi default

4. **Tips Penggunaan**:
   - Sumbu rotasi akan dinormalisasi otomatis
   - Gunakan nilai sumbu yang tidak nol semua
   - Experiment dengan berbagai sumbu dan sudut untuk memahami quaternion

## 📚 Referensi

### Dokumentasi Teknis
1. **PyQt5 Documentation**: https://doc.qt.io/qtforpython/
2. **OpenGL Programming Guide**: https://www.opengl.org/documentation/
3. **NumPy User Guide**: https://numpy.org/doc/stable/user/
4. **Trimesh Documentation**: https://trimsh.org/

### Quaternion dan Matematika 3D
1. **Aljabar Quaternion (bagian 1)** - Rinaldi Munir: https://informatika.stei.itb.ac.id/~rinaldi.munir/AljabarGeometri/2023-2024/Algeo-25-Aljabar-Quaternion-Bagian1-2023.pdf
2. **Aljabar Quaternion (bagian 2)** - Rinaldi Munir: https://informatika.stei.itb.ac.id/~rinaldi.munir/AljabarGeometri/2023-2024/Algeo-26-Aljabar-Quaternion-Bagian2-2023.pdf

## Pembuat
**Sakti Bimasena - 13523053**