import random
import threading

SPEED = 10
RESET = False

def rand_color():
    return "#" + ''.join([random.choice('ABCDEF0123456789') for _ in range(6)])

class Disk():
    def __init__(self, canvas, tower, n):
        self.number = n
        self.canvas = canvas
        self.length = 150 - 3*(30 - n)
        self.x = tower.get_x() + tower.get_width()/2 - self.length/2
        self.y = tower.get_y() + tower.get_height() - 16*len(tower.show())
        self.disk = self.canvas.create_rectangle(self.x, self.y, self.x+self.length, self.y-16, fill=rand_color(), outline="black", tag="disk_tag")
        self.label = self.canvas.create_text(self.x + self.length/2, self.y-8, text=str(n), fill='black', tag="disk_tag")
        self.tower = tower
        tower.push(self)

    def __repr__(self):
        return f"{self.number}"
    
    def __str__(self):
        return f"{self.number}"

    def get(self):
        return self.disk
    
    def move(self, tower):
        new_x = tower.get_x() + tower.get_width()/2 - self.length/2
        new_y = tower.get_y() + tower.get_height() - 16*len(tower.show())
        if RESET:
            return False
        # print(f"moving disk {self.number}")
        while self.y > self.tower.get_top():
            if RESET:
                return False
            spd = SPEED
            self.y -= spd
            self.canvas.move(self.disk, 0, -spd)
            self.canvas.move(self.label, 0, -spd)
            self.canvas.update()
        
        if tower.get_x() > self.x:
            while self.x < new_x:
                if RESET:
                    return False
                spd = SPEED
                if self.x + spd > new_x:
                    spd = new_x - self.x
                self.x += spd
                self.canvas.move(self.disk, spd, 0)
                self.canvas.move(self.label, spd, 0)
                self.canvas.update()
        
        elif tower.get_x() < self.x:
            spd = SPEED
            if RESET:
                return False
            while self.x > new_x:
                if self.x - spd < new_x:
                    spd = self.x - new_x
                self.x -= spd
                self.canvas.move(self.disk, -spd, 0)
                self.canvas.move(self.label, -spd, 0)
                self.canvas.update()
        
        while self.y < new_y:
            if RESET:
                return False
            spd = SPEED
            if self.y + spd > new_y:
                spd = new_y - self.y
            self.y += spd
            self.canvas.move(self.disk, 0, spd)
            self.canvas.move(self.label, 0, spd)
            self.canvas.update()

    
class Tower():
    def __init__(self, canvas, x, y, width, height, name):
        self.name = str(name)
        self.x, self.y = x, y
        self.disks = list()
        self.canvas = canvas
        self.width = width
        self.height = height
        self.tower = self.canvas.create_rectangle(x, y, x+width, y+height, fill='#384f94', outline='#384f94')
        self.label = self.canvas.create_text(self.x + self.width/2, self.y + height + 18, text=self.name, font=('Helvetica', 20), fill='#384f94')
        # print(f"Tower created at {x}, {y}, {x+width}, {y+height}")

    def __repr__(self) -> str:
        return self.name

    def __str__(self) -> str:
        return self.name

    def push(self, disk: Disk):
        # print(f"Disk No. {disk} was added to tower {self.name}")
        self.disks.append(disk)

    def pop(self):
        return self.disks.pop()
    
    def clear(self):
        self.disks.clear()

    def show(self):
        return self.disks

    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
    
    def get_width(self):
        return self.width
    
    def get_height(self):
        return self.height
    
    def get_top(self):
        disks_height =  self.y + self.height - 16*len(self.disks)
        return disks_height if disks_height < self.y else self.y


class Move(threading.Thread):
    def __init__(self):
        super(Move, self).__init__()
        self.__flag = threading.Event()
        self.__flag.set()
        self.__running = threading.Event()
        self.__running.set()
        self.__ready = threading.Event()
        self.__ready.clear()
    
    def run(self, origin: Tower, dest: Tower):
        self.__flag.wait()
        self.__ready.clear()
        try:
            # print("Moving disk from", origin, "to", dest)
            disk = origin.pop()
            disk.move(dest)
            dest.push(disk)
        except:
            pass
        self.__ready.set()
        return True if self.__running.isSet() else False

    def pause(self):
        self.__flag.clear()
    
    def resume(self):
        self.__flag.set()

    def stop(self):
        self.__flag.set()
        self.__running.clear()
    
    def wait(self):
        self.__ready.wait()