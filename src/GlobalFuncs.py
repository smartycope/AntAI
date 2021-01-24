from Point import *
import os, math
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import time

class Pointer:
    def __init__(self, val):
        self.contents = val


def loadAsset(dir, name, extension='png'):
    return loadImage(dir + name + '.' + extension)


# Finds the closest point in the list to what it's given
def findClosestPoint(target, comparatorList):
    finalDist = 1000000

    for i in comparatorList:
        current = getDist(target, i)
        if current < finalDist:
            finalDist = current

    return finalDist


def findClosestXPoint(target, comparatorList, offsetIndex = 0):
    finalDist = 1000000
    result = 0

    # for i in range(len(comparatorList) - offsetIndex):
    for current in comparatorList:
        # current = comparatorList[i + offsetIndex]
        currentDist = abs(target.x - current.x)
        if currentDist < finalDist:
            result = current
            finalDist = currentDist

    return result


def getDist(a, b):
    return math.sqrt(((b.x - a.x)**2) + ((b.y - a.y)**2))


def getGroundPoints(groundPoints):
    returnMe = []
    for i in range(len(groundPoints) - 1):
        returnMe += getPointsAlongLine(groundPoints[i], groundPoints[i + 1])

    return returnMe


def getPointsAlongLine(p1, p2):
    p1 = Pointi(p1)
    p2 = Pointi(p2)

    returnMe = []

    dx = p2.x - p1.x
    dy = p2.y - p1.y

    for x in range(p1.x, p2.x):
        y = p1.y + dy * (x - p1.x) / dx
        returnMe.append(Pointf(x, y))

    return returnMe
    

def portableFilename(filename):
    return os.path.join(*filename.split('/'))


def loadImage(filename):
    # if pygame.image.get_extended():
    filename = '/' + portableFilename(DATA + '/' + filename)

    image = pygame.image.load(filename)
    # self.image = self.image.convert()
    image = image.convert_alpha()
    # else:
    #     assert(not f"Cannot support the file extension {}")
    return image


def drawAllGroundPoints(surface, gp):
    for i in gp:
        pygame.gfxdraw.pixel(surface, *i.datai(), [255, 0, 0])


def rotatePoint(p, angle, pivotPoint, radians = False):
    if not radians:
        angle = math.radians(angle)
    # p -= pivotPoint
    # tmp = pygame.math.Vector2(p.data()).normalize().rotate(amount)
    # return Pointf(tmp.x, tmp.y) + pivotPoint

    dx = p.x - pivotPoint.x
    dy = p.y - pivotPoint.y
    newX = dx * math.cos(angle) - dy * math.sin(angle) + pivotPoint.x
    newY = dx * math.sin(angle) + dy * math.cos(angle) + pivotPoint.y

    return Pointf(newX, newY)


def rotateSurface(surface, angle, pivot, offset):
    """Rotate the surface around the pivot point.

    Args:
        surface (pygame.Surface): The surface that is to be rotated.
        angle (float): Rotate by this angle.
        pivot (tuple, list, pygame.math.Vector2): The pivot point.
        offset (pygame.math.Vector2): This vector is added to the pivot.
    """
    rotated_image = pygame.transform.rotozoom(surface, -angle, 1)  # Rotate the image.
    rotated_offset = offset.rotate(angle)  # Rotate the offset vector.
    # Add the offset vector to the center/pivot point to shift the rect.
    rect = rotated_image.get_rect(center=pivot+rotated_offset)
    return rotated_image, rect  # Return the rotated image and shifted rect.


def getMidPoint(p1, p2):
    return Pointf((p1.x + p2.x) / 2, (p1.y + p2.y) / 2)


def timeFunc(func, params, name, accuracy = 5):
    t = time.process_time()
    func(*params)
    elapsed_time = round(time.process_time() - t, accuracy)
    print(name, ' ' * (15 - len(name)), '\ttook', elapsed_time if elapsed_time >= 0.00001 else 0.00000, '\ttime to run.')