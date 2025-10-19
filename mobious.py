import math, os, sys, time

W, H = 80, 24
SHADES = " .:-=+*#%@"

def clear():
    sys.stdout.write("\x1b[H")
    sys.stdout.flush()

def mobius(u, v):
    x = (1 + 0.3 * v * math.cos(u / 2.0)) * math.cos(u)
    y = (1 + 0.3 * v * math.cos(u / 2.0)) * math.sin(u)
    z = 0.3 * v * math.sin(u / 2.0)
    return x, y, z

def rotate(x, y, z, ax, ay, az):
    cx, sx = math.cos(ax), math.sin(ax)
    cy, sy = math.cos(ay), math.sin(ay)
    cz, sz = math.cos(az), math.sin(az)
    x, y = cz*x - sz*y, sz*x + cz*y
    x, z = cy*x + sy*z, -sy*x + cy*z
    y, z = cx*y - sx*z, sx*y + cx*z
    return x, y, z

def normalize(v):
    vx, vy, vz = v
    n = math.sqrt(vx*vx + vy*vy + vz*vz) + 1e-9
    return vx/n, vy/n, vz/n

def main():
    os.system("")
    sys.stdout.write("\x1b[2J\x1b[?25l")

    fov, zcam = 15.0, 5.0
    Nu, Nv = 80, 12
    vmin, vmax = -1.0, 1.0
    us = [2*math.pi*i/(Nu-1) for i in range(Nu)]
    vs = [vmin + (vmax-vmin)*j/(Nv-1) for j in range(Nv)]

    t = 0
    try:
        while True:
            zbuf = [[-1e9]*W for _ in range(H)]
            scr = [[" "]*W for _ in range(H)]

            ax = 0.4 + 0.2*math.sin(t*0.6)
            ay = t*0.8
            az = 0.2*math.cos(t*0.5)
            light = normalize((0.5, 0.7, 1.0))

            for i in range(Nu-1):
                for j in range(Nv-1):
                    u00, v00 = us[i],   vs[j]
                    u10, v10 = us[i+1], vs[j]
                    u01, v01 = us[i],   vs[j+1]
                    u11, v11 = us[i+1], vs[j+1]
                    p00 = rotate(*mobius(u00, v00), ax, ay, az)
                    p10 = rotate(*mobius(u10, v10), ax, ay, az)
                    p01 = rotate(*mobius(u01, v01), ax, ay, az)
                    p11 = rotate(*mobius(u11, v11), ax, ay, az)

                    for tri in [(p00,p10,p11), (p00,p11,p01)]:
                        (x1,y1,z1),(x2,y2,z2),(x3,y3,z3)=tri
                        ux,uy,uz=x2-x1,y2-y1,z2-z1
                        vx,vy,vz=x3-x1,y3-y1,z3-z1
                        nx,ny,nz=uy*vz-uz*vy,uz*vx-ux*vz,ux*vy-uy*vx
                        n=normalize((nx,ny,nz))
                        ndotl=max(0,n[0]*light[0]+n[1]*light[1]+n[2]*light[2])
                        ch=SHADES[int(ndotl*(len(SHADES)-1))]

                        for a in (0.2,0.6,0.8):
                            for b in (0.3,0.5):
                                c=1-a-b
                                if c<0: continue
                                xp=a*x1+b*x2+c*x3
                                yp=a*y1+b*y2+c*y3
                                zp=a*z1+b*z2+c*z3
                                Z=zp+zcam
                                if Z<=0.1: continue
                                s=fov/Z
                                xs=int(W/2+s*xp*W*0.3)
                                ys=int(H/2-s*yp*H*0.4)
                                if 0<=xs<W and 0<=ys<H and Z>zbuf[ys][xs]:
                                    zbuf[ys][xs]=Z
                                    scr[ys][xs]=ch

            clear()
            sys.stdout.write('\n'.join(''.join(r) for r in scr))
            sys.stdout.flush()
            t+=0.05
            time.sleep(0.03)
    except KeyboardInterrupt:
        pass
    finally:
        sys.stdout.write("\x1b[?25h\n")

if __name__ == "__main__":
    main()
