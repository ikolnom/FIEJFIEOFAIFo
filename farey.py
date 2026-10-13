from PIL import Image, ImageDraw
import math

def gen_scf(n):
    seq = []

    if n[0] < n[1]:
        seq.append((0,0))

        num = n[0]
        den = n[1]
    else:
        num = n[1]
        den = n[0]
    while num != 1:
        tmp = num
        num = den
        den = tmp

        a = math.floor(num / den)
        seq.append((a,0))
        num = num - (a * den)
    seq.append((den,0))

    return seq

def gen_farey(n):
    seq = [(0,1),(1,1)]
    iterations = [seq]
    for i in range(0, n):
        new_seq = []
        for j in range(0, len(seq)-1):
            new_seq.append(seq[j])
            new_seq.append((seq[j][0]+seq[j+1][0], seq[j][1]+seq[j+1][1]))
        new_seq.append(seq[-1])
        iterations.append(new_seq)
        seq = new_seq
    return(iterations)

def draw_farey(farey_level, interval_size, draw, length, width, canvas_size):
    coordinate = 0
    for i in range(0,11):
        draw.line([(coordinate,0),(coordinate,canvas_size/2)])
        coordinate += interval_size
    iterations = gen_farey(farey_level)
    for i in range(0, 11):
        offset = i*interval_size
        for it in iterations:
            for i in range(0, len(it)-1):
                r = (interval_size*it[i+1][0]/it[i+1][1] - interval_size*it[i][0]/it[i][1])/2
                x1 = interval_size * it[i][0]/it[i][1]
                x2 = interval_size * it[i+1][0]/it[i+1][1]
                centerpoint = (x2-x1)/2 
                draw.circle(xy=(offset+centerpoint+x1,canvas_size/2), radius=r, outline = (255,255,255))

def fracToPixel(frac, interval_size):
    return interval_size + (frac[0]*interval_size // frac[1])

def drawGeodesic(p1, p2, draw):
    draw.circle(xy=(((p1+p2)//2),width), radius=((p2 - p1) //2))

def getIntersection(g1,g2,h1,h2, width):
    r1 = (g2-g1)/2
    r2 = (h2-h1)/2
    m1 = (g1+g2)/2
    m2 = (h1+h2)/2

    x = ((r1**2) - (r2**2) - (m1**2) + (m2**2)) // (2 * (m2 - m1))
    y = math.sqrt((r2**2) - ((x-m2)**2))
    return (x,width-y)


interval_size=420
length = interval_size*5
width = (interval_size*5)//2
canvas_size = interval_size*5

im = Image.new(mode="RGB", size=(canvas_size, canvas_size//2))
draw = ImageDraw.Draw(im)
draw_farey(4,interval_size,draw,length,width,canvas_size)

p1 = fracToPixel((-1,2), interval_size)
p2 = fracToPixel((7,3), interval_size)

drawGeodesic(p1,p2, draw)

p3 = fracToPixel((0,1), interval_size)
p4 = fracToPixel((4,1), interval_size)

drawGeodesic(p3,p4, draw)

draw.circle(xy=getIntersection(p1,p2,p3,p4, width), radius = 10)

im.show()
