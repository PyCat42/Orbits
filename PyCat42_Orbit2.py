from vpython import *
#Web VPython 3.2

scene.background = vector(0.024, 0.024, 0.25)
scene.center = vector(0, 0, 0)
scene.fov =0.01
scene.userspin=False
scene.width = 400

sun = sphere(radius = 0.5, pos = scene.center, color = color.yellow)

planet1 = sphere(radius = 0.3, pos = vector(5.2,0,0), color = color.orange, make_trail = True, interval = 100, trail_type="curve", trail_radius = 0.01)
startx1 = planet1.pos.x
r1 = sqrt(planet1.pos.x**2 + planet1.pos.y**2)
v1 = 1 / sqrt(r1)
vx1 = 0
vy1 = v1
m1 = 0.001

planet2 = sphere(radius = 0.1, pos = vector(4,0,0), color = vector(0.5, 0.5, 0.5), make_trail = True, interval = 100, trail_type="curve", trail_radius = 0.01)
startx2 = planet2.pos.x
r2 = sqrt(planet2.pos.x**2 + planet2.pos.y**2)
v2 = 1 / sqrt(r2)
vx2 = 0
vy2 = v2
m2 = 1e-8

def totalEnergy(r, v, m):
    potentialEnergy = - m / r
    kineticEnergy = m * v*v / 2
    return potentialEnergy + kineticEnergy

def interplanetaryPotEnergy(planet1, m1, planet2, m2):
    r12 = sqrt((planet1.pos.x - planet2.pos.x)**2 + (planet1.pos.y - planet2.pos.y)**2)
    potentialEnergy = - m1 * m2 / r12
    return potentialEnergy

def acceleration(planet, distance, planet1, m1):
    ax = - planet.pos.x / (distance**3)
    ay = - planet.pos.y / (distance**3)
    x = planet.pos.x - planet1.pos.x
    y = planet.pos.y - planet1.pos.y
    r = sqrt(x**2 + y**2)
    axfrom1 = - m1 * x / (r**3)
    ayfrom1 = - m1 * x / (r**3)
    ax += axfrom1
    ay += ayfrom1
    return ax, ay
ax1, ay1 = acceleration(planet1, r1, planet2, m2)
ax2, ay2 = acceleration(planet2, r2, planet1, m1)


t = 0
tolerance = 0.001

running = False

timeenergyReadout = wtext(text = "")

def startButton():
    global running, m1, v1, vx1, vy1, r1, ax1, ay1, planet1, m2, v2, vx2, vy2, r2, ax2, ay2, planet2, t, tolerance
    if running == False:
        running = True
        print("Zapoceta simulacija")
        while running:
            rate(1000000)
            a1 = sqrt(ax1**2 + ay1**2)
            a2 = sqrt(ax2**2 + ay2**2)
            amax = max(a1, a2)
            dt = tolerance / abs(amax)
            
            planet1.pos.x += (vx1 * dt + 0.5 * ax1 * (dt**2))
            planet1.pos.y += (vy1 * dt + 0.5 * ay1 * (dt**2))
            planet2.pos.x += (vx2 * dt + 0.5 * ax2 * (dt**2))
            planet2.pos.y += (vy2 * dt + 0.5 * ay2 * (dt**2))

            r1 = sqrt(planet1.pos.x**2 + planet1.pos.y**2)
            r2 = sqrt(planet2.pos.x**2 + planet2.pos.y**2)
            
            vx1 += 0.5 * ax1 * dt
            vy1 += 0.5 * ay1 * dt
            vx2 += 0.5 * ax2 * dt
            vy2 += 0.5 * ay2 * dt
            
            ax1, ay1 = acceleration(planet1, r1, planet2, m2)
            ax2, ay2 = acceleration(planet2, r2, planet1, m1)
            
            vx1 += 0.5 * ax1 * dt
            vy1 += 0.5 * ay1 * dt
            vx2 += 0.5 * ax2 * dt
            vy2 += 0.5 * ay2 * dt
            
            tE = totalEnergy(r1, v1, m1) + totalEnergy(r2, v2, m2) + interplanetaryPotEnergy(planet1, m1, planet2, m2)
            timeenergyReadout.text = "<b>Proteklo vreme: {:f6.2}    Ukupna energija sistema: {:e8.4}</b>".format(t, tE)
            
            t += dt
            
    if running == True:
        running = False
        print("Pauzirana simulacija")
        
scene.append_to_caption("\n\n")
button(text = "Zapocni/Zaustavi", bind = startButton)



