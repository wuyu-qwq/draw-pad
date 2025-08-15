# python画板

## 介绍

本项目是一个使用tkinter构建的简易画板

## 快速开始

### 1、导入程序依赖包

PS：用不到的包其实可以不导入，但为了避免出错，还是建议全部导入。

```python
from tkinter import * # 用于显示主窗口（必导）
from tkinter.colorchooser import askcolor # 用于颜色选择功能
from tkinter import filedialog, messagebox # 用于文件保存功能
import PIL.ImageGrab as ImageGrab # 用于保存画板图片
```

### 2、创建tk窗口对象和画板对象

```python
root = Tk()
app = PaintApp(root)
```

上述代码中的app是画板对象，对画板的操作都基于这个对象进行。

## 函数说明

### use_eraser()
 
切换到橡皮擦模式

### clear_canvas()

清除画布上的所有内容

### change_pen_size(val)

改变画笔大小为val

### change_pen_color()

改变画笔颜色（弹出窗口）

### save_canvas()

保存画布（弹出窗口）

### get_pixel(x, y)

获取画布上(x, y)点的像素颜色

### get_pixels()

获取画布上所有像素颜色

### set_pixel((r,g,b), (x,y))

设置画布上(x, y)点的像素颜色为(r, g, b)