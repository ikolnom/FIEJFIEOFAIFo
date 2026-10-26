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

        if den == 0:
            break


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

def drawGeodesic(p1, p2, draw, intersections):
    draw.circle(xy=(((p1+p2)//2),width), radius=((p2 - p1) //2))

def getIntersection(g1,g2,h1,h2, width):
    r1 = (g2-g1)/2
    r2 = (h2-h1)/2
    m1 = (g1+g2)/2
    m2 = (h1+h2)/2

    x = ((r1**2) - (r2**2) - (m1**2) + (m2**2)) // (2 * (m2 - m1))
    y = math.sqrt((r2**2) - ((x-m2)**2))
    return (x,width-y)

def getGeodesicIntersections(g1,g2,fn, interval_size, width):
    intersection_points = []

    g1p = fracToPixel(g1, interval_size)
    g2p = fracToPixel(g2, interval_size)

    m = (g1p+g2p)/2
    r = (g2p-g1p)/2

    eta = math.floor(g2[0]/g2[1])

    for x in range(0, eta+1):
        x = fracToPixel([x,1], interval_size)
        intersection_points.append((x, width - math.sqrt((r**2) - ((x-m)**2))))

    g = g2[0]/g2[1]
    fareys = gen_farey(fn)

    for farey in fareys:
        for k in range(0, len(farey)):
            p = eta + (farey[k][0]/farey[k][1])
            if g < p:

                h1 = fracToPixel((farey[k-1][0]+(eta*farey[k-1][1]), farey[k-1][1]), interval_size)
                h2 = fracToPixel((farey[k][0]+(eta*farey[k][1]), farey[k][1]), interval_size)
                v1 = fracToPixel(g1, interval_size)
                v2 = fracToPixel(g2, interval_size)

                intersection_points.append(getIntersection(v1,v2,h1,h2,width))
                print(p)
                break
    return intersection_points

def drawNewGeodesic(p1, p2, draw, intersections, interval_size, width, n):
    leftCuts = Image.new("RGBA", size=(canvas_size, canvas_size//2))
    rightCuts = Image.new("RGBA", size=(canvas_size, canvas_size//2))

    leftDraw = ImageDraw.Draw(leftCuts)
    rightDraw = ImageDraw.Draw(rightCuts)

    leftDraw.circle(xy=(((p1+p2)//2),width), radius=((p2 - p1) //2), width= 1, outline=(255,0,0))
    rightDraw.circle(xy=(((p1+p2)//2),width), radius=((p2 - p1) //2), width= 1, outline=(0,255,0))

    seq = gen_scf(n)
    count = 0
    lr = 0
    for i in range(0, len(intersections)):
        if len(seq)==0:
            break

        if count == seq[0][0]:
            lr += 1
            count = 0
            seq.pop(0)

        if lr % 2 == 0:
            if intersections[i+1][1] > intersections[i][1]:
                leftDraw.rectangle(xy=[(intersections[i][0], intersections[i][1]), (intersections[i+1][0], intersections[i+1][1])], fill = (0,0,0,0))
            else:
                leftDraw.rectangle(xy=[(intersections[i][0], intersections[i+1][1]), (intersections[i+1][0], intersections[i][1])], fill = (0,0,0,0))
        count += 1

    rightCuts.alpha_composite(leftCuts, (0,0))
    return rightCuts



interval_size=840
length = interval_size*5
width = (interval_size*5)//2
canvas_size = interval_size*5

im = Image.new(mode="RGBA", size=(canvas_size, canvas_size//2), color=(0,0,0,255))
draw = ImageDraw.Draw(im)
draw_farey(7,interval_size,draw,length,width,canvas_size)

endpoint = (7,24)

p1 = fracToPixel((-1,2), interval_size)
p2 = fracToPixel(endpoint, interval_size)

intersections = getGeodesicIntersections((-1,2),endpoint,6, interval_size, width)
new = drawNewGeodesic(p1,p2,draw,intersections, interval_size, width, endpoint)

im.alpha_composite(new)

im.show()
