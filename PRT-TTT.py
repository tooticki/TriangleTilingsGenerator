import math, cmath, cairo, sys

goldenRatio = (1 + math.sqrt(5))/2

def subdivide(base_triangles):
    result = []
    if(TTT):
        for color, A, B, C in base_triangles:
            if color == 0:
                P, Q = B + (C - B)/goldenRatio, B + (A - B)/goldenRatio
                result += [(0, C, A, P), (0, P, B, Q), (1, A, Q, P)]
            else:
                P = A + (C - A) / goldenRatio
                result += [(0, B, A, P), (1, C, P, B)]
    else:
        for color, A, B, C in base_triangles:
            if color == 0:
                P, Q = B + (C - B)/goldenRatio, A + (B - A)/goldenRatio
                result += [(0, C, A, P), (0, Q, A, P), (1, B, Q, P)]
            else:
                P = A + (C - A) / goldenRatio
                result += [(0, B, A, P), (1, B, P, C)]
    return result

#input
if len(sys.argv) != 4:
	print('./PRT_TTT.py <image_size> <type> <level>')
	sys.exit()

size = int(sys.argv[1])
if sys.argv[2] == 'TTT':
	TTT = 1
elif sys.argv[2] == 'PRT':
	TTT = 0
else:
	print('<type> TTT PRT')
	sys.exit()
hierarchyLevel = int(sys.argv[3])
wheelRadius = size/2

# basic form
base_triangles = []
triangles = []
for i in xrange(10):
    B = cmath.rect(1, (2*i - 1)*math.pi / 10)
    C = cmath.rect(1, (2*i + 1)*math.pi / 10)
    if i % 2 == 0:
        B, C = C, B
    base_triangles.append((0, B, 0j, C))

# subdivision
triangles.append(base_triangles)
for i in xrange(hierarchyLevel):
    base_triangles = subdivide(base_triangles)
    triangles.append(base_triangles)
    print 'level %s: done'%i

# drawing
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, size, size)
cr = cairo.Context(surface)
cr.rectangle(0, 0, size, size)
cr.set_source_rgb(1., 1., 1.)
cr.fill()

cr.translate(size/2, size/2)
cr.scale(wheelRadius, wheelRadius)

# painting triangles
for color, A, B, C in base_triangles:
    if color == 1:
        cr.move_to(A.real, A.imag)
        cr.line_to(B.real, B.imag)
        cr.line_to(C.real, C.imag)
        cr.close_path()
cr.set_source_rgb(0.8, 0.6, 1.1)
cr.fill()
    
for color, A, B, C in base_triangles:
    if color == 0:
        cr.move_to(A.real, A.imag)
        cr.line_to(B.real, B.imag)
        cr.line_to(C.real, C.imag)
        cr.close_path()
cr.set_source_rgb(0.3, 0.01, 0.4)
cr.fill()  
print 'painting: done'

# drawing outlines
color, A, B, C = base_triangles[0]
cr.set_line_width(abs(B-A)/20.0)
cr.set_line_join(cairo.LINE_JOIN_ROUND)
for i in xrange(hierarchyLevel+1):
    t = triangles[i]
    cr.set_line_width(max(abs(B-A)/5.0/(i/3+15), 0.001))
    for color, A, B, C in t:
        cr.move_to(A.real, A.imag)
        cr.line_to(B.real, B.imag)
        cr.line_to(C.real, C.imag)
        cr.close_path()
    cr.set_source_rgb(0, 0, 0)
    cr.stroke()
print 'outlines: done'

# output
if TTT: name = 'TTT'
else: name = 'PRT'
surface.write_to_png(name + '_level-%s_size-%s'%(hierarchyLevel,size) + '.png')
