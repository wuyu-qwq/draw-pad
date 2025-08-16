from tkinter import *
from tkinter.colorchooser import askcolor
from tkinter import filedialog, messagebox
import PIL.ImageGrab as ImageGrab

class PaintApp:
    # 常量定义
    PIXEL_TAG = "pixel"
    GRID_TAG = "pixel_grid"
    
    def __init__(self, root, grid_width=64, grid_height=48):
        self.root = root
        self.root.title("Python画板")
        self.root.geometry("800x600")
        self.root.configure(background="white")
        # 默认画笔颜色和大小
        self.pen_color = "black"
        self.eraser_color = "white"
        self.pen_size = 1  # 修改默认值为1，表示1个像素单位
        # 像素网格设置
        self.pixel_grid_enabled = False
        self.grid_width = grid_width  # 固定网格宽度
        self.grid_height = grid_height  # 固定网格高度
        self.pixel_size = 10  # 每个像素方格的大小
        self.grid_lines = []
        # 橡皮擦模式
        self.is_eraser_mode = False
        
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
        # 像素网格控制按钮
        Button(button_frame, text="显示/隐藏像素网格", command=self.toggle_pixel_grid).pack(side=LEFT, padx=10)

        # 笔墨粗细滑块 (修改范围以适配像素网格)
        Label(button_frame, text="笔墨粗细:").pack(side=LEFT, padx=10)
        self.size_scale = Scale(button_frame, from_=1, to=5, orient=HORIZONTAL, command=self.change_pen_size)
        self.size_scale.set(self.pen_size)
        self.size_scale.pack(side=LEFT, padx=10)
        
        # 创建画布
        self.canvas = Canvas(main_frame, bg="white")
        self.canvas.pack(fill=BOTH, expand=True)
        
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<Button-1>", self.paint)
        self.canvas.bind("<Configure>", self.on_canvas_resize)
        
    def paint(self, event):
        # 保存当前颜色
        original_color = self.pen_color
        
        # 如果是橡皮擦模式，使用橡皮擦颜色
        if self.is_eraser_mode:
            self.pen_color = self.eraser_color
        
        # 计算像素网格中的位置
        center_x = event.x // self.pixel_size
        center_y = event.y // self.pixel_size
        
        # 根据笔墨粗细绘制多个像素
        radius = self.pen_size // 2
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                x = center_x + dx
                y = center_y + dy
                
                # 检查边界
                if self._is_within_bounds(x, y):
                    # 计算屏幕坐标
                    screen_x = x * self.pixel_size
                    screen_y = y * self.pixel_size
                    
                    # 删除该区域内的像素项或绘制新像素
                    if self.is_eraser_mode:
                        self._erase_pixel_at(screen_x, screen_y)
                    else:
                        self._draw_pixel(screen_x, screen_y, self.pen_color)
        
        # 恢复原来的颜色
        self.pen_color = original_color
        
    def _is_within_bounds(self, x, y):
        """检查坐标是否在网格范围内"""
        return 0 <= x < self.grid_width and 0 <= y < self.grid_height
    
    def _erase_pixel_at(self, screen_x, screen_y):
        """在指定位置擦除像素"""
        items = self.canvas.find_overlapping(screen_x, screen_y, 
                                            screen_x + self.pixel_size, 
                                            screen_y + self.pixel_size)
        for item in items:
            if self.PIXEL_TAG in self.canvas.gettags(item):
                self.canvas.delete(item)
                
    def _draw_pixel(self, screen_x, screen_y, color):
        """在指定位置绘制像素"""
        self.canvas.create_rectangle(
            screen_x, screen_y, 
            screen_x + self.pixel_size, screen_y + self.pixel_size,
            fill=color, outline=color, tags=self.PIXEL_TAG
        )
        
    def _get_current_drawing_color(self):
        """获取当前绘制颜色"""
        return self.eraser_color if self.is_eraser_mode else self.pen_color
        
    def choose_color(self):
        color = askcolor()[1]
        if color:
            self.pen_color = color
            
    def change_pen_size(self, val):
        self.pen_size = int(val)
        
    def use_eraser(self):
        self.is_eraser_mode = not self.is_eraser_mode
        if self.is_eraser_mode:
            print("切换到橡皮擦模式")
        else:
            print("切换到画笔模式")
        
    def clear_canvas(self):
        self.canvas.delete("all")
        # 重新绘制像素网格
        if self.pixel_grid_enabled:
            self.draw_pixel_grid()
            
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

    def on_canvas_resize(self, event):
        # 当画布大小改变时重新计算像素大小并绘制像素网格
        self.calculate_pixel_size()
        if self.pixel_grid_enabled:
            self.draw_pixel_grid()
            
    def calculate_pixel_size(self):
        # 根据画布大小和网格数量计算每个像素的大小
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        # 计算每个像素的大小，取较小值以确保整个网格都能显示
        if self.grid_width > 0 and self.grid_height > 0:
            pixel_width = canvas_width // self.grid_width
            pixel_height = canvas_height // self.grid_height
            self.pixel_size = min(pixel_width, pixel_height)
            # 确保像素大小至少为1
            self.pixel_size = max(1, self.pixel_size)
            
    def toggle_pixel_grid(self):
        self.pixel_grid_enabled = not self.pixel_grid_enabled
        if self.pixel_grid_enabled:
            self.calculate_pixel_size()
            self.draw_pixel_grid()
        else:
            self.clear_pixel_grid()
            
    def draw_pixel_grid(self):
        # 清除现有的网格线
        self.clear_pixel_grid()
        
        # 重新计算像素大小
        self.calculate_pixel_size()
        
        # 获取画布尺寸
        width = self.grid_width * self.pixel_size
        height = self.grid_height * self.pixel_size
        
        # 绘制垂直线
        for x in range(0, width + 1, self.pixel_size):
            line = self.canvas.create_line(x, 0, x, height, fill="#e0e0e0", tags=self.GRID_TAG)
            self.grid_lines.append(line)
            
        # 绘制水平线
        for y in range(0, height + 1, self.pixel_size):
            line = self.canvas.create_line(0, y, width, y, fill="#e0e0e0", tags=self.GRID_TAG)
            self.grid_lines.append(line)
            
        # 确保网格线在最底层，像素在最上层
        for line in self.grid_lines:
            self.canvas.tag_lower(line)
        self.canvas.tag_raise(self.PIXEL_TAG)
            
    def clear_pixel_grid(self):
        # 删除所有网格线
        self.canvas.delete(self.GRID_TAG)
        self.grid_lines = []
        
    def get_pixel(self, x, y):
        """
        获取像素网格中指定位置的颜色值
        x, y: 像素坐标（不是屏幕坐标）
        返回: RGB颜色元组
        """
        # 检查边界
        if not self._is_within_bounds(x, y):
            return (255, 255, 255)  # 超出边界返回白色
            
        # 将像素坐标转换为屏幕坐标（像素网格的左上角坐标）
        screen_x = x * self.pixel_size
        screen_y = y * self.pixel_size
        
        # 查找在指定点上的所有项目
        # 使用像素中心点来检测颜色
        center_x = screen_x + self.pixel_size // 2
        center_y = screen_y + self.pixel_size // 2
        items = self.canvas.find_overlapping(center_x, center_y, center_x, center_y)
        
        color = None
        
        if items:
            # 从最上层项目开始查找有颜色的项目
            for item in reversed(items):
                # 检查是否是像素块（通过tag）
                if self.PIXEL_TAG in self.canvas.gettags(item):
                    try:
                        # 获取项目的填充颜色
                        fill_color = self.canvas.itemcget(item, "fill")
                        if fill_color and fill_color != "":
                            color = fill_color
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
        
        # 默认返回白色（画布背景色）
        return (255, 255, 255)
    
    def get_pixels(self):
        """
        获取整个像素网格的颜色数据
        返回: 二维列表，每个元素是RGB颜色元组
        """
        # 创建二维列表存储像素值
        pixels = []
        
        # 遍历每个像素点
        for y in range(self.grid_height):
            row = []
            for x in range(self.grid_width):
                # 使用get_pixel方法获取每个像素的颜色
                color = self.get_pixel(x, y)
                row.append(color)
            pixels.append(row)
        
        return pixels

    def set_pixel(self, color, position):
        """
        设置像素网格中指定位置的颜色
        
        参数:
        color: RGB元组，如 (255, 0, 0) 表示红色
        position: 坐标元组，如 (x, y) 表示像素位置
        """
        # 解析颜色和位置参数
        r, g, b = color
        x, y = position
        
        # 检查边界
        if self._is_within_bounds(x, y):
            # 计算屏幕坐标
            screen_x = x * self.pixel_size
            screen_y = y * self.pixel_size
            
            # 将RGB转换为十六进制颜色值
            hex_color = f"#{r:02x}{g:02x}{b:02x}"
            
            # 在像素网格位置绘制方块
            self._draw_pixel(screen_x, screen_y, hex_color)

    def set_canvas(self, pixel_data):
        """
        将二维RGB数据绘制到画布上
        
        参数:
        pixel_data: 二维列表，每个元素是RGB颜色元组，如 [(255, 0, 0), (0, 255, 0), ...]
        """
        # 清除现有的像素内容
        self.canvas.delete(self.PIXEL_TAG)
        
        # 检查输入数据的维度
        if not pixel_data or not pixel_data[0]:
            return
        
        # 获取数据维度
        data_height = len(pixel_data)
        data_width = len(pixel_data[0])
        
        # 确保不超过画布网格范围
        height = min(data_height, self.grid_height)
        width = min(data_width, self.grid_width)
        
        # 遍历像素数据并绘制
        for y in range(height):
            for x in range(width):
                # 获取RGB值
                r, g, b = pixel_data[y][x]
                
                # 检查边界
                if self._is_within_bounds(x, y):
                    # 计算屏幕坐标
                    screen_x = x * self.pixel_size
                    screen_y = y * self.pixel_size
                    
                    # 将RGB转换为十六进制颜色值
                    hex_color = f"#{r:02x}{g:02x}{b:02x}"
                    
                    # 在像素网格位置绘制方块
                    self._draw_pixel(screen_x, screen_y, hex_color)
        
        # 确保像素在最上层显示
        self.canvas.tag_raise(self.PIXEL_TAG)

if __name__ == "__main__":
    root = Tk()
    # 可以在这里指定网格的宽高，例如 64x48
    app = PaintApp(root, grid_width=100, grid_height=100)
    root.mainloop()