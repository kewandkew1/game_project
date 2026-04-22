class BouncingBall:
    def __init__(self, x, y, size, color, vx, vy, limits):
        self.__x = float(x)
        self.__y = float(y)
        self.__size = float(size)
        self.__color = str(color)
        self.__vx = float(vx)
        self.__vy = float(vy)
        self.__limits = (float(limits[0]), float(limits[1]))
        self.__frame = 0

    def __iter__(self):
        return self

    def __next__(self):
        self.__frame += 1
        if self.__frame >= 500:
            raise StopIteration

        self.__x += self.__vx
        self.__y += self.__vy

        if self.__x < 0:
            self.__x = 0
            self.__vx *= -1
        elif self.__x + self.__size > self.__limits[0]:
            self.__x = self.__limits[0] - self.__size
            self.__vx *= -1

        if self.__y < 0:
            self.__y = 0
            self.__vy *= -1
        elif self.__y + self.__size > self.__limits[1]:
            self.__y = self.__limits[1] - self.__size
            self.__vy *= -1

        return (
            self.__x,
            self.__y,
            self.__x + self.__size,
            self.__y + self.__size,
            self.__color,
        )
