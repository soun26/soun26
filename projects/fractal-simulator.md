[← Soun](https://github.com/tienleeee)

# FDUT · Fractal 5 Pro Simulator

**Focus:** desktop visualization of 3/3+2-axis FDM printing.

**Status:** working desktop prototype. [Public source repository →](https://github.com/tienleeee/fdut-fractal-simulator)

A Python application for studying a Fractal 5 Pro printing workflow without a
physical machine. The FDUT GUI uses Fractal Cortex for slicing and adds offline
motion playback and an interactive machine view.

## Features

- Load STL and G-code, play/pause and seek through a print.
- Visualize XYZ motion and the rotating/tilting A/B table.
- Slice in three axes or multiple print orientations with Cortex.
- Navigate the 3D scene with OpenGL, pointer-centered zoom and stable orbit controls.
- Switch between Vietnamese/English and light/dark appearance.

## Engineering scope

The machine view uses illustrative geometry and ideal kinematics. It does not
perform full-machine collision checking, thermal simulation or material simulation.

Fractal Cortex and Fractal 5 Pro are original projects by
[Fractal Robotics](https://github.com/fractalrobotics). The FDUT interface is an
additional desktop layer.

**Tools:** Python · NumPy · PySide6 · OpenGL · STL · G-code.

<details>
<summary>Tiếng Việt</summary>

Ứng dụng Python để học và quan sát quá trình in 3/3+2 trục mà chưa cần máy thật.
GUI FDUT bổ sung phát lại chuyển động, điều khiển vùng 3D và chuyển Việt/Anh,
sáng/tối. Vùng 3D dùng hình học minh họa và động học lý tưởng;
chưa kiểm tra va chạm toàn máy hoặc mô phỏng nhiệt/cơ học nhựa.

</details>
