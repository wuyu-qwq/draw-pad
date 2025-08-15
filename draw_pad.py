from tkinter import *
from tkinter.colorchooser import askcolor
from tkinter import filedialog, messagebox
import PIL.ImageGrab as ImageGrab

class PaintApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python画板")
        self.root.geometry("800x600")
        self.root.configure(background="white")
        # 默认画笔颜色和大小
        self.pen_color = "black"
        self.eraser_color = "white"
        self.pen_size = 5
        # 创建主框架
        main_frame = Frame(self.root, bg="white")
        main_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        # 创建按钮框架并放在顶部
        button_frame = Frame(main_frame, bg="white")
        button_frame.pack(fill=X, pady=(0, 10))
        
        # 工具按钮
        Button(button_frame, text="选择颜色", command=self.choose_color).pack(side=LEFT, padx=10)
        Button(button_frame, text="橡皮擦", command=self.use_eraser).pack(side=LEFT, padx=10)
        Button(button_frame, text="清屏", command=self.clear_canvas).pack(side=LEFT, padx=10)
        Button(button_frame, text="保存", command=self.save_canvas).pack(side=LEFT, padx=10)

        # 笔墨粗细滑块
        Label(button_frame, text="笔墨粗细:").pack(side=LEFT, padx=10)
        self.size_scale = Scale(button_frame, from_=1, to=20, orient=HORIZONTAL, command=self.change_pen_size)
        self.size_scale.set(self.pen_size)
        self.size_scale.pack(side=LEFT, padx=10)
        
        # 创建画布
        self.canvas = Canvas(main_frame, bg="white")
        self.canvas.pack(fill=BOTH, expand=True)
        
        self.canvas.bind("<B1-Motion>", self.paint)
    def paint(self, event):
        x1, y1 = (event.x - self.pen_size), (event.y - self.pen_size)
        x2, y2 = (event.x + self.pen_size), (event.y + self.pen_size)
        self.canvas.create_oval(x1, y1, x2, y2, fill=self.pen_color, outline=self.pen_color)
    def choose_color(self):
        color = askcolor()[1]
        if color:
            self.pen_color = color
    def change_pen_size(self, val):
        self.pen_size = int(val)
    def use_eraser(self):
        self.pen_color = self.eraser_color
    def clear_canvas(self):
        self.canvas.delete("all")
    def save_canvas(self):
        try:
            file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                        filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
            if file_path:
                x = self.root.winfo_rootx() + self.canvas.winfo_x()
                y = self.root.winfo_rooty() + self.canvas.winfo_y()
                x1 = x + self.canvas.winfo_width()
                y1 = y + self.canvas.winfo_height()
                ImageGrab.grab().crop((x, y, x1, y1)).save(file_path)
                messagebox.showinfo("保存成功", f"文件已保存到 {file_path}")
        except Exception as e:
            messagebox.showerror("错误", f"保存失败: {e}")

    def get_pixel(self, x, y): # 拿到某个点的像素值
        # 查找在指定点上的所有项目
        items = self.canvas.find_overlapping(x, y, x, y)
        
        color = None
        
        if items:
            # 从最上层项目开始查找有颜色的项目
            for item in reversed(items):
                try:
                    # 尝试获取项目的填充颜色
                    fill_color = self.canvas.itemcget(item, "fill")
                    if fill_color and fill_color != "":
                        color = fill_color
                        break
                except:
                    pass
                
                # 尝试获取轮廓颜色
                try:
                    outline_color = self.canvas.itemcget(item, "outline")
                    if outline_color and outline_color != "":
                        color = outline_color
                        break
                except:
                    pass
        
        # 如果没有找到任何颜色，使用画布背景色
        if not color:
            color = self.canvas.cget("bg")
        
        # 处理颜色名称（如"white", "black"等）
        color_names = {
            'white': (255, 255, 255),
            'black': (0, 0, 0),
            'red': (255, 0, 0),
            'green': (0, 255, 0),
            'blue': (0, 0, 255),
            # 可以根据需要添加更多颜色名称
        }
        
        if color in color_names:
            return color_names[color]
        
        # 处理十六进制颜色值
        hex_color = color
        if hex_color.startswith('#'):
            hex_color = hex_color[1:]
        
        # 处理3位十六进制颜色值（如#FFF）
        if len(hex_color) == 3:
            hex_color = ''.join([c*2 for c in hex_color])
        
        # 转换为RGB元组
        if len(hex_color) == 6:
            try:
                r = int(hex_color[0:2], 16)
                g = int(hex_color[2:4], 16)
                b = int(hex_color[4:6], 16)
                return (r, g, b)
            except ValueError:
                pass
        
        # 默认返回黑色
        return (0, 0, 0)
    
    def get_pixels(self):
        # 获取画布的宽度和高度
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        
        # 创建二维列表存储像素值
        pixels = []
        
        # 遍历每个像素点
        for y in range(height):
            row = []
            for x in range(width):
                # 使用现有的get_pixel方法获取每个像素的颜色
                color = self.get_pixel(x, y)
                row.append(color)
            pixels.append(row)
        
        return pixels

if __name__ == "__main__":
    root = Tk()
    app = PaintApp(root)
    root.mainloop()