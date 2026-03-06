import time, math
import browserbotics as bb

bb.resetSimulation()
bb.setGravity(0, 0, -9.8)
DT = 1.0 / 240.0

# ============================================================
# HELPER — tracked moveable group
# ============================================================
def _mk(parts, halfExtent, position, color, mass=0, shape="box"):
    b = bb.createBody(shape=shape, halfExtent=halfExtent,
                      position=position, color=color, mass=mass)
    parts.append((b, list(position)))
    return b

def reposition_group(parts, new_cx, new_cy, orig_cx, orig_cy):
    dx = new_cx - orig_cx; dy = new_cy - orig_cy
    if abs(dx) < 0.001 and abs(dy) < 0.001:
        return
    qI = [0, 0, 0, 1]
    for bid, (ox, oy, oz) in parts:
        try: bb.resetBasePose(bid, [ox + dx, oy + dy, oz], qI)
        except: pass

# ============================================================
# ROOM  (10 x 8 x 4 m)  — STATIC
# ============================================================
RL = 10.0; RW = 8.0; RH = 4.0; WT = 0.2

bb.createBody(shape="box", halfExtent=[RL/2, RW/2, 0.05],
    position=[0, 0, -0.05], color=0xf0eeea, mass=0)
for i in range(-4, 5):
    bb.createBody(shape="box", halfExtent=[RL/2, 0.01, 0.001],
        position=[0, i*1.0, 0.001], color=0xddddcc, mass=0)
for j in range(-4, 6):
    bb.createBody(shape="box", halfExtent=[0.01, RW/2, 0.001],
        position=[j*1.0, 0, 0.001], color=0xddddcc, mass=0)

bb.createBody(shape="box", halfExtent=[RL/2, RW/2, 0.04],
    position=[0, 0, RH+0.04], color=0xfafafa, mass=0)
for cpx, cpy in [(-2.5,1.5),(0,1.5),(2.5,1.5),(-2.5,-1.5),(0,-1.5),(2.5,-1.5)]:
    bb.createBody(shape="box", halfExtent=[0.45,0.28,0.008],
        position=[cpx,cpy,RH-0.01], color=0xffffff, mass=0)
    bb.createBody(shape="box", halfExtent=[0.42,0.25,0.004],
        position=[cpx,cpy,RH-0.016], color=0xfffde0, mass=0)

bb.createBody(shape="box", halfExtent=[RL/2, WT/2, RH/2],
    position=[0, -RW/2, RH/2], color=0xeae6e0, mass=0)
bb.createBody(shape="box", halfExtent=[WT/2, RW/2, RH/2],
    position=[-RL/2, 0, RH/2], color=0xeae6e0, mass=0)
bb.createBody(shape="box", halfExtent=[WT/2, RW/2, RH/2],
    position=[RL/2, 0, RH/2], color=0xeae6e0, mass=0)

for swy in [-RW/2, RW/2]:
    bb.createBody(shape="box", halfExtent=[RL/2, 0.012, 0.055],
        position=[0, swy, 1.2], color=0x2c6fad, mass=0)
bb.createBody(shape="box", halfExtent=[0.012, RW/2, 0.055],
    position=[-RL/2, 0, 1.2], color=0x2c6fad, mass=0)
bb.createBody(shape="box", halfExtent=[0.012, RW/2, 0.055],
    position=[RL/2, 0, 1.2], color=0x2c6fad, mass=0)
for sy in [-RW/2, RW/2]:
    bb.createBody(shape="box", halfExtent=[RL/2, WT/2, 0.05],
        position=[0, sy, 0.05], color=0xd0ccc5, mass=0)
bb.createBody(shape="box", halfExtent=[WT/2, RW/2, 0.05],
    position=[-RL/2, 0, 0.05], color=0xd0ccc5, mass=0)
bb.createBody(shape="box", halfExtent=[WT/2, RW/2, 0.05],
    position=[RL/2, 0, 0.05], color=0xd0ccc5, mass=0)

# ============================================================
# FRONT WALL + DOOR + HOSPITAL SIGN  — STATIC
# ============================================================
dw=2.0; dh=2.8; sw=(RL-dw)/2
bb.createBody(shape="box", halfExtent=[sw/2, WT/2, RH/2],
    position=[-dw/2-sw/2, RW/2, RH/2], color=0xeae6e0, mass=0)
bb.createBody(shape="box", halfExtent=[sw/2, WT/2, RH/2],
    position=[dw/2+sw/2, RW/2, RH/2], color=0xeae6e0, mass=0)
bb.createBody(shape="box", halfExtent=[dw/2, WT/2, (RH-dh)/2],
    position=[0, RW/2, dh+(RH-dh)/2], color=0xeae6e0, mass=0)
bb.createBody(shape="box", halfExtent=[dw/2-0.05, 0.04, dh/2],
    position=[0, RW/2+0.04, dh/2], color=0x7a9e7e, mass=0)
for sx in [-dw/2, dw/2]:
    bb.createBody(shape="box", halfExtent=[0.045, 0.06, dh/2],
        position=[sx, RW/2, dh/2], color=0xc8b89a, mass=0)
bb.createBody(shape="box", halfExtent=[dw/2, 0.06, 0.045],
    position=[0, RW/2, dh], color=0xc8b89a, mass=0)
bb.createBody(shape="box", halfExtent=[0.045, 0.012, 0.009],
    position=[0.72, RW/2+0.05, 1.05], color=0xd4af37, mass=0)
bb.createBody(shape="box", halfExtent=[0.85, 0.05, 0.14],
    position=[0, RW/2+0.02, dh+0.18], color=0xcc0000, mass=0)
bb.createBody(shape="box", halfExtent=[0.05, 0.06, 0.10],
    position=[-0.72, RW/2+0.07, dh+0.18], color=0xffffff, mass=0)
bb.createBody(shape="box", halfExtent=[0.10, 0.06, 0.05],
    position=[-0.72, RW/2+0.07, dh+0.18], color=0xffffff, mass=0)
try:
    bb.createDebugText("", [0.0, RW/2-0.10, dh+0.18],
        color='white', size=1.3)
except: pass

for hsx in [-dw/2-0.28, dw/2+0.28]:
    bb.createBody(shape="box", halfExtent=[0.045,0.04,0.11],
        position=[hsx, RW/2-0.05, 1.4], color=0xffffff, mass=0)
    bb.createBody(shape="box", halfExtent=[0.018,0.018,0.025],
        position=[hsx, RW/2-0.06, 1.27], color=0xcccccc, mass=0)

bb.createBody(shape="box", halfExtent=[0.60, 0.60, 0.06],
    position=[0, 0, RH+0.09], color=0xcc0000, mass=0)
bb.createBody(shape="box", halfExtent=[0.14, 0.46, 0.08],
    position=[0, 0, RH+0.17], color=0xffffff, mass=0)
bb.createBody(shape="box", halfExtent=[0.46, 0.14, 0.08],
    position=[0, 0, RH+0.17], color=0xffffff, mass=0)

# ============================================================
# WINDOWS  — STATIC
# ============================================================
wx=-RL/2; wy=1.5
bb.createBody(shape="box", halfExtent=[0.04,0.72,0.57],
    position=[wx,wy,2.0], color=0x87ceeb, mass=0)
for zz in [1.43,2.57]:
    bb.createBody(shape="box", halfExtent=[0.055,0.74,0.038],
        position=[wx,wy,zz], color=0xffffff, mass=0)
for yy in [wy-0.72,wy+0.72]:
    bb.createBody(shape="box", halfExtent=[0.055,0.038,0.60],
        position=[wx,yy,2.0], color=0xffffff, mass=0)
for bi in range(7):
    bb.createBody(shape="box", halfExtent=[0.032,0.66,0.013],
        position=[wx+0.01,wy,1.55+bi*0.16], color=0xf5f0e8, mass=0)
wx2=RL/2; wy2=-1.5
bb.createBody(shape="box", halfExtent=[0.04,0.70,0.55],
    position=[wx2,wy2,2.0], color=0x87ceeb, mass=0)
for zz in [1.45,2.55]:
    bb.createBody(shape="box", halfExtent=[0.05,0.72,0.035],
        position=[wx2,wy2,zz], color=0xffffff, mass=0)
for yy in [wy2-0.70,wy2+0.70]:
    bb.createBody(shape="box", halfExtent=[0.05,0.035,0.57],
        position=[wx2,yy,2.0], color=0xffffff, mass=0)

# ============================================================
# HOSPITAL BED  — MOVEABLE GROUP  (anchor 0, 0)
# ============================================================
bed_parts = []
BED_AX = 0.0; BED_AY = 0.0
BL=2.2; BW=1.1; BH=0.5

_mk(bed_parts, [BL/2,BW/2,BH/2], [0,0,BH/2], 0xdde8f0)
for lx in [-BL/2+0.1, BL/2-0.1]:
    for ly in [-BW/2+0.08, BW/2-0.08]:
        _mk(bed_parts, [0.04,0.04,BH/2], [lx,ly,BH/2], 0xaabbc8)
_mk(bed_parts, [BL/2-0.06,BW/2-0.06,0.1], [0,0,BH+0.1], 0xf0f8ff)
_mk(bed_parts, [0.28,0.22,0.09], [BL/2-0.32,0,BH+0.25], 0xfff8f0)
_mk(bed_parts, [0.6,BW/2-0.07,0.06], [-0.35,0,BH+0.25], 0x5b9bd5)
for sy in [-1,1]:
    _mk(bed_parts, [BL/2-0.1,0.018,0.18], [0,sy*BW/2,BH+0.18], 0xb8ccd8)
    for px in [-0.7,0,0.7]:
        _mk(bed_parts, [0.015,0.015,0.18], [px,sy*BW/2,BH+0.18], 0x99aabb)
_mk(bed_parts, [0.04,BW/2,0.35], [BL/2,0,BH+0.35], 0x3a6186)
_mk(bed_parts, [0.04,BW/2,0.22], [-BL/2,0,BH+0.22], 0x3a6186)
for cx3,cy3,he in [
    [0, BW/2+0.35,  [BL/2+0.3,0.014,0.014]],
    [0,-(BW/2+0.35),[BL/2+0.3,0.014,0.014]],
    [ BL/2+0.3,0,   [0.014,BW/2+0.35,0.014]],
    [-(BL/2+0.3),0, [0.014,BW/2+0.35,0.014]],
]:
    _mk(bed_parts, he, [cx3,cy3,RH-0.1], 0xbbbbbb)
_mk(bed_parts, [0.007,BW/2+0.33,0.88], [BL/2+0.3,0,RH-0.54], 0x4a7fc1)
# Drop-zone marker
_mk(bed_parts, [0.08,0.08,0.004], [0.0,0.0,BH+0.204], 0xffaa00)
_mk(bed_parts, [0.055,0.055,0.003], [0.0,0.0,BH+0.207], 0xffd060)

# ============================================================
# PANDA ROBOT ARM  — MOVEABLE BASE
# ============================================================
RBX = 0.0; RBY = -1.0; RBZ = 0.12
robo_orn = bb.getQuaternionFromEuler([0, 0, math.pi/2])

robot = bb.loadURDF(
    'panda.urdf',
    [RBX, RBY, RBZ],
    robo_orn,
    fixedBase=True
)

ARM_JOINT_INDICES    = list(range(7))
FINGER_JOINT_INDICES = [7, 8]
ee_link              = 10
FINGER_OPEN   = 0.04
FINGER_CLOSED = 0.0

def set_fingers(val):
    for ji in FINGER_JOINT_INDICES:
        bb.setJointMotorControl(robot, ji, targetPosition=val)

# Visual gripper boxes
FINGER_HALF = [0.013, 0.014, 0.055]
finger_L = bb.createBody(shape="box", halfExtent=FINGER_HALF,
    position=[0,0,-5], color=0x445566, mass=0)
finger_R = bb.createBody(shape="box", halfExtent=FINGER_HALF,
    position=[0,0,-5], color=0x445566, mass=0)

SPREAD_OPEN   = 0.042
SPREAD_CLOSED = 0.006
grip_spread   = SPREAD_OPEN

def quat_rotate(q, v):
    qx,qy,qz,qw = q
    ix =  qw*v[0] + qy*v[2] - qz*v[1]
    iy =  qw*v[1] + qz*v[0] - qx*v[2]
    iz =  qw*v[2] + qx*v[1] - qy*v[0]
    iw = -qx*v[0] - qy*v[1] - qz*v[2]
    return [
        ix*qw + iw*(-qx) + iy*(-qz) - iz*(-qy),
        iy*qw + iw*(-qy) + iz*(-qx) - ix*(-qz),
        iz*qw + iw*(-qz) + ix*(-qy) - iy*(-qx)
    ]

def update_fingers(ep, eo, spread):
    dL = quat_rotate(eo, [ spread, 0, -0.05])
    dR = quat_rotate(eo, [-spread, 0, -0.05])
    try:
        bb.resetBasePose(finger_L,
            [ep[0]+dL[0], ep[1]+dL[1], ep[2]+dL[2]], eo)
        bb.resetBasePose(finger_R,
            [ep[0]+dR[0], ep[1]+dR[1], ep[2]+dR[2]], eo)
    except: pass

def open_grip():
    global grip_spread
    grip_spread = SPREAD_OPEN
    set_fingers(FINGER_OPEN)

def close_grip():
    global grip_spread
    grip_spread = SPREAD_CLOSED
    set_fingers(FINGER_CLOSED)

# ============================================================
# ROBOT PLATFORM + TRAY TABLE  — MOVEABLE GROUP  (anchor RBX, RBY)
# ============================================================
robo_parts = []

_mk(robo_parts, [0.35,0.35,0.1], [RBX,RBY,0.1], 0x1c3f6e)
for wx4,wy4 in [(-0.3,-0.3),(-0.3,0.3),(0.3,-0.3),(0.3,0.3)]:
    _mk(robo_parts, [0.08,0.055,0.075], [RBX+wx4,RBY+wy4,0.075], 0x0a0a0a)
    _mk(robo_parts, [0.03,0.06,0.03], [RBX+wx4,RBY+wy4,0.075], 0x444444)
_mk(robo_parts, [0.33,0.018,0.005], [RBX,RBY,0.205], 0x00aaff)
_mk(robo_parts, [0.018,0.33,0.005], [RBX,RBY,0.205], 0x00aaff)
_mk(robo_parts, [0.026,0.026,0.032], [RBX+0.28,RBY,0.21], 0x00ff88)

# Tray table (part of robot group — moves with robot)
TRX_OFF = 0.55   # offset from RBX
TRY_OFF = 0.0    # offset from RBY
TRX = RBX + TRX_OFF; TRY = RBY + TRY_OFF; TRZ = 0.62

_mk(robo_parts, [0.025,0.025,TRZ/2], [TRX,TRY,TRZ/2], 0xaaaaaa)
_mk(robo_parts, [0.24,0.03,0.015], [TRX,TRY,0.025], 0x999999)
_mk(robo_parts, [0.03,0.24,0.015], [TRX,TRY,0.025], 0x999999)
_mk(robo_parts, [0.30,0.22,0.016], [TRX,TRY,TRZ], 0xb8d4b8)
for sign in [-1,1]:
    _mk(robo_parts, [0.30,0.012,0.022], [TRX,TRY+sign*0.22,TRZ+0.018], 0x888888)
    _mk(robo_parts, [0.012,0.22,0.022], [TRX+sign*0.30,TRY,TRZ+0.018], 0x888888)
_mk(robo_parts, [0.018,0.018,0.038], [TRX+0.18,TRY+0.12,TRZ+0.054], 0xffffff)
_mk(robo_parts, [0.007,0.007,0.072], [TRX+0.18,TRY+0.12,TRZ+0.13], 0xcccccc)
_mk(robo_parts, [0.022,0.016,0.032], [TRX+0.18,TRY-0.12,TRZ+0.048], 0xe67e22)

# ============================================================
# CUBE  — DYNAMIC (mass > 0, physically moveable)
# ============================================================
CH = 0.028
LOC_A = [TRX, TRY, TRZ + 0.016 + CH]       # on tray
LOC_B = [0.0, 0.0, BH + 0.21 + CH]         # on bed drop-zone

cube = bb.createBody(shape="box", halfExtent=[CH, CH, CH],
    position=LOC_A, color=0xff4500, mass=0)

# ============================================================
# IV STAND  — MOVEABLE GROUP  (anchor IVX, IVY)
# ============================================================
iv_parts = []
IVX=-0.9; IVY=BW/2+0.35

_mk(iv_parts, [0.018,0.018,0.98], [IVX,IVY,0.98], 0xbbbbbb)
_mk(iv_parts, [0.28,0.032,0.016], [IVX,IVY,0.018], 0xaaaaaa)
_mk(iv_parts, [0.032,0.28,0.016], [IVX,IVY,0.018], 0xaaaaaa)
_mk(iv_parts, [0.072,0.022,0.115], [IVX,IVY,1.87], 0xc8e6ff)
_mk(iv_parts, [0.006,0.006,0.48], [IVX+0.01,IVY-0.02,1.28], 0xaaffaa)
_mk(iv_parts, [0.07,0.04,0.08], [IVX,IVY,1.35], 0x2255aa)

# ============================================================
# VITAL SIGNS MONITOR  — MOVEABLE GROUP  (anchor MNX, MNY)
# ============================================================
mon_parts = []
MNX=-1.7; MNY=-(BW/2+0.35)

_mk(mon_parts, [0.02,0.02,0.62], [MNX,MNY,0.62], 0x777777)
_mk(mon_parts, [0.16,0.16,0.025], [MNX,MNY,0.025], 0x666666)
_mk(mon_parts, [0.28,0.05,0.22], [MNX,MNY,1.38], 0x1a1a2e)
_mk(mon_parts, [0.25,0.02,0.18], [MNX,MNY-0.04,1.38], 0x003300)
for k in range(6):
    h=0.03 if k==2 else 0.008
    _mk(mon_parts, [0.022,0.004,h], [MNX-0.12+k*0.048,MNY-0.045,1.4+h], 0x00ff55)
for k in range(5):
    _mk(mon_parts, [0.02,0.004,0.007], [MNX-0.1+k*0.05,MNY-0.045,1.22], 0x4488ff)

# ============================================================
# CRASH CART  — MOVEABLE GROUP  (anchor CCX, CCY)
# ============================================================
cart_parts = []
CCX=3.8; CCY=RW/2-1.5

_mk(cart_parts, [0.28,0.22,0.58], [CCX,CCY,0.58], 0xdd2222)
_mk(cart_parts, [0.28,0.22,0.04], [CCX,CCY,1.2], 0xcc1111)
_mk(cart_parts, [0.18,0.04,0.12], [CCX,CCY-0.22,0.9], 0x111111)
for dz2 in [0.22,0.45,0.72]:
    _mk(cart_parts, [0.26,0.005,0.09], [CCX,CCY-0.225,dz2], 0xcc1111)
    _mk(cart_parts, [0.04,0.015,0.015], [CCX,CCY-0.238,dz2+0.045], 0xd4af37)
for cwx,cwy in [(-0.22,-0.18),(-0.22,0.18),(0.22,-0.18),(0.22,0.18)]:
    _mk(cart_parts, [0.04,0.03,0.04], [CCX+cwx,CCY+cwy,0.04], 0x111111)

# ============================================================
# OXYGEN TANK  — MOVEABLE GROUP  (anchor OXX, OXY)
# ============================================================
o2_parts = []
OXX=-1.4; OXY=BW/2+0.6

_mk(o2_parts, [0.07,0.07,0.52], [OXX,OXY,0.52], 0x228b22)
_mk(o2_parts, [0.05,0.05,0.08], [OXX,OXY,1.12], 0x1a6b1a)
_mk(o2_parts, [0.08,0.04,0.04], [OXX,OXY,1.3], 0x888888)

# ============================================================
# MEDICINE CABINET  — STATIC
# ============================================================
MCX=3.5; MCY=-RW/2+0.16
bb.createBody(shape="box", halfExtent=[0.5,0.18,0.72],
    position=[MCX,MCY,1.06], color=0xf8f8f8, mass=0)
bb.createBody(shape="box", halfExtent=[0.48,0.008,0.7],
    position=[MCX,MCY-0.188,1.06], color=0xe0e0e0, mass=0)
bb.createBody(shape="box", halfExtent=[0.12,0.009,0.038],
    position=[MCX,MCY-0.196,1.3], color=0xff2222, mass=0)
bb.createBody(shape="box", halfExtent=[0.038,0.009,0.12],
    position=[MCX,MCY-0.196,1.3], color=0xff2222, mass=0)
for sz in [0.75,1.05,1.35]:
    bb.createBody(shape="box", halfExtent=[0.46,0.16,0.008],
        position=[MCX,MCY,sz], color=0xeeeeee, mass=0)

# ============================================================
# SINK + MIRROR  — STATIC
# ============================================================
SKX=-3.8; SKY=-RW/2+0.2
bb.createBody(shape="box", halfExtent=[0.3,0.22,0.4],
    position=[SKX,SKY,0.4], color=0xf5f5f5, mass=0)
bb.createBody(shape="box", halfExtent=[0.28,0.2,0.016],
    position=[SKX,SKY,0.83], color=0xffffff, mass=0)
bb.createBody(shape="box", halfExtent=[0.2,0.16,0.058],
    position=[SKX,SKY,0.798], color=0xd8eeff, mass=0)
bb.createBody(shape="box", halfExtent=[0.012,0.012,0.1],
    position=[SKX,SKY-0.11,0.96], color=0xcccccc, mass=0)
bb.createBody(shape="box", halfExtent=[0.038,0.012,0.012],
    position=[SKX,SKY-0.12,1.06], color=0xcccccc, mass=0)
bb.createBody(shape="box", halfExtent=[0.025,0.025,0.065],
    position=[SKX+0.2,SKY-0.1,0.895], color=0x87ceeb, mass=0)
bb.createBody(shape="box", halfExtent=[0.27,0.012,0.32],
    position=[SKX,SKY-0.214,1.32], color=0xaaaaaa, mass=0)
bb.createBody(shape="box", halfExtent=[0.25,0.008,0.30],
    position=[SKX,SKY-0.212,1.32], color=0xd0eef8, mass=0)

# ============================================================
# OVERHEAD SURGICAL LIGHT  — STATIC
# ============================================================
bb.createBody(shape="box", halfExtent=[0.55,0.55,0.04],
    position=[0,0,RH-0.04], color=0xffffff, mass=0)
bb.createBody(shape="box", halfExtent=[0.48,0.48,0.025],
    position=[0,0,RH-0.09], color=0xffffee, mass=0)
bb.createBody(shape="box", halfExtent=[0.016,0.016,0.38],
    position=[0,0,RH-0.47], color=0x888888, mass=0)
for lx2 in [-2.5,2.5]:
    bb.createBody(shape="box", halfExtent=[0.08,1.2,0.02],
        position=[lx2,0,RH-0.02], color=0xfff8ee, mass=0)

# ============================================================
# WALL CLOCK  — STATIC
# ============================================================
bb.createBody(shape="box", halfExtent=[0.16,0.03,0.16],
    position=[2.0,-RW/2+0.06,2.5], color=0xffffff, mass=0)
bb.createBody(shape="box", halfExtent=[0.005,0.022,0.08],
    position=[2.0,-RW/2+0.032,2.54], color=0x333333, mass=0)
bb.createBody(shape="box", halfExtent=[0.07,0.022,0.005],
    position=[2.04,-RW/2+0.032,2.5], color=0x333333, mass=0)

# ============================================================
# WHITEBOARD  — STATIC
# ============================================================
bb.createBody(shape="box", halfExtent=[0.42,0.022,0.34],
    position=[-2.0,-RW/2+0.022,1.8], color=0x888888, mass=0)
bb.createBody(shape="box", halfExtent=[0.40,0.018,0.32],
    position=[-2.0,-RW/2+0.03,1.8], color=0xffffff, mass=0)
for k in range(4):
    bb.createBody(shape="box", halfExtent=[0.36,0.02,0.007],
        position=[-2.0,-RW/2+0.05,1.62+k*0.1], color=0x3366cc, mass=0)
bb.createBody(shape="box", halfExtent=[0.42,0.03,0.018],
    position=[-2.0,-RW/2+0.04,1.48], color=0x888888, mass=0)
for mk in range(3):
    bb.createBody(shape="box", halfExtent=[0.008,0.008,0.055],
        position=[-2.1+mk*0.12,-RW/2+0.04,1.50],
        color=[0x2244cc,0xff2222,0x229922][mk], mass=0)

# ============================================================
# WASTE BINS  — STATIC
# ============================================================
bb.createBody(shape="box", halfExtent=[0.12,0.12,0.18],
    position=[0.6,RBY-0.5,0.18], color=0xcc1111, mass=0)
bb.createBody(shape="box", halfExtent=[0.125,0.125,0.018],
    position=[0.6,RBY-0.5,0.375], color=0xaa0000, mass=0)
bb.createBody(shape="box", halfExtent=[0.1,0.1,0.16],
    position=[0.6,RBY-0.72,0.16], color=0xccaa00, mass=0)
bb.createBody(shape="box", halfExtent=[0.13,0.13,0.2],
    position=[-2.6,RBY-0.4,0.2], color=0x2a2a2a, mass=0)

# ============================================================
# OPERATOR / NURSE WORKSTATION  — STATIC
# ============================================================
OPX=-3.6; OPY=RW/2-1.6
bb.createBody(shape="box", halfExtent=[0.80,0.40,0.032],
    position=[OPX,OPY,0.768], color=0x8b6343, mass=0)
for odx in [-0.72,0.72]:
    for ody in [-0.36,0.36]:
        bb.createBody(shape="box", halfExtent=[0.036,0.036,0.384],
            position=[OPX+odx,OPY+ody,0.384], color=0x5c4033, mass=0)
bb.createBody(shape="box", halfExtent=[0.28,0.34,0.34],
    position=[OPX+0.46,OPY,0.34], color=0x9e7b55, mass=0)
for dz3 in [0.18,0.40,0.62]:
    bb.createBody(shape="box", halfExtent=[0.27,0.005,0.08],
        position=[OPX+0.46,OPY-0.345,dz3], color=0x7a5c3a, mass=0)
    bb.createBody(shape="box", halfExtent=[0.04,0.015,0.015],
        position=[OPX+0.46,OPY-0.36,dz3+0.04], color=0xd4af37, mass=0)
bb.createBody(shape="box", halfExtent=[0.36,0.05,0.24],
    position=[OPX-0.12,OPY+0.30,1.10], color=0x111111, mass=0)
bb.createBody(shape="box", halfExtent=[0.33,0.018,0.20],
    position=[OPX-0.12,OPY+0.31,1.10], color=0x001a33, mass=0)
for k in range(7):
    bb.createBody(shape="box", halfExtent=[0.28,0.005,0.008],
        position=[OPX-0.12,OPY+0.332,0.93+k*0.055], color=0x00aaff, mass=0)
bb.createBody(shape="box", halfExtent=[0.20,0.005,0.06],
    position=[OPX-0.12,OPY+0.332,1.22], color=0x00ff88, mass=0)
bb.createBody(shape="box", halfExtent=[0.08,0.005,0.06],
    position=[OPX+0.14,OPY+0.332,1.22], color=0xff6600, mass=0)
bb.createBody(shape="box", halfExtent=[0.036,0.036,0.15],
    position=[OPX-0.12,OPY+0.30,0.918], color=0x333333, mass=0)
bb.createBody(shape="box", halfExtent=[0.10,0.08,0.012],
    position=[OPX-0.12,OPY+0.30,0.782], color=0x333333, mass=0)
bb.createBody(shape="box", halfExtent=[0.28,0.045,0.20],
    position=[OPX+0.42,OPY+0.28,1.08], color=0x111111, mass=0)
bb.createBody(shape="box", halfExtent=[0.25,0.016,0.17],
    position=[OPX+0.42,OPY+0.295,1.08], color=0x001122, mass=0)
for k in range(5):
    bb.createBody(shape="box", halfExtent=[0.20,0.004,0.007],
        position=[OPX+0.42,OPY+0.314,0.945+k*0.055], color=0x4488ff, mass=0)
bb.createBody(shape="box", halfExtent=[0.028,0.028,0.12],
    position=[OPX+0.42,OPY+0.28,0.908], color=0x333333, mass=0)
bb.createBody(shape="box", halfExtent=[0.08,0.06,0.010],
    position=[OPX+0.42,OPY+0.28,0.782], color=0x333333, mass=0)
bb.createBody(shape="box", halfExtent=[0.20,0.085,0.012],
    position=[OPX-0.12,OPY-0.05,0.800], color=0x1a1a1a, mass=0)
for row in range(4):
    for col in range(10):
        bb.createBody(shape="box", halfExtent=[0.008,0.007,0.005],
            position=[OPX-0.28+col*0.038, OPY-0.05+row*0.018, 0.815],
            color=0x333333, mass=0)
bb.createBody(shape="box", halfExtent=[0.030,0.022,0.012],
    position=[OPX+0.18,OPY-0.05,0.800], color=0x222222, mass=0)
bb.createBody(shape="box", halfExtent=[0.028,0.010,0.004],
    position=[OPX+0.18,OPY-0.065,0.814], color=0x111111, mass=0)
bb.createBody(shape="box", halfExtent=[0.10,0.22,0.22],
    position=[OPX-0.62,OPY+0.12,0.22], color=0x1a1a2e, mass=0)
for dbz in [0.32,0.38]:
    bb.createBody(shape="box", halfExtent=[0.09,0.005,0.025],
        position=[OPX-0.62,OPY-0.105,dbz], color=0x333355, mass=0)
bb.createBody(shape="box", halfExtent=[0.006,0.006,0.006],
    position=[OPX-0.62,OPY-0.108,0.28], color=0x00ff44, mass=0)
bb.createBody(shape="box", halfExtent=[0.36,0.36,0.062],
    position=[OPX,OPY-1.0,0.48], color=0x1a1a2e, mass=0)
bb.createBody(shape="box", halfExtent=[0.36,0.062,0.30],
    position=[OPX,OPY-1.32,0.82], color=0x1a1a2e, mass=0)
for odx,ody in [(-0.28,-0.28),(-0.28,0.28),(0.28,-0.28),(0.28,0.28)]:
    bb.createBody(shape="box", halfExtent=[0.034,0.034,0.24],
        position=[OPX+odx,OPY-1.0+ody,0.24], color=0x0d0d1a, mass=0)
for arx in [-0.34,0.34]:
    bb.createBody(shape="box", halfExtent=[0.032,0.10,0.018],
        position=[OPX+arx,OPY-1.0,0.60], color=0x222244, mass=0)
    bb.createBody(shape="box", halfExtent=[0.032,0.032,0.12],
        position=[OPX+arx,OPY-0.92,0.54], color=0x222244, mass=0)

# ============================================================
# SECONDARY WORKSTATION  — STATIC
# ============================================================
WS2X=3.6; WS2Y=-RW/2+0.5
bb.createBody(shape="box", halfExtent=[0.55,0.32,0.028],
    position=[WS2X,WS2Y,0.758], color=0x7a6248, mass=0)
for odx2 in [-0.48,0.48]:
    for ody2 in [-0.28,0.28]:
        bb.createBody(shape="box", halfExtent=[0.030,0.030,0.38],
            position=[WS2X+odx2,WS2Y+ody2,0.38], color=0x5a4535, mass=0)
bb.createBody(shape="box", halfExtent=[0.30,0.045,0.20],
    position=[WS2X,WS2Y+0.26,1.06], color=0x111111, mass=0)
bb.createBody(shape="box", halfExtent=[0.27,0.015,0.17],
    position=[WS2X,WS2Y+0.275,1.06], color=0x001122, mass=0)
for k in range(5):
    bb.createBody(shape="box", halfExtent=[0.22,0.004,0.007],
        position=[WS2X,WS2Y+0.294,0.93+k*0.055], color=0x00ccff, mass=0)
bb.createBody(shape="box", halfExtent=[0.030,0.030,0.13],
    position=[WS2X,WS2Y+0.26,0.888], color=0x333333, mass=0)
bb.createBody(shape="box", halfExtent=[0.17,0.075,0.010],
    position=[WS2X,WS2Y-0.02,0.778], color=0x1a1a1a, mass=0)
bb.createBody(shape="box", halfExtent=[0.20,0.20,0.040],
    position=[WS2X,WS2Y-0.80,0.58], color=0x336699, mass=0)
for sdx,sdy in [(-0.15,-0.15),(-0.15,0.15),(0.15,-0.15),(0.15,0.15)]:
    bb.createBody(shape="box", halfExtent=[0.025,0.025,0.29],
        position=[WS2X+sdx,WS2Y-0.80+sdy,0.29], color=0x777777, mass=0)

# ============================================================
# MEDICATION PREPARATION COUNTER  — STATIC
# ============================================================
MPX=-2.5; MPY=-RW/2+0.28
bb.createBody(shape="box", halfExtent=[0.70,0.26,0.04],
    position=[MPX,MPY,0.90], color=0xf0f0f0, mass=0)
bb.createBody(shape="box", halfExtent=[0.68,0.24,0.44],
    position=[MPX,MPY,0.46], color=0xe8e8e8, mass=0)
for dz4 in [0.22,0.52,0.78]:
    bb.createBody(shape="box", halfExtent=[0.66,0.005,0.09],
        position=[MPX,MPY-0.245,dz4], color=0xd0d0d0, mass=0)
    bb.createBody(shape="box", halfExtent=[0.06,0.015,0.015],
        position=[MPX,MPY-0.262,dz4+0.045], color=0xc0c0c0, mass=0)
for bx5,by5,col in [(-2.7,-3.6,0xffffff),(-2.5,-3.6,0x88ccff),(-2.3,-3.6,0xffee88)]:
    bb.createBody(shape="box", halfExtent=[0.022,0.022,0.042],
        position=[bx5,MPY-0.05,0.98], color=col, mass=0)
    bb.createBody(shape="box", halfExtent=[0.010,0.010,0.010],
        position=[bx5,MPY-0.05,1.032], color=0x888888, mass=0)
bb.createBody(shape="box", halfExtent=[0.045,0.035,0.065],
    position=[MPX+0.55,MPY-0.05,0.985], color=0xffcc00, mass=0)
bb.createBody(shape="box", halfExtent=[0.042,0.032,0.012],
    position=[MPX+0.55,MPY-0.05,1.062], color=0xff8800, mass=0)

# ============================================================
# TABLET / TABLET STAND  — STATIC
# ============================================================
bb.createBody(shape="box", halfExtent=[0.14,0.012,0.20],
    position=[-BL/2-0.20, 0.0, BH+0.40], color=0x222222, mass=0)
bb.createBody(shape="box", halfExtent=[0.12,0.005,0.17],
    position=[-BL/2-0.20, 0.01, BH+0.40], color=0x001a33, mass=0)
for k in range(4):
    bb.createBody(shape="box", halfExtent=[0.09,0.003,0.007],
        position=[-BL/2-0.20,0.016,BH+0.30+k*0.06], color=0x00aaff, mass=0)
bb.createBody(shape="box", halfExtent=[0.012,0.012,0.22],
    position=[-BL/2-0.20,-0.06,BH+0.22], color=0x888888, mass=0)
bb.createBody(shape="box", halfExtent=[0.12,0.10,0.010],
    position=[-BL/2-0.20,-0.06,BH+0.11], color=0x666666, mass=0)

# ============================================================
# NETWORK RACK  — STATIC
# ============================================================
NRX=-4.5; NRY=RW/2-0.5
bb.createBody(shape="box", halfExtent=[0.30,0.28,0.90],
    position=[NRX,NRY,0.90], color=0x1a1a1a, mass=0)
bb.createBody(shape="box", halfExtent=[0.28,0.005,0.88],
    position=[NRX,NRY-0.285,0.90], color=0x111111, mass=0)
for k in range(8):
    bb.createBody(shape="box", halfExtent=[0.26,0.004,0.036],
        position=[NRX,NRY-0.288,0.28+k*0.20], color=0x2244aa, mass=0)
    col_led = 0x00ff44 if k % 3 != 0 else 0xff8800
    bb.createBody(shape="box", halfExtent=[0.006,0.006,0.006],
        position=[NRX-0.22,NRY-0.292,0.30+k*0.20], color=col_led, mass=0)
bb.createBody(shape="box", halfExtent=[0.28,0.04,0.04],
    position=[NRX,NRY-0.25,1.84], color=0x333333, mass=0)

# ============================================================
# EMERGENCY CALL PANEL  — STATIC
# ============================================================
bb.createBody(shape="box", halfExtent=[0.12,0.025,0.18],
    position=[dw/2+0.55, RW/2-0.025, 1.60], color=0xffffff, mass=0)
bb.createBody(shape="box", halfExtent=[0.10,0.010,0.16],
    position=[dw/2+0.55, RW/2-0.030, 1.60], color=0xffe0e0, mass=0)
bb.createBody(shape="box", halfExtent=[0.06,0.015,0.06],
    position=[dw/2+0.55, RW/2-0.038, 1.70], color=0xff0000, mass=0)
bb.createBody(shape="box", halfExtent=[0.06,0.015,0.04],
    position=[dw/2+0.55, RW/2-0.038, 1.54], color=0x00aa00, mass=0)

# ============================================================
# VACUUM ROBOT  (animated)
# ============================================================
vac_x=-3.5; vac_y=-3.0
vac_body = bb.createBody(shape="box", halfExtent=[0.17,0.17,0.045],
    position=[vac_x,vac_y,0.045], color=0x2c2c2c, mass=0)
bb.createBody(shape="box", halfExtent=[0.10,0.10,0.025],
    position=[vac_x,vac_y,0.115], color=0x444444, mass=0)
vac_light = bb.createBody(shape="box", halfExtent=[0.025,0.025,0.018],
    position=[vac_x,vac_y,0.14], color=0x00ff44, mass=0)
bb.createBody(shape="box", halfExtent=[0.155,0.016,0.028],
    position=[vac_x,vac_y-0.168,0.028], color=0x555555, mass=0)
vac_path=[[-3.5,-3.0],[3.5,-3.0],[3.5,-1.5],[1.5,-1.5],
          [1.5,3.0],[-1.5,3.0],[-1.5,-1.5],[-3.5,-1.5],
          [-3.5,3.0],[3.5,3.0],[3.5,1.5],[-3.5,1.5],[-3.5,-3.0]]
vac_wp=0; vac_spd=0.018

# ============================================================
#  DA VINCI SURGICAL ROBOT  (animated)
# ============================================================
SRX = 2.8; SRY = 2.2

bb.createBody(shape="box", halfExtent=[0.80,0.45,0.38],
    position=[SRX, SRY, 0.38], color=0xd8dde0, mass=0)
bb.createBody(shape="box", halfExtent=[0.78,0.43,0.025],
    position=[SRX, SRY, 0.78], color=0x88ccaa, mass=0)
for tlx, tly in [(-0.65,-0.35),(-0.65,0.35),(0.65,-0.35),(0.65,0.35)]:
    bb.createBody(shape="box", halfExtent=[0.04,0.04,0.38],
        position=[SRX+tlx, SRY+tly, 0.38], color=0x888888, mass=0)
bb.createBody(shape="box", halfExtent=[0.20,0.15,0.003],
    position=[SRX, SRY, 0.808], color=0xffcccc, mass=0)
try:
    bb.createDebugText("", [SRX, SRY-0.8, 2.2],
        color='blue', size=0.9)
except: pass

bb.createBody(shape="box", halfExtent=[0.18,0.18,0.95],
    position=[SRX, SRY+0.75, 0.95], color=0x2a2a3e, mass=0)
bb.createBody(shape="box", halfExtent=[0.22,0.22,0.03],
    position=[SRX, SRY+0.75, 1.93], color=0x3a3a4e, mass=0)
bb.createBody(shape="box", halfExtent=[0.28,0.28,0.04],
    position=[SRX, SRY+0.75, 0.04], color=0x444444, mass=0)
for lz in [0.5, 1.0, 1.5]:
    bb.createBody(shape="box", halfExtent=[0.008,0.008,0.008],
        position=[SRX-0.19, SRY+0.75, lz], color=0x00ff44, mass=0)

s1_shoulder = bb.createBody(shape="box", halfExtent=[0.06,0.06,0.06],
    position=[SRX-0.15, SRY+0.75, 1.90], color=0x555577, mass=0)
s1_upper = bb.createBody(shape="box", halfExtent=[0.025,0.025,0.28],
    position=[SRX-0.30, SRY+0.30, 1.60], color=0x6666aa, mass=0)
s1_lower = bb.createBody(shape="box", halfExtent=[0.020,0.020,0.22],
    position=[SRX-0.20, SRY+0.05, 1.20], color=0x6666aa, mass=0)
s1_tool  = bb.createBody(shape="box", halfExtent=[0.008,0.008,0.12],
    position=[SRX-0.10, SRY, 0.95], color=0xcccccc, mass=0)
s1_grip_L = bb.createBody(shape="box", halfExtent=[0.015,0.004,0.025],
    position=[SRX-0.10, SRY-0.01, 0.82], color=0xaaaacc, mass=0)
s1_grip_R = bb.createBody(shape="box", halfExtent=[0.015,0.004,0.025],
    position=[SRX-0.10, SRY+0.01, 0.82], color=0xaaaacc, mass=0)

s2_shoulder = bb.createBody(shape="box", halfExtent=[0.06,0.06,0.06],
    position=[SRX+0.15, SRY+0.75, 1.90], color=0x555577, mass=0)
s2_upper = bb.createBody(shape="box", halfExtent=[0.025,0.025,0.28],
    position=[SRX+0.30, SRY+0.30, 1.60], color=0x6666aa, mass=0)
s2_lower = bb.createBody(shape="box", halfExtent=[0.020,0.020,0.22],
    position=[SRX+0.20, SRY+0.05, 1.20], color=0x6666aa, mass=0)
s2_tool  = bb.createBody(shape="box", halfExtent=[0.008,0.008,0.12],
    position=[SRX+0.10, SRY, 0.95], color=0xcccccc, mass=0)
s2_grip_L = bb.createBody(shape="box", halfExtent=[0.015,0.004,0.025],
    position=[SRX+0.10, SRY-0.01, 0.82], color=0xaaaacc, mass=0)
s2_grip_R = bb.createBody(shape="box", halfExtent=[0.015,0.004,0.025],
    position=[SRX+0.10, SRY+0.01, 0.82], color=0xaaaacc, mass=0)

s3_shoulder = bb.createBody(shape="box", halfExtent=[0.05,0.05,0.05],
    position=[SRX, SRY+0.75, 1.90], color=0x555577, mass=0)
s3_boom = bb.createBody(shape="box", halfExtent=[0.018,0.018,0.35],
    position=[SRX, SRY+0.30, 1.55], color=0x888888, mass=0)
s3_cam  = bb.createBody(shape="box", halfExtent=[0.03,0.03,0.04],
    position=[SRX, SRY, 1.10], color=0x222222, mass=0)
s3_lens = bb.createBody(shape="box", halfExtent=[0.015,0.015,0.008],
    position=[SRX, SRY, 1.05], color=0x4488ff, mass=0)

SCX = SRX + 1.5; SCY = SRY
bb.createBody(shape="box", halfExtent=[0.50,0.45,0.50],
    position=[SCX, SCY, 0.50], color=0x2a2a3e, mass=0)
bb.createBody(shape="box", halfExtent=[0.48,0.43,0.025],
    position=[SCX, SCY, 1.025], color=0x333355, mass=0)
bb.createBody(shape="box", halfExtent=[0.25,0.08,0.20],
    position=[SCX-0.10, SCY-0.35, 1.25], color=0x1a1a2e, mass=0)
bb.createBody(shape="box", halfExtent=[0.22,0.04,0.16],
    position=[SCX-0.10, SCY-0.38, 1.25], color=0x003322, mass=0)
for mx in [-0.20, 0.20]:
    bb.createBody(shape="box", halfExtent=[0.04,0.08,0.03],
        position=[SCX+mx, SCY-0.15, 1.06], color=0x444466, mass=0)
    bb.createBody(shape="box", halfExtent=[0.015,0.015,0.10],
        position=[SCX+mx, SCY-0.15, 1.16], color=0x888888, mass=0)

VCX = SRX - 1.2; VCY = SRY + 0.5
bb.createBody(shape="box", halfExtent=[0.30,0.25,0.55],
    position=[VCX, VCY, 0.55], color=0x222233, mass=0)
bb.createBody(shape="box", halfExtent=[0.36,0.04,0.26],
    position=[VCX, VCY-0.22, 1.36], color=0x111111, mass=0)
bb.createBody(shape="box", halfExtent=[0.33,0.02,0.23],
    position=[VCX, VCY-0.24, 1.36], color=0x002211, mass=0)
for vk in range(5):
    bb.createBody(shape="box", halfExtent=[0.28,0.005,0.006],
        position=[VCX, VCY-0.255, 1.18+vk*0.08], color=0x00ffaa, mass=0)
bb.createBody(shape="box", halfExtent=[0.02,0.02,0.15],
    position=[VCX, VCY-0.22, 1.05], color=0x333333, mass=0)

# ============================================================
# LOKOMAT ROBOTIC REHABILITATION EXOSKELETON  (animated)
# ============================================================
LKX = -3.0; LKY = 2.0
try:
    bb.createDebugText("", [LKX, LKY-0.8, 2.2],
        color='orange', size=0.9)
except: pass

bb.createBody(shape="box", halfExtent=[0.50,0.35,0.12],
    position=[LKX, LKY, 0.12], color=0x333333, mass=0)
bb.createBody(shape="box", halfExtent=[0.48,0.30,0.008],
    position=[LKX, LKY, 0.248], color=0x2a2a2a, mass=0)
for lk in range(-2, 3):
    bb.createBody(shape="box", halfExtent=[0.005,0.28,0.002],
        position=[LKX+lk*0.15, LKY, 0.258], color=0x444444, mass=0)
for rs in [-1, 1]:
    bb.createBody(shape="box", halfExtent=[0.55,0.03,0.06],
        position=[LKX, LKY+rs*0.38, 0.55], color=0xaaaaaa, mass=0)
    bb.createBody(shape="box", halfExtent=[0.03,0.03,0.30],
        position=[LKX-0.50, LKY+rs*0.38, 0.40], color=0xaaaaaa, mass=0)
    bb.createBody(shape="box", halfExtent=[0.03,0.03,0.30],
        position=[LKX+0.50, LKY+rs*0.38, 0.40], color=0xaaaaaa, mass=0)

for ps in [-1, 1]:
    bb.createBody(shape="box", halfExtent=[0.05,0.05,1.20],
        position=[LKX+ps*0.55, LKY-0.35, 1.20], color=0x888888, mass=0)
bb.createBody(shape="box", halfExtent=[0.60,0.06,0.05],
    position=[LKX, LKY-0.35, 2.45], color=0x888888, mass=0)
bb.createBody(shape="box", halfExtent=[0.08,0.08,0.10],
    position=[LKX, LKY-0.35, 2.35], color=0x444444, mass=0)
bb.createBody(shape="box", halfExtent=[0.005,0.005,0.45],
    position=[LKX, LKY-0.10, 1.80], color=0x222222, mass=0)
bb.createBody(shape="box", halfExtent=[0.14,0.10,0.18],
    position=[LKX, LKY, 1.35], color=0x3366aa, mass=0)
for hs in [-1, 1]:
    bb.createBody(shape="box", halfExtent=[0.02,0.005,0.22],
        position=[LKX+hs*0.10, LKY-0.05, 1.55], color=0x3355aa, mass=0)

bb.createBody(shape="box", halfExtent=[0.13,0.09,0.25],
    position=[LKX, LKY, 1.35], color=0xeeddcc, mass=0)
bb.createBody(shape="box", halfExtent=[0.08,0.08,0.10],
    position=[LKX, LKY, 1.70], color=0xeeddcc, mass=0)
for sa in [-1, 1]:
    bb.createBody(shape="box", halfExtent=[0.04,0.04,0.22],
        position=[LKX+sa*0.20, LKY, 1.20], color=0xeeddcc, mass=0)

bb.createBody(shape="box", halfExtent=[0.18,0.12,0.06],
    position=[LKX, LKY, 1.05], color=0x666688, mass=0)

lk_L_thigh = bb.createBody(shape="box", halfExtent=[0.035,0.035,0.22],
    position=[LKX-0.10, LKY, 0.78], color=0x4488cc, mass=0)
lk_L_shank = bb.createBody(shape="box", halfExtent=[0.030,0.030,0.20],
    position=[LKX-0.10, LKY, 0.38], color=0x4488cc, mass=0)
lk_L_foot  = bb.createBody(shape="box", halfExtent=[0.06,0.035,0.02],
    position=[LKX-0.10, LKY, 0.27], color=0x333355, mass=0)
lk_R_thigh = bb.createBody(shape="box", halfExtent=[0.035,0.035,0.22],
    position=[LKX+0.10, LKY, 0.78], color=0x4488cc, mass=0)
lk_R_shank = bb.createBody(shape="box", halfExtent=[0.030,0.030,0.20],
    position=[LKX+0.10, LKY, 0.38], color=0x4488cc, mass=0)
lk_R_foot  = bb.createBody(shape="box", halfExtent=[0.06,0.035,0.02],
    position=[LKX+0.10, LKY, 0.27], color=0x333355, mass=0)

for mx2 in [-0.10, 0.10]:
    bb.createBody(shape="box", halfExtent=[0.04,0.05,0.04],
        position=[LKX+mx2, LKY-0.06, 1.02], color=0x555577, mass=0)
lk_L_knee_motor = bb.createBody(shape="box", halfExtent=[0.035,0.04,0.035],
    position=[LKX-0.10, LKY-0.04, 0.58], color=0x555577, mass=0)
lk_R_knee_motor = bb.createBody(shape="box", halfExtent=[0.035,0.04,0.035],
    position=[LKX+0.10, LKY-0.04, 0.58], color=0x555577, mass=0)

belt_markers = []
for bm in range(6):
    m = bb.createBody(shape="box", halfExtent=[0.005,0.28,0.003],
        position=[LKX-0.40+bm*0.16, LKY, 0.254], color=0x555555, mass=0)
    belt_markers.append(m)
belt_offset = 0.0

bb.createBody(shape="box", halfExtent=[0.15,0.04,0.25],
    position=[LKX+0.65, LKY, 1.25], color=0x222233, mass=0)
bb.createBody(shape="box", halfExtent=[0.13,0.02,0.20],
    position=[LKX+0.65, LKY-0.045, 1.25], color=0x001a1a, mass=0)
for ck in range(4):
    bb.createBody(shape="box", halfExtent=[0.10,0.005,0.006],
        position=[LKX+0.65, LKY-0.055, 1.10+ck*0.08], color=0x00ddff, mass=0)
bb.createBody(shape="box", halfExtent=[0.05,0.005,0.03],
    position=[LKX+0.65, LKY-0.055, 1.40], color=0x00ff88, mass=0)
bb.createBody(shape="box", halfExtent=[0.025,0.025,0.025],
    position=[LKX+0.65, LKY-0.02, 1.52], color=0xff0000, mass=0)

LK_HIP_HEIGHT  = 1.05
LK_THIGH_LEN   = 0.44
LK_SHANK_LEN   = 0.40
LK_GAIT_SPEED  = 0.8
LK_HIP_AMP     = 0.35
LK_KNEE_AMP    = 0.45
LK_BELT_SPEED  = 0.004

# ============================================================
# OUTSIDE ENHANCEMENTS
# ============================================================

# ── Ground / Parking Lot outside front ────────────────────────
bb.createBody(shape="box", halfExtent=[8.0, 4.0, 0.02],
    position=[0, RW/2+4.2, -0.02], color=0x555555, mass=0)
# parking lines
for pk in range(-3, 4):
    bb.createBody(shape="box", halfExtent=[0.02, 1.8, 0.003],
        position=[pk*2.0, RW/2+4.2, 0.003], color=0xffffff, mass=0)
# lane centre line (dashed)
for dl in range(-7, 8):
    bb.createBody(shape="box", halfExtent=[0.35, 0.02, 0.003],
        position=[dl*1.0, RW/2+2.1, 0.003], color=0xffcc00, mass=0)

# ── Parked vehicles (simple box cars) ────────────────────────
car_colors = [0x2244aa, 0xcc2222, 0x22aa44, 0x888888, 0xeeeeee]
for ci, cx in enumerate([-4.0, -2.0, 2.0, 4.0]):
    cy = RW/2 + 5.0
    cc = car_colors[ci % len(car_colors)]
    bb.createBody(shape="box", halfExtent=[0.70, 0.40, 0.35],
        position=[cx, cy, 0.35], color=cc, mass=0)
    bb.createBody(shape="box", halfExtent=[0.40, 0.38, 0.22],
        position=[cx+0.05, cy, 0.72], color=cc, mass=0)
    # windshield
    bb.createBody(shape="box", halfExtent=[0.02, 0.34, 0.18],
        position=[cx-0.35, cy, 0.72], color=0x88ccee, mass=0)
    # wheels
    for wx5, wy5 in [(-0.45,-0.40),(-0.45,0.40),(0.45,-0.40),(0.45,0.40)]:
        bb.createBody(shape="box", halfExtent=[0.08, 0.05, 0.10],
            position=[cx+wx5, cy+wy5, 0.10], color=0x111111, mass=0)

# ── Ambulance Bay ─────────────────────────────────────────────
AMB_X = 0.0; AMB_Y = RW/2 + 2.8
# ambulance body
bb.createBody(shape="box", halfExtent=[1.20, 0.55, 0.55],
    position=[AMB_X, AMB_Y, 0.55], color=0xffffff, mass=0)
# red stripe
bb.createBody(shape="box", halfExtent=[1.22, 0.56, 0.04],
    position=[AMB_X, AMB_Y, 0.72], color=0xff2222, mass=0)
# cab
bb.createBody(shape="box", halfExtent=[0.45, 0.53, 0.35],
    position=[AMB_X-1.00, AMB_Y, 0.85], color=0xffffff, mass=0)
# windshield
bb.createBody(shape="box", halfExtent=[0.02, 0.48, 0.28],
    position=[AMB_X-1.45, AMB_Y, 0.90], color=0x88ccee, mass=0)
# wheels
for awx, awy in [(-0.85,-0.55),(-0.85,0.55),(0.70,-0.55),(0.70,0.55)]:
    bb.createBody(shape="box", halfExtent=[0.12, 0.06, 0.14],
        position=[AMB_X+awx, AMB_Y+awy, 0.14], color=0x111111, mass=0)
# cross symbol on side
bb.createBody(shape="box", halfExtent=[0.06, 0.005, 0.16],
    position=[AMB_X+0.5, AMB_Y-0.56, 0.72], color=0xff2222, mass=0)
bb.createBody(shape="box", halfExtent=[0.16, 0.005, 0.06],
    position=[AMB_X+0.5, AMB_Y-0.56, 0.72], color=0xff2222, mass=0)
# animated flashing lights on roof
amb_light_L = bb.createBody(shape="box", halfExtent=[0.06, 0.06, 0.04],
    position=[AMB_X-0.75, AMB_Y-0.15, 1.24], color=0xff0000, mass=0)
amb_light_R = bb.createBody(shape="box", halfExtent=[0.06, 0.06, 0.04],
    position=[AMB_X-0.75, AMB_Y+0.15, 1.24], color=0x0000ff, mass=0)
# light bar base
bb.createBody(shape="box", halfExtent=[0.12, 0.22, 0.02],
    position=[AMB_X-0.75, AMB_Y, 1.20], color=0xdddddd, mass=0)

# ── Emergency entrance canopy ─────────────────────────────────
for cpx2 in [-2.0, 2.0]:
    bb.createBody(shape="box", halfExtent=[0.06, 0.06, 1.8],
        position=[cpx2, RW/2+0.8, 1.8], color=0x888888, mass=0)
bb.createBody(shape="box", halfExtent=[2.2, 1.0, 0.04],
    position=[0, RW/2+0.8, 3.60], color=0xe0e0e0, mass=0)
# canopy edge stripe
bb.createBody(shape="box", halfExtent=[2.2, 0.02, 0.06],
    position=[0, RW/2+1.8, 3.56], color=0xff2222, mass=0)
try:
    bb.createDebugText("EMERGENCY", [0, RW/2+1.82, 3.4],
        color='red', size=0.8)
except: pass

# ── Helipad ───────────────────────────────────────────────────
HELI_X = -5.0; HELI_Y = RW/2 + 6.0
bb.createBody(shape="box", halfExtent=[2.0, 2.0, 0.03],
    position=[HELI_X, HELI_Y, -0.01], color=0x444444, mass=0)
# H marking
bb.createBody(shape="box", halfExtent=[0.08, 0.65, 0.005],
    position=[HELI_X-0.35, HELI_Y, 0.025], color=0xffffff, mass=0)
bb.createBody(shape="box", halfExtent=[0.08, 0.65, 0.005],
    position=[HELI_X+0.35, HELI_Y, 0.025], color=0xffffff, mass=0)
bb.createBody(shape="box", halfExtent=[0.35, 0.08, 0.005],
    position=[HELI_X, HELI_Y, 0.025], color=0xffffff, mass=0)
# circle boundary markers
for ha in range(12):
    angle = ha * math.pi / 6
    hx = HELI_X + 1.7 * math.cos(angle)
    hy = HELI_Y + 1.7 * math.sin(angle)
    bb.createBody(shape="box", halfExtent=[0.06, 0.06, 0.02],
        position=[hx, hy, 0.02], color=0xffcc00, mass=0)
# helipad beacon (animated)
heli_beacon = bb.createBody(shape="box", halfExtent=[0.08, 0.08, 0.06],
    position=[HELI_X, HELI_Y, 0.06], color=0x00ff00, mass=0)

# ── Pathway lamps (along front of building) ──────────────────
lamp_lights = []
for lx3 in [-3.5, -1.5, 1.5, 3.5]:
    ly3 = RW/2 + 1.0
    bb.createBody(shape="box", halfExtent=[0.03, 0.03, 1.0],
        position=[lx3, ly3, 1.0], color=0x555555, mass=0)
    lmp = bb.createBody(shape="box", halfExtent=[0.06, 0.06, 0.04],
        position=[lx3, ly3, 2.04], color=0xffee88, mass=0)
    lamp_lights.append(lmp)
    bb.createBody(shape="box", halfExtent=[0.08, 0.08, 0.01],
        position=[lx3, ly3, 2.0], color=0x444444, mass=0)

# ── Garden area & benches (right side of building) ────────────
# grass patch
bb.createBody(shape="box", halfExtent=[2.5, 1.5, 0.01],
    position=[RL/2+2.8, 0, -0.01], color=0x44aa44, mass=0)
# flower beds
for fb in range(5):
    bb.createBody(shape="box", halfExtent=[0.15, 0.15, 0.08],
        position=[RL/2+1.5+fb*0.8, 1.0, 0.08], color=0x663300, mass=0)
    bb.createBody(shape="box", halfExtent=[0.12, 0.12, 0.06],
        position=[RL/2+1.5+fb*0.8, 1.0, 0.16], color=[0xff4488,0xffaa22,0xff66cc,0xaa44ff,0xff8844][fb], mass=0)
# benches
for bx6 in [RL/2+2.0, RL/2+3.5]:
    # seat
    bb.createBody(shape="box", halfExtent=[0.35, 0.18, 0.02],
        position=[bx6, -0.5, 0.45], color=0x8b6343, mass=0)
    # backrest
    bb.createBody(shape="box", halfExtent=[0.35, 0.02, 0.18],
        position=[bx6, -0.68, 0.63], color=0x8b6343, mass=0)
    # legs
    for blx, bly in [(-0.28,-0.12),(0.28,-0.12),(-0.28,0.12),(0.28,0.12)]:
        bb.createBody(shape="box", halfExtent=[0.02, 0.02, 0.22],
            position=[bx6+blx, -0.5+bly, 0.22], color=0x444444, mass=0)
# tree
bb.createBody(shape="box", halfExtent=[0.08, 0.08, 0.8],
    position=[RL/2+2.8, -1.0, 0.8], color=0x5c4033, mass=0)
bb.createBody(shape="box", halfExtent=[0.45, 0.45, 0.35],
    position=[RL/2+2.8, -1.0, 1.9], color=0x228b22, mass=0)
bb.createBody(shape="box", halfExtent=[0.35, 0.35, 0.25],
    position=[RL/2+2.8, -1.0, 2.3], color=0x2da02d, mass=0)

# ── Flagpoles ─────────────────────────────────────────────────
for fpx, fpc in [(-3.5, 0xff0000), (-2.5, 0xffffff), (-1.5, 0x0000ff)]:
    fpy = RW/2 + 1.6
    bb.createBody(shape="box", halfExtent=[0.02, 0.02, 2.0],
        position=[fpx, fpy, 2.0], color=0xcccccc, mass=0)
    bb.createBody(shape="box", halfExtent=[0.18, 0.005, 0.12],
        position=[fpx+0.18, fpy, 3.88], color=fpc, mass=0)

# ── Walkway from parking to entrance ─────────────────────────
bb.createBody(shape="box", halfExtent=[1.0, 1.2, 0.005],
    position=[0, RW/2+1.3, 0.005], color=0xccbbaa, mass=0)
# directional arrows on walkway
for ay in [RW/2+0.6, RW/2+1.2, RW/2+1.8]:
    bb.createBody(shape="box", halfExtent=[0.08, 0.02, 0.003],
        position=[0, ay, 0.01], color=0x2266aa, mass=0)
    bb.createBody(shape="box", halfExtent=[0.02, 0.06, 0.003],
        position=[0, ay-0.06, 0.01], color=0x2266aa, mass=0)

# ============================================================
# IMAGING ROOM  (adjacent, right side — 10 x 8 x 4 m)  BIGGER
# ============================================================
# The imaging room is attached to the right wall of the main room.
# It has its own floor, walls, ceiling and a connecting doorway.
IRL = 10.0; IRW = 8.0; IRH = RH
IR_CX = RL/2 + IRL/2 + WT   # centre X of imaging room
IR_CY = 0.0                   # centre Y (aligned with main room)
IR_WALL_T = 0.18

# Floor
bb.createBody(shape="box", halfExtent=[IRL/2, IRW/2, 0.04],
    position=[IR_CX, IR_CY, -0.04], color=0xe8e8f0, mass=0)
# floor tiles
for ti in range(-2, 3):
    bb.createBody(shape="box", halfExtent=[IRL/2, 0.01, 0.002],
        position=[IR_CX, IR_CY+ti*1.0, 0.002], color=0xd0d0dd, mass=0)
for tj in range(-2, 4):
    bb.createBody(shape="box", halfExtent=[0.01, IRW/2, 0.002],
        position=[IR_CX-IRL/2+tj*1.0, IR_CY, 0.002], color=0xd0d0dd, mass=0)

# Ceiling
bb.createBody(shape="box", halfExtent=[IRL/2, IRW/2, 0.04],
    position=[IR_CX, IR_CY, IRH+0.04], color=0xf5f5f5, mass=0)
# ceiling lights
for clx2 in [-2.5, 0.0, 2.5]:
    for cly2 in [-1.5, 1.5]:
        bb.createBody(shape="box", halfExtent=[0.45, 0.22, 0.01],
            position=[IR_CX+clx2, IR_CY+cly2, IRH-0.01], color=0xffffff, mass=0)
        bb.createBody(shape="box", halfExtent=[0.40, 0.18, 0.005],
            position=[IR_CX+clx2, IR_CY+cly2, IRH-0.02], color=0xfffde0, mass=0)

# Walls -- back (far X)
bb.createBody(shape="box", halfExtent=[IR_WALL_T/2, IRW/2, IRH/2],
    position=[IR_CX+IRL/2, IR_CY, IRH/2], color=0xdde0e8, mass=0)
# front (near X) — has connecting doorway to main room
# The connecting door is in the right wall of main room at Y ~ -0.5
IR_DOOR_W = 1.6; IR_DOOR_H = 2.8
# Sections of right wall of main room around the doorway
ir_door_cy = IR_CY
ir_sw_top = (IRH - IR_DOOR_H)
ir_sw_side = (IRW - IR_DOOR_W) / 2
# top above imaging room door (on main room's right wall)
bb.createBody(shape="box", halfExtent=[IR_WALL_T/2, IR_DOOR_W/2, ir_sw_top/2],
    position=[RL/2, ir_door_cy, IR_DOOR_H + ir_sw_top/2], color=0xeae6e0, mass=0)
# side sections of imaging room front wall
bb.createBody(shape="box", halfExtent=[IR_WALL_T/2, ir_sw_side/2, IRH/2],
    position=[IR_CX-IRL/2-IR_WALL_T, IR_CY - IR_DOOR_W/2 - ir_sw_side/2, IRH/2], color=0xdde0e8, mass=0)
bb.createBody(shape="box", halfExtent=[IR_WALL_T/2, ir_sw_side/2, IRH/2],
    position=[IR_CX-IRL/2-IR_WALL_T, IR_CY + IR_DOOR_W/2 + ir_sw_side/2, IRH/2], color=0xdde0e8, mass=0)
# top section above imaging room door
bb.createBody(shape="box", halfExtent=[IR_WALL_T/2, IR_DOOR_W/2, ir_sw_top/2],
    position=[IR_CX-IRL/2-IR_WALL_T, IR_CY, IR_DOOR_H + ir_sw_top/2], color=0xdde0e8, mass=0)
# door frame
for dfx in [-IR_DOOR_W/2, IR_DOOR_W/2]:
    bb.createBody(shape="box", halfExtent=[0.04, 0.05, IR_DOOR_H/2],
        position=[IR_CX-IRL/2-IR_WALL_T, IR_CY+dfx, IR_DOOR_H/2], color=0xb89a78, mass=0)
bb.createBody(shape="box", halfExtent=[0.04, IR_DOOR_W/2, 0.04],
    position=[IR_CX-IRL/2-IR_WALL_T, IR_CY, IR_DOOR_H], color=0xb89a78, mass=0)

# Side walls (top & bottom Y)
bb.createBody(shape="box", halfExtent=[IRL/2, IR_WALL_T/2, IRH/2],
    position=[IR_CX, IR_CY-IRW/2, IRH/2], color=0xdde0e8, mass=0)
bb.createBody(shape="box", halfExtent=[IRL/2, IR_WALL_T/2, IRH/2],
    position=[IR_CX, IR_CY+IRW/2, IRH/2], color=0xdde0e8, mass=0)

# Room sign
bb.createBody(shape="box", halfExtent=[0.60, 0.04, 0.12],
    position=[IR_CX-IRL/2-IR_WALL_T, IR_CY, IR_DOOR_H+0.16], color=0x2255aa, mass=0)
try:
    bb.createDebugText("IMAGING", [IR_CX-IRL/2-IR_WALL_T+0.05, IR_CY, IR_DOOR_H+0.16],
        color='white', size=0.7)
except: pass

# Lead-lined stripe (radiation shielding indicator)
for lsy in [IR_CY-IRW/2, IR_CY+IRW/2]:
    bb.createBody(shape="box", halfExtent=[IRL/2, 0.01, 0.04],
        position=[IR_CX, lsy, 1.2], color=0x555555, mass=0)

# ── Radiation warning signs ──────────────────────────────────
for wsx2, wsy2 in [(IR_CX+IRL/2-0.02, IR_CY), (IR_CX, IR_CY-IRW/2+0.02)]:
    bb.createBody(shape="box", halfExtent=[0.10, 0.005, 0.10],
        position=[wsx2, wsy2, 1.8], color=0xffcc00, mass=0)
    bb.createBody(shape="box", halfExtent=[0.04, 0.006, 0.04],
        position=[wsx2, wsy2, 1.8], color=0x111111, mass=0)

# ============================================================
# MRI SCANNER  (inside imaging room — animated)
# ============================================================
MRI_X = IR_CX + 2.0; MRI_Y = IR_CY - 1.0

# Main bore housing (outer shell)
bb.createBody(shape="box", halfExtent=[0.75, 0.70, 0.70],
    position=[MRI_X, MRI_Y, 0.90], color=0xeeeef5, mass=0)
# bore tunnel (darker centre, visual contrast)
bb.createBody(shape="box", halfExtent=[0.78, 0.32, 0.32],
    position=[MRI_X, MRI_Y, 0.90], color=0x333344, mass=0)
# inner bore lining
bb.createBody(shape="box", halfExtent=[0.80, 0.28, 0.28],
    position=[MRI_X, MRI_Y, 0.90], color=0x555566, mass=0)
# front ring detail
bb.createBody(shape="box", halfExtent=[0.02, 0.68, 0.68],
    position=[MRI_X-0.75, MRI_Y, 0.90], color=0xccccdd, mass=0)
bb.createBody(shape="box", halfExtent=[0.02, 0.30, 0.30],
    position=[MRI_X-0.75, MRI_Y, 0.90], color=0x444455, mass=0)
# back ring detail
bb.createBody(shape="box", halfExtent=[0.02, 0.68, 0.68],
    position=[MRI_X+0.75, MRI_Y, 0.90], color=0xccccdd, mass=0)
# base platform
bb.createBody(shape="box", halfExtent=[0.80, 0.75, 0.10],
    position=[MRI_X, MRI_Y, 0.10], color=0xdddddd, mass=0)

# MRI Patient Table (animated — slides in and out)
mri_table_base = bb.createBody(shape="box", halfExtent=[0.75, 0.22, 0.04],
    position=[MRI_X-1.5, MRI_Y, 0.50], color=0xdedede, mass=0)
mri_table_pad = bb.createBody(shape="box", halfExtent=[0.70, 0.20, 0.03],
    position=[MRI_X-1.5, MRI_Y, 0.57], color=0xf0f8ff, mass=0)
# table rail
mri_table_rail_L = bb.createBody(shape="box", halfExtent=[0.75, 0.01, 0.015],
    position=[MRI_X-1.5, MRI_Y-0.22, 0.48], color=0xaaaaaa, mass=0)
mri_table_rail_R = bb.createBody(shape="box", halfExtent=[0.75, 0.01, 0.015],
    position=[MRI_X-1.5, MRI_Y+0.22, 0.48], color=0xaaaaaa, mass=0)
# patient body on table (moves with table)
mri_patient_torso = bb.createBody(shape="box", halfExtent=[0.25, 0.14, 0.07],
    position=[MRI_X-1.5, MRI_Y, 0.67], color=0xeeddcc, mass=0)
mri_patient_head = bb.createBody(shape="box", halfExtent=[0.08, 0.08, 0.08],
    position=[MRI_X-1.3, MRI_Y, 0.72], color=0xeeddcc, mass=0)
mri_patient_legs = bb.createBody(shape="box", halfExtent=[0.30, 0.10, 0.06],
    position=[MRI_X-1.9, MRI_Y, 0.65], color=0x4488cc, mass=0)

# Animated magnetic ring (spins around bore)
mri_ring_H = bb.createBody(shape="box", halfExtent=[0.02, 0.55, 0.04],
    position=[MRI_X, MRI_Y, 0.90], color=0x6688ff, mass=0)
mri_ring_V = bb.createBody(shape="box", halfExtent=[0.02, 0.04, 0.55],
    position=[MRI_X, MRI_Y, 0.90], color=0x6688ff, mass=0)
mri_ring2_H = bb.createBody(shape="box", halfExtent=[0.02, 0.50, 0.04],
    position=[MRI_X+0.15, MRI_Y, 0.90], color=0x8888dd, mass=0)
mri_ring2_V = bb.createBody(shape="box", halfExtent=[0.02, 0.04, 0.50],
    position=[MRI_X+0.15, MRI_Y, 0.90], color=0x8888dd, mass=0)

# MRI control console
MRI_CON_X = MRI_X - 2.5; MRI_CON_Y = MRI_Y - 1.2
bb.createBody(shape="box", halfExtent=[0.45, 0.30, 0.40],
    position=[MRI_CON_X, MRI_CON_Y, 0.40], color=0x333344, mass=0)
bb.createBody(shape="box", halfExtent=[0.43, 0.28, 0.02],
    position=[MRI_CON_X, MRI_CON_Y, 0.82], color=0x444455, mass=0)
# monitor
bb.createBody(shape="box", halfExtent=[0.30, 0.04, 0.22],
    position=[MRI_CON_X, MRI_CON_Y-0.26, 1.18], color=0x111122, mass=0)
bb.createBody(shape="box", halfExtent=[0.27, 0.02, 0.18],
    position=[MRI_CON_X, MRI_CON_Y-0.28, 1.18], color=0x001a33, mass=0)
# MRI scan lines on screen (animated)
mri_scan_line = bb.createBody(shape="box", halfExtent=[0.24, 0.005, 0.005],
    position=[MRI_CON_X, MRI_CON_Y-0.30, 1.10], color=0x00ffaa, mass=0)
# keyboard
bb.createBody(shape="box", halfExtent=[0.20, 0.10, 0.012],
    position=[MRI_CON_X, MRI_CON_Y, 0.845], color=0x1a1a2e, mass=0)
# status LED
mri_status_led = bb.createBody(shape="box", halfExtent=[0.012, 0.012, 0.012],
    position=[MRI_CON_X+0.35, MRI_CON_Y-0.18, 0.84], color=0x00ff00, mass=0)

MRI_TABLE_OUT = MRI_X - 1.5   # table fully out (patient visible)
MRI_TABLE_IN  = MRI_X         # table fully inside bore
MRI_SLIDE_SPEED = 0.3
MRI_RING_SPEED  = 2.5
MRI_SCAN_CYCLE  = 18.0        # seconds per full scan cycle

# ============================================================
# X-RAY MACHINE  (inside imaging room — animated)
# ============================================================
XR_X = IR_CX - 2.0; XR_Y = IR_CY + 1.5

# Floor-mounted column
bb.createBody(shape="box", halfExtent=[0.15, 0.15, 0.08],
    position=[XR_X, XR_Y, 0.08], color=0x888888, mass=0)
bb.createBody(shape="box", halfExtent=[0.06, 0.06, 1.20],
    position=[XR_X, XR_Y, 1.20], color=0xaaaaaa, mass=0)
# top rail
bb.createBody(shape="box", halfExtent=[0.08, 0.08, 0.05],
    position=[XR_X, XR_Y, 2.40], color=0x777777, mass=0)

# Animated swinging arm + X-ray emitter head
xr_arm = bb.createBody(shape="box", halfExtent=[0.40, 0.025, 0.025],
    position=[XR_X+0.4, XR_Y, 2.30], color=0x888899, mass=0)
xr_head = bb.createBody(shape="box", halfExtent=[0.10, 0.10, 0.08],
    position=[XR_X+0.80, XR_Y, 2.22], color=0x444455, mass=0)
# X-ray beam indicator (animated visibility — pulses)
xr_beam = bb.createBody(shape="box", halfExtent=[0.06, 0.06, 0.40],
    position=[XR_X+0.80, XR_Y, 1.70], color=0x44aaff, mass=0)
# lens/emitter detail
bb.createBody(shape="box", halfExtent=[0.04, 0.04, 0.01],
    position=[XR_X+0.80, XR_Y, 2.14], color=0x888888, mass=0)

# Patient table for X-ray
bb.createBody(shape="box", halfExtent=[0.60, 0.30, 0.03],
    position=[XR_X+0.3, XR_Y, 0.75], color=0xdddddd, mass=0)
# table legs
for tlx2, tly2 in [(-0.50,-0.25),(0.50,-0.25),(-0.50,0.25),(0.50,0.25)]:
    bb.createBody(shape="box", halfExtent=[0.025, 0.025, 0.375],
        position=[XR_X+0.3+tlx2, XR_Y+tly2, 0.375], color=0x999999, mass=0)
# patient pad
bb.createBody(shape="box", halfExtent=[0.55, 0.26, 0.02],
    position=[XR_X+0.3, XR_Y, 0.80], color=0xf0f8ff, mass=0)

# Animated detector panel (under table, moves with arm)
xr_detector = bb.createBody(shape="box", halfExtent=[0.14, 0.14, 0.01],
    position=[XR_X+0.80, XR_Y, 0.72], color=0x222233, mass=0)
# detector detail
bb.createBody(shape="box", halfExtent=[0.12, 0.12, 0.005],
    position=[XR_X+0.80, XR_Y, 0.71], color=0x333355, mass=0)

# X-ray patient (on the X-ray table)
bb.createBody(shape="box", halfExtent=[0.22, 0.12, 0.06],
    position=[XR_X+0.3, XR_Y, 0.88], color=0xeeddcc, mass=0)
bb.createBody(shape="box", halfExtent=[0.07, 0.07, 0.07],
    position=[XR_X+0.6, XR_Y, 0.90], color=0xeeddcc, mass=0)

# X-ray viewer lightbox on wall
XR_VIEW_X = IR_CX - IRL/2 + 0.3
bb.createBody(shape="box", halfExtent=[0.35, 0.015, 0.28],
    position=[XR_VIEW_X, IR_CY-IRW/2+0.02, 1.6], color=0xffffff, mass=0)
bb.createBody(shape="box", halfExtent=[0.30, 0.010, 0.24],
    position=[XR_VIEW_X, IR_CY-IRW/2+0.025, 1.6], color=0xccddff, mass=0)
# X-ray film silhouette (ribs)
for rx in range(5):
    bb.createBody(shape="box", halfExtent=[0.005, 0.008, 0.04],
        position=[XR_VIEW_X-0.10+rx*0.05, IR_CY-IRW/2+0.03, 1.6], color=0xffffff, mass=0)
bb.createBody(shape="box", halfExtent=[0.005, 0.008, 0.12],
    position=[XR_VIEW_X, IR_CY-IRW/2+0.03, 1.6], color=0xeeeeff, mass=0)

# X-ray control panel
XR_CTRL_X = XR_X - 0.8; XR_CTRL_Y = XR_Y - 1.5
bb.createBody(shape="box", halfExtent=[0.25, 0.20, 0.55],
    position=[XR_CTRL_X, XR_CTRL_Y, 0.55], color=0x333344, mass=0)
bb.createBody(shape="box", halfExtent=[0.23, 0.18, 0.02],
    position=[XR_CTRL_X, XR_CTRL_Y, 1.12], color=0x444455, mass=0)
# small monitor
bb.createBody(shape="box", halfExtent=[0.18, 0.03, 0.14],
    position=[XR_CTRL_X, XR_CTRL_Y-0.18, 1.40], color=0x111122, mass=0)
bb.createBody(shape="box", halfExtent=[0.15, 0.02, 0.11],
    position=[XR_CTRL_X, XR_CTRL_Y-0.20, 1.40], color=0x001a22, mass=0)
# buttons on control panel
for bk in range(4):
    bb.createBody(shape="box", halfExtent=[0.02, 0.02, 0.015],
        position=[XR_CTRL_X-0.12+bk*0.08, XR_CTRL_Y, 1.14], color=[0x00ff00,0xff0000,0xffaa00,0x0088ff][bk], mass=0)
# exposure indicator (animated)
xr_expose_led = bb.createBody(shape="box", halfExtent=[0.015, 0.015, 0.015],
    position=[XR_CTRL_X+0.18, XR_CTRL_Y-0.10, 1.14], color=0x00ff00, mass=0)

XR_ARM_SWING_SPEED = 0.4
XR_ARM_RANGE = 0.6       # how far arm swings in X
XR_EXPOSE_INTERVAL = 8.0 # seconds between exposures
XR_EXPOSE_DURATION = 1.5 # seconds the beam is "on"

# ── Debug control for MRI/X-ray ──────────────────────────────
bb.addDebugToggle('MRI_Active', True)
bb.addDebugToggle('XRay_Active', True)

# ============================================================
# RECEPTION WARD  (adjacent, left side — 10 x 8 x 4 m)
# ============================================================
# Attached to the left wall of the main room, opposite the imaging room.
REC_L = 10.0; REC_W = 8.0; REC_H = RH
REC_CX = -RL/2 - REC_L/2 - WT   # centre X
REC_CY = 0.0                      # centre Y (aligned)
REC_WT = 0.18

# Floor (polished look)
bb.createBody(shape="box", halfExtent=[REC_L/2, REC_W/2, 0.04],
    position=[REC_CX, REC_CY, -0.04], color=0xf0eeea, mass=0)
# floor tiles
for rti in range(-3, 4):
    bb.createBody(shape="box", halfExtent=[REC_L/2, 0.01, 0.002],
        position=[REC_CX, REC_CY+rti*1.0, 0.002], color=0xddddcc, mass=0)
for rtj in range(-4, 6):
    bb.createBody(shape="box", halfExtent=[0.01, REC_W/2, 0.002],
        position=[REC_CX-REC_L/2+rtj*1.0, REC_CY, 0.002], color=0xddddcc, mass=0)

# Ceiling
bb.createBody(shape="box", halfExtent=[REC_L/2, REC_W/2, 0.04],
    position=[REC_CX, REC_CY, REC_H+0.04], color=0xfafafa, mass=0)

# Ceiling lights
for rcx in [-2.5, 0.0, 2.5]:
    for rcy in [-1.5, 1.5]:
        bb.createBody(shape="box", halfExtent=[0.45, 0.22, 0.008],
            position=[REC_CX+rcx, REC_CY+rcy, REC_H-0.01], color=0xffffff, mass=0)
        bb.createBody(shape="box", halfExtent=[0.42, 0.19, 0.004],
            position=[REC_CX+rcx, REC_CY+rcy, REC_H-0.016], color=0xfffde0, mass=0)

# ── AC Units on ceiling ──────────────────────────────────────
for acx, acy in [(-2.0, 0.0), (2.0, 0.0), (0.0, 2.5), (0.0, -2.5)]:
    # AC body
    bb.createBody(shape="box", halfExtent=[0.40, 0.40, 0.06],
        position=[REC_CX+acx, REC_CY+acy, REC_H-0.06], color=0xf0f0f0, mass=0)
    # AC front grille
    bb.createBody(shape="box", halfExtent=[0.38, 0.38, 0.01],
        position=[REC_CX+acx, REC_CY+acy, REC_H-0.12], color=0xe0e0e0, mass=0)
    # grille slats
    for gs in range(-3, 4):
        bb.createBody(shape="box", halfExtent=[0.35, 0.008, 0.003],
            position=[REC_CX+acx, REC_CY+acy+gs*0.08, REC_H-0.13], color=0xcccccc, mass=0)
    # status light
    bb.createBody(shape="box", halfExtent=[0.008, 0.008, 0.005],
        position=[REC_CX+acx+0.35, REC_CY+acy, REC_H-0.13], color=0x00ff44, mass=0)

# Walls
# Back wall (far -X)
bb.createBody(shape="box", halfExtent=[REC_WT/2, REC_W/2, REC_H/2],
    position=[REC_CX-REC_L/2, REC_CY, REC_H/2], color=0xeae6e0, mass=0)
# Top wall (+Y)
bb.createBody(shape="box", halfExtent=[REC_L/2, REC_WT/2, REC_H/2],
    position=[REC_CX, REC_CY+REC_W/2, REC_H/2], color=0xeae6e0, mass=0)
# Bottom wall (-Y)
bb.createBody(shape="box", halfExtent=[REC_L/2, REC_WT/2, REC_H/2],
    position=[REC_CX, REC_CY-REC_W/2, REC_H/2], color=0xeae6e0, mass=0)
# Front wall (near +X) — doorway connects to main room's left wall
REC_DOOR_W = 2.0; REC_DOOR_H = 2.8
rec_sw_side = (REC_W - REC_DOOR_W) / 2
rec_sw_top = (REC_H - REC_DOOR_H)
# side sections
bb.createBody(shape="box", halfExtent=[REC_WT/2, rec_sw_side/2, REC_H/2],
    position=[REC_CX+REC_L/2+REC_WT, REC_CY - REC_DOOR_W/2 - rec_sw_side/2, REC_H/2], color=0xeae6e0, mass=0)
bb.createBody(shape="box", halfExtent=[REC_WT/2, rec_sw_side/2, REC_H/2],
    position=[REC_CX+REC_L/2+REC_WT, REC_CY + REC_DOOR_W/2 + rec_sw_side/2, REC_H/2], color=0xeae6e0, mass=0)
# top above door on front wall
bb.createBody(shape="box", halfExtent=[REC_WT/2, REC_DOOR_W/2, rec_sw_top/2],
    position=[REC_CX+REC_L/2+REC_WT, REC_CY, REC_DOOR_H + rec_sw_top/2], color=0xeae6e0, mass=0)
# top above door on main room left wall
bb.createBody(shape="box", halfExtent=[REC_WT/2, REC_DOOR_W/2, rec_sw_top/2],
    position=[-RL/2, REC_CY, REC_DOOR_H + rec_sw_top/2], color=0xeae6e0, mass=0)
# door frame
for dfr in [-REC_DOOR_W/2, REC_DOOR_W/2]:
    bb.createBody(shape="box", halfExtent=[0.04, 0.05, REC_DOOR_H/2],
        position=[REC_CX+REC_L/2+REC_WT, REC_CY+dfr, REC_DOOR_H/2], color=0xb89a78, mass=0)
bb.createBody(shape="box", halfExtent=[0.04, REC_DOOR_W/2, 0.04],
    position=[REC_CX+REC_L/2+REC_WT, REC_CY, REC_DOOR_H], color=0xb89a78, mass=0)

# Wall accent stripe
for rsy in [REC_CY-REC_W/2, REC_CY+REC_W/2]:
    bb.createBody(shape="box", halfExtent=[REC_L/2, 0.012, 0.055],
        position=[REC_CX, rsy, 1.2], color=0x2c6fad, mass=0)
bb.createBody(shape="box", halfExtent=[0.012, REC_W/2, 0.055],
    position=[REC_CX-REC_L/2, REC_CY, 1.2], color=0x2c6fad, mass=0)

# Room sign above door
bb.createBody(shape="box", halfExtent=[0.70, 0.04, 0.12],
    position=[REC_CX+REC_L/2+REC_WT, REC_CY, REC_DOOR_H+0.16], color=0x2c6fad, mass=0)
try:
    bb.createDebugText("RECEPTION", [REC_CX+REC_L/2+REC_WT+0.05, REC_CY, REC_DOOR_H+0.16],
        color='white', size=0.7)
except: pass

# Skirting
for rsy2 in [REC_CY-REC_W/2, REC_CY+REC_W/2]:
    bb.createBody(shape="box", halfExtent=[REC_L/2, REC_WT/2, 0.05],
        position=[REC_CX, rsy2, 0.05], color=0xd0ccc5, mass=0)
bb.createBody(shape="box", halfExtent=[REC_WT/2, REC_W/2, 0.05],
    position=[REC_CX-REC_L/2, REC_CY, 0.05], color=0xd0ccc5, mass=0)

# ── Reception Desk (L-shaped counter) ────────────────────────
RD_X = REC_CX + 2.5; RD_Y = REC_CY - 1.5
# main counter front (the long part facing patients)
bb.createBody(shape="box", halfExtent=[1.20, 0.20, 0.55],
    position=[RD_X, RD_Y, 0.55], color=0x5c4033, mass=0)
# counter top surface
bb.createBody(shape="box", halfExtent=[1.22, 0.22, 0.025],
    position=[RD_X, RD_Y, 1.125], color=0xf0e8d8, mass=0)
# side wing of L
bb.createBody(shape="box", halfExtent=[0.20, 0.60, 0.55],
    position=[RD_X+1.20, RD_Y+0.60, 0.55], color=0x5c4033, mass=0)
bb.createBody(shape="box", halfExtent=[0.22, 0.62, 0.025],
    position=[RD_X+1.20, RD_Y+0.60, 1.125], color=0xf0e8d8, mass=0)
# higher front panel (patient-facing)
bb.createBody(shape="box", halfExtent=[1.20, 0.03, 0.18],
    position=[RD_X, RD_Y-0.22, 1.28], color=0x4a3528, mass=0)
# desk sign
bb.createBody(shape="box", halfExtent=[0.40, 0.02, 0.08],
    position=[RD_X, RD_Y-0.25, 1.38], color=0x2c6fad, mass=0)
try:
    bb.createDebugText("RECEPTION", [RD_X, RD_Y-0.28, 1.38],
        color='white', size=0.4)
except: pass

# Computer on desk
bb.createBody(shape="box", halfExtent=[0.20, 0.04, 0.16],
    position=[RD_X-0.4, RD_Y+0.10, 1.30], color=0x111111, mass=0)
bb.createBody(shape="box", halfExtent=[0.18, 0.02, 0.13],
    position=[RD_X-0.4, RD_Y+0.12, 1.30], color=0x001a33, mass=0)
# screen data lines
for sk in range(5):
    bb.createBody(shape="box", halfExtent=[0.14, 0.004, 0.006],
        position=[RD_X-0.4, RD_Y+0.145, 1.20+sk*0.04], color=0x00aaff, mass=0)
# monitor stand
bb.createBody(shape="box", halfExtent=[0.025, 0.025, 0.08],
    position=[RD_X-0.4, RD_Y+0.10, 1.08], color=0x333333, mass=0)
bb.createBody(shape="box", halfExtent=[0.08, 0.06, 0.008],
    position=[RD_X-0.4, RD_Y+0.10, 1.148], color=0x333333, mass=0)
# keyboard
bb.createBody(shape="box", halfExtent=[0.14, 0.06, 0.008],
    position=[RD_X-0.4, RD_Y-0.02, 1.148], color=0x222222, mass=0)
# phone
bb.createBody(shape="box", halfExtent=[0.06, 0.04, 0.03],
    position=[RD_X+0.5, RD_Y+0.08, 1.17], color=0x222222, mass=0)
bb.createBody(shape="box", halfExtent=[0.025, 0.06, 0.015],
    position=[RD_X+0.5, RD_Y+0.16, 1.16], color=0x333333, mass=0)
# paper tray
bb.createBody(shape="box", halfExtent=[0.10, 0.07, 0.02],
    position=[RD_X+0.1, RD_Y+0.08, 1.17], color=0xeeeeee, mass=0)
bb.createBody(shape="box", halfExtent=[0.08, 0.05, 0.012],
    position=[RD_X+0.1, RD_Y+0.08, 1.152], color=0xffffff, mass=0)

# ── Nurse figure (behind the desk) ───────────────────────────
NURSE_X = RD_X; NURSE_Y = RD_Y + 0.50
# body/torso (scrubs)
bb.createBody(shape="box", halfExtent=[0.12, 0.08, 0.22],
    position=[NURSE_X, NURSE_Y, 1.02], color=0x4488cc, mass=0)
# head
bb.createBody(shape="box", halfExtent=[0.07, 0.07, 0.08],
    position=[NURSE_X, NURSE_Y, 1.32], color=0xeeddcc, mass=0)
# hair
bb.createBody(shape="box", halfExtent=[0.075, 0.075, 0.04],
    position=[NURSE_X, NURSE_Y, 1.42], color=0x3a2a1a, mass=0)
bb.createBody(shape="box", halfExtent=[0.04, 0.078, 0.06],
    position=[NURSE_X, NURSE_Y+0.04, 1.36], color=0x3a2a1a, mass=0)
# nurse cap
bb.createBody(shape="box", halfExtent=[0.06, 0.015, 0.035],
    position=[NURSE_X, NURSE_Y-0.06, 1.44], color=0xffffff, mass=0)
bb.createBody(shape="box", halfExtent=[0.02, 0.012, 0.015],
    position=[NURSE_X, NURSE_Y-0.06, 1.46], color=0xff2222, mass=0)
# arms
for nside in [-1, 1]:
    bb.createBody(shape="box", halfExtent=[0.035, 0.035, 0.18],
        position=[NURSE_X+nside*0.16, NURSE_Y, 1.00], color=0x4488cc, mass=0)
    # hands
    bb.createBody(shape="box", halfExtent=[0.03, 0.03, 0.03],
        position=[NURSE_X+nside*0.16, NURSE_Y, 0.80], color=0xeeddcc, mass=0)
# legs
for nside2 in [-1, 1]:
    bb.createBody(shape="box", halfExtent=[0.04, 0.04, 0.24],
        position=[NURSE_X+nside2*0.06, NURSE_Y, 0.56], color=0x4488cc, mass=0)
    bb.createBody(shape="box", halfExtent=[0.05, 0.035, 0.02],
        position=[NURSE_X+nside2*0.06, NURSE_Y-0.02, 0.32], color=0xffffff, mass=0)
# ID badge
bb.createBody(shape="box", halfExtent=[0.025, 0.005, 0.035],
    position=[NURSE_X-0.10, NURSE_Y-0.085, 1.15], color=0xffffff, mass=0)
bb.createBody(shape="box", halfExtent=[0.018, 0.004, 0.010],
    position=[NURSE_X-0.10, NURSE_Y-0.088, 1.17], color=0x2266aa, mass=0)
# stethoscope around neck
bb.createBody(shape="box", halfExtent=[0.005, 0.005, 0.10],
    position=[NURSE_X+0.08, NURSE_Y-0.06, 1.10], color=0x555555, mass=0)
bb.createBody(shape="box", halfExtent=[0.02, 0.02, 0.012],
    position=[NURSE_X+0.08, NURSE_Y-0.06, 0.99], color=0xaaaaaa, mass=0)

# ── Waiting area — chairs with patients ──────────────────────
# 2 rows of 4 chairs, some with patients
CHAIR_POSITIONS = [
    (REC_CX - 2.0, REC_CY - 2.0),
    (REC_CX - 0.5, REC_CY - 2.0),
    (REC_CX + 1.0, REC_CY - 2.0),
    (REC_CX + 2.5, REC_CY - 2.0),
    (REC_CX - 2.0, REC_CY + 2.0),
    (REC_CX - 0.5, REC_CY + 2.0),
    (REC_CX + 1.0, REC_CY + 2.0),
    (REC_CX + 2.5, REC_CY + 2.0),
]

for ci2, (chx, chy) in enumerate(CHAIR_POSITIONS):
    # Chair seat
    bb.createBody(shape="box", halfExtent=[0.22, 0.22, 0.02],
        position=[chx, chy, 0.44], color=0x336699, mass=0)
    # Chair backrest
    bb.createBody(shape="box", halfExtent=[0.22, 0.02, 0.22],
        position=[chx, chy+0.22, 0.66], color=0x336699, mass=0)
    # Chair legs
    for clx3, cly3 in [(-0.18,-0.18),(0.18,-0.18),(-0.18,0.18),(0.18,0.18)]:
        bb.createBody(shape="box", halfExtent=[0.018, 0.018, 0.22],
            position=[chx+clx3, chy+cly3, 0.22], color=0x888888, mass=0)
    # Armrests
    for ars in [-1, 1]:
        bb.createBody(shape="box", halfExtent=[0.018, 0.20, 0.015],
            position=[chx+ars*0.22, chy, 0.56], color=0x888888, mass=0)
        bb.createBody(shape="box", halfExtent=[0.018, 0.018, 0.08],
            position=[chx+ars*0.22, chy-0.16, 0.50], color=0x888888, mass=0)

# Patients sitting in chairs (on chairs 0,1,2,4,5,7)
PATIENT_CHAIRS = [0, 1, 2, 4, 5, 7]
PATIENT_COLORS = [0xeeddcc, 0xd4a574, 0xeeddcc, 0xd4a574, 0xeeddcc, 0xd4a574]
SHIRT_COLORS   = [0x4488cc, 0x22aa44, 0xcc4444, 0xff8800, 0x8844cc, 0x44aaaa]
PANT_COLORS    = [0x333355, 0x444444, 0x2a2a55, 0x334433, 0x555555, 0x333344]

for pi, pci in enumerate(PATIENT_CHAIRS):
    px2, py2 = CHAIR_POSITIONS[pci]
    skin = PATIENT_COLORS[pi]
    shirt = SHIRT_COLORS[pi]
    pant = PANT_COLORS[pi]
    # torso (sitting)
    bb.createBody(shape="box", halfExtent=[0.10, 0.08, 0.18],
        position=[px2, py2, 0.64], color=shirt, mass=0)
    # head
    bb.createBody(shape="box", halfExtent=[0.06, 0.06, 0.07],
        position=[px2, py2, 0.89], color=skin, mass=0)
    # hair
    bb.createBody(shape="box", halfExtent=[0.065, 0.065, 0.03],
        position=[px2, py2, 0.96], color=[0x3a2a1a,0x1a1a1a,0x8b6343,0x3a2a1a,0x1a1a1a,0x5c3a1a][pi], mass=0)
    # upper legs (horizontal on seat)
    for ls in [-1, 1]:
        bb.createBody(shape="box", halfExtent=[0.04, 0.14, 0.035],
            position=[px2+ls*0.06, py2-0.06, 0.475], color=pant, mass=0)
    # lower legs (hanging down)
    for ls2 in [-1, 1]:
        bb.createBody(shape="box", halfExtent=[0.035, 0.035, 0.16],
            position=[px2+ls2*0.06, py2-0.18, 0.28], color=pant, mass=0)
    # feet/shoes
    for ls3 in [-1, 1]:
        bb.createBody(shape="box", halfExtent=[0.04, 0.05, 0.02],
            position=[px2+ls3*0.06, py2-0.22, 0.12], color=0x333333, mass=0)
    # arms
    for as2 in [-1, 1]:
        bb.createBody(shape="box", halfExtent=[0.03, 0.03, 0.14],
            position=[px2+as2*0.14, py2, 0.58], color=shirt, mass=0)
        bb.createBody(shape="box", halfExtent=[0.025, 0.025, 0.025],
            position=[px2+as2*0.14, py2-0.02, 0.43], color=skin, mass=0)

# ── Coffee table in waiting area ──────────────────────────────
for ctx, cty in [(REC_CX-0.5, REC_CY), (REC_CX+1.8, REC_CY)]:
    bb.createBody(shape="box", halfExtent=[0.35, 0.25, 0.02],
        position=[ctx, cty, 0.38], color=0x8b6343, mass=0)
    for tlx4, tly4 in [(-0.28,-0.18),(0.28,-0.18),(-0.28,0.18),(0.28,0.18)]:
        bb.createBody(shape="box", halfExtent=[0.025, 0.025, 0.18],
            position=[ctx+tlx4, cty+tly4, 0.18], color=0x5c4033, mass=0)
    # magazines on table
    for mg in range(3):
        bb.createBody(shape="box", halfExtent=[0.06, 0.04, 0.003],
            position=[ctx-0.10+mg*0.10, cty, 0.405], color=[0xcc4444,0x4488cc,0xff8800][mg], mass=0)

# ── Water dispenser ──────────────────────────────────────────
WD_X = REC_CX - 3.5; WD_Y = REC_CY + REC_W/2 - 0.5
bb.createBody(shape="box", halfExtent=[0.15, 0.15, 0.55],
    position=[WD_X, WD_Y, 0.55], color=0xf0f0f0, mass=0)
bb.createBody(shape="box", halfExtent=[0.14, 0.14, 0.02],
    position=[WD_X, WD_Y, 1.12], color=0xdddddd, mass=0)
# water bottle on top
bb.createBody(shape="box", halfExtent=[0.08, 0.08, 0.16],
    position=[WD_X, WD_Y, 1.28], color=0x88ccff, mass=0)
bb.createBody(shape="box", halfExtent=[0.06, 0.06, 0.02],
    position=[WD_X, WD_Y, 1.12], color=0x88ccff, mass=0)
# taps
bb.createBody(shape="box", halfExtent=[0.025, 0.02, 0.025],
    position=[WD_X, WD_Y-0.16, 0.85], color=0xcc2222, mass=0)
bb.createBody(shape="box", halfExtent=[0.025, 0.02, 0.025],
    position=[WD_X+0.06, WD_Y-0.16, 0.85], color=0x2222cc, mass=0)
# drip tray
bb.createBody(shape="box", halfExtent=[0.08, 0.06, 0.015],
    position=[WD_X+0.03, WD_Y-0.16, 0.70], color=0xaaaaaa, mass=0)

# ── Potted plants ────────────────────────────────────────────
for ppx, ppy in [(REC_CX-3.8, REC_CY-3.2), (REC_CX-3.8, REC_CY+3.2),
                 (REC_CX+3.8, REC_CY-3.2)]:
    bb.createBody(shape="box", halfExtent=[0.12, 0.12, 0.15],
        position=[ppx, ppy, 0.15], color=0x8b4513, mass=0)
    bb.createBody(shape="box", halfExtent=[0.10, 0.10, 0.005],
        position=[ppx, ppy, 0.30], color=0x5c3a1a, mass=0)
    bb.createBody(shape="box", halfExtent=[0.15, 0.15, 0.12],
        position=[ppx, ppy, 0.42], color=0x228b22, mass=0)
    bb.createBody(shape="box", halfExtent=[0.10, 0.10, 0.08],
        position=[ppx, ppy, 0.56], color=0x2da02d, mass=0)

# ── Information board on wall ─────────────────────────────────
bb.createBody(shape="box", halfExtent=[0.55, 0.025, 0.40],
    position=[REC_CX-1.5, REC_CY-REC_W/2+0.025, 1.8], color=0x8b6343, mass=0)
bb.createBody(shape="box", halfExtent=[0.52, 0.015, 0.37],
    position=[REC_CX-1.5, REC_CY-REC_W/2+0.04, 1.8], color=0xeeeedd, mass=0)
# notices pinned
for nk in range(4):
    bb.createBody(shape="box", halfExtent=[0.10, 0.008, 0.12],
        position=[REC_CX-1.9+nk*0.26, REC_CY-REC_W/2+0.05, 1.85],
        color=[0xffeeaa,0xaaddff,0xffbbbb,0xbbffbb][nk], mass=0)
    bb.createBody(shape="box", halfExtent=[0.008, 0.008, 0.008],
        position=[REC_CX-1.9+nk*0.26, REC_CY-REC_W/2+0.06, 1.97],
        color=[0xff2222,0x2222ff,0xff8800,0x22aa22][nk], mass=0)

# ── Wall clock in reception ──────────────────────────────────
bb.createBody(shape="box", halfExtent=[0.16, 0.03, 0.16],
    position=[REC_CX, REC_CY+REC_W/2-0.06, 2.8], color=0xffffff, mass=0)
bb.createBody(shape="box", halfExtent=[0.005, 0.022, 0.08],
    position=[REC_CX, REC_CY+REC_W/2-0.032, 2.84], color=0x333333, mass=0)
bb.createBody(shape="box", halfExtent=[0.07, 0.022, 0.005],
    position=[REC_CX+0.04, REC_CY+REC_W/2-0.032, 2.8], color=0x333333, mass=0)

# ── TV Screen on wall ────────────────────────────────────────
bb.createBody(shape="box", halfExtent=[0.55, 0.03, 0.35],
    position=[REC_CX+2.0, REC_CY+REC_W/2-0.03, 2.2], color=0x111111, mass=0)
bb.createBody(shape="box", halfExtent=[0.52, 0.015, 0.32],
    position=[REC_CX+2.0, REC_CY+REC_W/2-0.04, 2.2], color=0x002244, mass=0)
for tvk in range(3):
    bb.createBody(shape="box", halfExtent=[0.44, 0.005, 0.008],
        position=[REC_CX+2.0, REC_CY+REC_W/2-0.055, 2.0+tvk*0.12], color=0x00aaff, mass=0)
bb.createBody(shape="box", halfExtent=[0.20, 0.005, 0.05],
    position=[REC_CX+2.0, REC_CY+REC_W/2-0.055, 2.38], color=0xff6600, mass=0)

# ============================================================
# ROBOT DOG  (Spot URDF — walks around reception)
# ============================================================
SPOT_START_X = REC_CX; SPOT_START_Y = REC_CY
spot_orn = bb.getQuaternionFromEuler([0, 0, 0])
spot_robot = bb.loadURDF(
    'spot.urdf', position=[SPOT_START_X, SPOT_START_Y, 0.75],
    fixedBase=False
)

# Joint IDs for Spot
SPOT_FL_HIP  = 1;  SPOT_FL_KNEE  = 2
SPOT_FR_HIP  = 4;  SPOT_FR_KNEE  = 5
SPOT_RL_HIP  = 7;  SPOT_RL_KNEE  = 8
SPOT_RR_HIP  = 10; SPOT_RR_KNEE  = 11

# Gait parameters
SPOT_TAU = 8
SPOT_HIP_BASE    = 1.0
SPOT_KNEE_BASE   = -1.8
SPOT_HIP_SWING   = 0.5
SPOT_KNEE_SWING  = 0.8
SPOT_PHASE_DELAY = math.pi / 2
spot_step_i = 0

# Patrol waypoints inside reception room
SPOT_PATROL = [
    [REC_CX - 3.0, REC_CY - 1.0],
    [REC_CX - 3.0, REC_CY + 1.0],
    [REC_CX,        REC_CY + 2.5],
    [REC_CX + 3.0,  REC_CY + 1.0],
    [REC_CX + 3.0,  REC_CY - 1.0],
    [REC_CX,        REC_CY - 2.5],
]
spot_wp = 0
spot_x = SPOT_START_X; spot_y = SPOT_START_Y
SPOT_WALK_SPEED = 0.012

def animate_spot_dog():
    """Animate Spot's legs with a walking gait and move along patrol path."""
    global spot_step_i, spot_wp, spot_x, spot_y

    spot_step_i += 1

    # Front legs
    hip_f = SPOT_HIP_BASE + SPOT_HIP_SWING * math.sin(spot_step_i / SPOT_TAU)
    knee_f = SPOT_KNEE_BASE + SPOT_KNEE_SWING * math.cos(spot_step_i / SPOT_TAU)
    for ji in [SPOT_FL_HIP, SPOT_FR_HIP]:
        bb.setJointMotorControl(spot_robot, ji, targetPosition=hip_f)
    for ji in [SPOT_FL_KNEE, SPOT_FR_KNEE]:
        bb.setJointMotorControl(spot_robot, ji, targetPosition=knee_f)

    # Rear legs (phase-delayed)
    hip_r = SPOT_HIP_BASE + SPOT_HIP_SWING * math.sin(spot_step_i / SPOT_TAU + SPOT_PHASE_DELAY)
    knee_r = SPOT_KNEE_BASE + SPOT_KNEE_SWING * math.cos(spot_step_i / SPOT_TAU + SPOT_PHASE_DELAY)
    for ji in [SPOT_RL_HIP, SPOT_RR_HIP]:
        bb.setJointMotorControl(spot_robot, ji, targetPosition=hip_r)
    for ji in [SPOT_RL_KNEE, SPOT_RR_KNEE]:
        bb.setJointMotorControl(spot_robot, ji, targetPosition=knee_r)

    # Move toward current waypoint
    tgt_x, tgt_y = SPOT_PATROL[spot_wp]
    dx = tgt_x - spot_x; dy = tgt_y - spot_y
    dist = math.sqrt(dx*dx + dy*dy)
    if dist < 0.3:
        spot_wp = (spot_wp + 1) % len(SPOT_PATROL)
    elif dist > 0.01:
        spot_x += (dx/dist) * SPOT_WALK_SPEED
        spot_y += (dy/dist) * SPOT_WALK_SPEED
        heading = math.atan2(dy, dx) - math.pi/2
        try:
            bb.resetBasePose(spot_robot,
                [spot_x, spot_y, 0.75],
                bb.getQuaternionFromEuler([0, 0, heading]))
        except: pass

# ============================================================
# ANIMATION: MRI Scanner
# ============================================================
def animate_mri(t):
    qI = [0, 0, 0, 1]
    cycle_t = (t % MRI_SCAN_CYCLE) / MRI_SCAN_CYCLE  # 0..1

    # Table slides: out for 0-0.25, sliding in 0.25-0.40, inside 0.40-0.75, sliding out 0.75-0.90, out 0.90-1.0
    if cycle_t < 0.25:
        table_x = MRI_TABLE_OUT
    elif cycle_t < 0.40:
        frac = (cycle_t - 0.25) / 0.15
        table_x = MRI_TABLE_OUT + (MRI_TABLE_IN - MRI_TABLE_OUT) * frac
    elif cycle_t < 0.75:
        table_x = MRI_TABLE_IN
    elif cycle_t < 0.90:
        frac = (cycle_t - 0.75) / 0.15
        table_x = MRI_TABLE_IN + (MRI_TABLE_OUT - MRI_TABLE_IN) * frac
    else:
        table_x = MRI_TABLE_OUT

    try:
        bb.resetBasePose(mri_table_base, [table_x, MRI_Y, 0.50], qI)
        bb.resetBasePose(mri_table_pad, [table_x, MRI_Y, 0.57], qI)
        bb.resetBasePose(mri_table_rail_L, [table_x, MRI_Y-0.22, 0.48], qI)
        bb.resetBasePose(mri_table_rail_R, [table_x, MRI_Y+0.22, 0.48], qI)
        bb.resetBasePose(mri_patient_torso, [table_x, MRI_Y, 0.67], qI)
        bb.resetBasePose(mri_patient_head, [table_x+0.20, MRI_Y, 0.72], qI)
        bb.resetBasePose(mri_patient_legs, [table_x-0.40, MRI_Y, 0.65], qI)
    except: pass

    # Ring rotation (only when scanning — table is inside)
    scanning = 0.40 <= cycle_t <= 0.75
    if scanning:
        ring_angle = t * MRI_RING_SPEED
        r = 0.40  # ring radius
        # 4-point cross rotating around bore axis (X-axis)
        cos_a = math.cos(ring_angle)
        sin_a = math.sin(ring_angle)
        ry1 = MRI_Y + r * cos_a
        rz1 = 0.90 + r * sin_a
        ry2 = MRI_Y - r * sin_a
        rz2 = 0.90 + r * cos_a
        try:
            q_r1 = bb.getQuaternionFromEuler([ring_angle, 0, 0])
            bb.resetBasePose(mri_ring_H, [MRI_X, MRI_Y, 0.90], q_r1)
            bb.resetBasePose(mri_ring_V, [MRI_X, MRI_Y, 0.90], q_r1)
            q_r2 = bb.getQuaternionFromEuler([ring_angle+0.3, 0, 0])
            bb.resetBasePose(mri_ring2_H, [MRI_X+0.15, MRI_Y, 0.90], q_r2)
            bb.resetBasePose(mri_ring2_V, [MRI_X+0.15, MRI_Y, 0.90], q_r2)
        except: pass

        # scan line on console sweeps up/down
        scan_frac = (t * 0.8) % 2.0
        if scan_frac > 1.0:
            scan_frac = 2.0 - scan_frac
        scan_z = 1.02 + scan_frac * 0.32
        try:
            bb.resetBasePose(mri_scan_line, [MRI_CON_X, MRI_CON_Y-0.30, scan_z], qI)
        except: pass

        # pulsing status LED
        led_on = int(t * 4) % 2 == 0
        try:
            bb.resetBasePose(mri_status_led,
                [MRI_CON_X+0.35, MRI_CON_Y-0.18, 0.84], qI)
        except: pass
    else:
        # rings hidden (off to side when not scanning)
        try:
            bb.resetBasePose(mri_ring_H, [MRI_X, MRI_Y, 0.90], qI)
            bb.resetBasePose(mri_ring_V, [MRI_X, MRI_Y, 0.90], qI)
            bb.resetBasePose(mri_ring2_H, [MRI_X+0.15, MRI_Y, 0.90], qI)
            bb.resetBasePose(mri_ring2_V, [MRI_X+0.15, MRI_Y, 0.90], qI)
        except: pass


# ============================================================
# ANIMATION: X-Ray Machine
# ============================================================
def animate_xray(t):
    qI = [0, 0, 0, 1]

    # Arm swings back and forth over the patient
    swing = math.sin(t * XR_ARM_SWING_SPEED) * XR_ARM_RANGE
    arm_tip_x = XR_X + 0.4 + swing
    arm_mid_x = XR_X + 0.2 + swing * 0.5

    try:
        bb.resetBasePose(xr_arm, [arm_mid_x, XR_Y, 2.30], qI)
        bb.resetBasePose(xr_head, [arm_tip_x, XR_Y, 2.22], qI)
        # detector panel tracks under the arm
        bb.resetBasePose(xr_detector, [arm_tip_x, XR_Y, 0.72], qI)
    except: pass

    # Exposure pulse (beam appears periodically)
    cycle_pos = t % XR_EXPOSE_INTERVAL
    exposing = cycle_pos < XR_EXPOSE_DURATION

    if exposing:
        # beam visible between head and detector
        beam_z = (2.14 + 0.72) / 2
        beam_half_h = (2.14 - 0.72) / 2
        try:
            bb.resetBasePose(xr_beam, [arm_tip_x, XR_Y, beam_z], qI)
        except: pass
        # flash red LED
        try:
            bb.resetBasePose(xr_expose_led,
                [XR_CTRL_X+0.18, XR_CTRL_Y-0.10, 1.14], qI)
        except: pass
    else:
        # hide beam underground
        try:
            bb.resetBasePose(xr_beam, [XR_X, XR_Y, -5.0], qI)
        except: pass


# ============================================================
# ANIMATION: Outside flashing lights & beacon
# ============================================================
def animate_outside(t):
    qI = [0, 0, 0, 1]

    # Ambulance alternating red/blue lights
    flash = int(t * 3) % 2
    try:
        if flash == 0:
            bb.resetBasePose(amb_light_L,
                [AMB_X-0.75, AMB_Y-0.15, 1.24], qI)
            bb.resetBasePose(amb_light_R,
                [AMB_X-0.75, AMB_Y+0.15, -5.0], qI)
        else:
            bb.resetBasePose(amb_light_L,
                [AMB_X-0.75, AMB_Y-0.15, -5.0], qI)
            bb.resetBasePose(amb_light_R,
                [AMB_X-0.75, AMB_Y+0.15, 1.24], qI)
    except: pass

    # Helipad beacon rotation
    beacon_angle = t * 1.5
    bx2 = HELI_X + 0.3 * math.cos(beacon_angle)
    by2 = HELI_Y + 0.3 * math.sin(beacon_angle)
    pulse = 0.5 + 0.5 * math.sin(t * 4)
    try:
        bb.resetBasePose(heli_beacon, [bx2, by2, 0.06], qI)
    except: pass


# ============================================================
# DEBUG CONTROLS
# ============================================================

# --- Moveable-object sliders ---
bb.addDebugSlider('bed_X', BED_AX, -3.0, 3.0)
bb.addDebugSlider('bed_Y', BED_AY, -3.0, 3.0)
bb.addDebugSlider('base_X', RBX, -3.0, 3.0)
bb.addDebugSlider('base_Y', RBY, -3.0, 1.0)
bb.addDebugSlider('iv_X', IVX, -4.0, 4.0)
bb.addDebugSlider('iv_Y', IVY, -3.5, 3.5)
bb.addDebugSlider('cart_X', CCX, -4.0, 4.5)
bb.addDebugSlider('cart_Y', CCY, -3.5, 3.5)
bb.addDebugSlider('o2_X', OXX, -4.0, 4.0)
bb.addDebugSlider('o2_Y', OXY, -3.5, 3.5)
bb.addDebugSlider('mon_X', MNX, -4.0, 4.0)
bb.addDebugSlider('mon_Y', MNY, -3.5, 3.5)

# --- Arm manual control ---
bb.addDebugSlider('ee_X', LOC_A[0], -1.5, 1.5)
bb.addDebugSlider('ee_Y', LOC_A[1], -2.5, 1.0)
bb.addDebugSlider('ee_Z', LOC_A[2],  0.1, 1.6)
bb.addDebugButton('MoveArm')
bb.addDebugButton('GripOpen')
bb.addDebugButton('GripClose')

# --- Auto pick-and-drop ---
bb.addDebugButton('PickAndDrop')
bb.addDebugButton('ResetCube')

goal_frame = bb.createDebugFrame(position=LOC_A)

# ============================================================
# ARM HELPERS
# ============================================================
HOME_JP = [0, -0.4, 0.0, -1.65, 0.0, 1.48, 0.785]
DQ      = bb.getQuaternionFromEuler([math.pi, 0, 0])
CARRY   = 0.055

def arm_home():
    for i, v in enumerate(HOME_JP):
        bb.setJointMotorControl(robot, i, targetPosition=v)

def ik_move(px, py, pz):
    jp = bb.calculateInverseKinematics(robot, ee_link, [px, py, pz], DQ)
    for i in range(min(7, len(jp))):
        bb.setJointMotorControl(robot, i, targetPosition=jp[i])

def get_ee_pos():
    """Get current end-effector position."""
    try:
        ep, _ = bb.getLinkPose(robot, ee_link)
        return list(ep)
    except:
        return [0.0, 0.0, 0.5]

def smooth_ease(t):
    """Smooth-step ease-in-out: 3t^2 - 2t^3"""
    t = max(0.0, min(1.0, t))
    return t * t * (3.0 - 2.0 * t)

def lerp3(a, b, t):
    """Linearly interpolate between two 3D points."""
    s = smooth_ease(t)
    return [a[0]+(b[0]-a[0])*s, a[1]+(b[1]-a[1])*s, a[2]+(b[2]-a[2])*s]

arm_home()
open_grip()

# ============================================================
# PICK-AND-PLACE SEQUENCE  (smooth interpolation)
# ============================================================
HOLD_S = 50; HOLD_M = 100; HOLD_L = 180

# Step types: "move" = smooth IK interpolation, "action" = instant (grip/home)
def make_sequence(pick_loc, drop_loc):
    px, py, pz = pick_loc
    dx, dy, dz = drop_loc
    above_pick = pz + 0.16
    at_pick    = pz + 0.005
    carry_h    = max(above_pick + 0.08, dz + 0.22)
    above_drop = dz + 0.16
    at_drop    = dz + 0.005
    home_pos   = [0.3, -0.5, 0.7]  # approximate home EE position
    return [
        ("HOME",       "action", lambda: arm_home(),     home_pos,                           HOLD_M),
        ("OPEN",       "action", lambda: open_grip(),    None,                                HOLD_S),
        ("ABOVE_PICK", "move",   None, [px, py, above_pick],                                  HOLD_L),
        ("TO_PICK",    "move",   None, [px, py, at_pick],                                     HOLD_L),
        ("GRIP",       "action", lambda: close_grip(),   None,                                HOLD_M),
        ("LIFT",       "move",   None, [px, py, carry_h],                                     HOLD_L),
        ("TRANSIT",    "move",   None, [(px+dx)/2, (py+dy)/2, carry_h+0.05],                  HOLD_L),
        ("ABOV_DROP",  "move",   None, [dx, dy, above_drop],                                  HOLD_L),
        ("TO_DROP",    "move",   None, [dx, dy, at_drop],                                     HOLD_L),
        ("RELEASE",    "action", lambda: open_grip(),    None,                                HOLD_M),
        ("RETREAT",    "move",   None, [dx, dy, above_drop],                                  HOLD_L),
        ("HOME_END",   "action", lambda: arm_home(),     home_pos,                           HOLD_M),
    ]

CARRY_STEPS = {"GRIP","LIFT","TRANSIT","ABOV_DROP","TO_DROP"}

seq        = None
step_idx   = 0
step_timer = 0
step_start_pos = None  # captured EE position at start of each smooth move
gripped    = False
cube_at_A  = True
auto_running = False

old_move_btn       = 0
old_grip_open_btn  = 0
old_grip_close_btn = 0
old_pick_btn       = 0
old_reset_btn      = 0
status_txt  = None
prev_label  = ""

# Smooth manual-move state
manual_moving    = False
manual_start_pos = None
manual_target    = None
manual_frames    = 0
manual_frame_max = 180

sim_time = 0.0

# Track previous slider values so we only reposition when changed
prev_bed_x = BED_AX;  prev_bed_y = BED_AY
prev_base_x = RBX;    prev_base_y = RBY
prev_iv_x = IVX;      prev_iv_y = IVY
prev_cart_x = CCX;    prev_cart_y = CCY
prev_o2_x = OXX;      prev_o2_y = OXY
prev_mon_x = MNX;     prev_mon_y = MNY

# ============================================================
# ANIMATION HELPERS
# ============================================================
def animate_surgical_robot(t):
    qI = bb.getQuaternionFromEuler([0, 0, 0])
    tower_x = SRX;  tower_y = SRY + 0.75;  tower_top_z = 1.90
    table_z = 0.81

    a1 = t * 0.6
    tip1_x = SRX + math.sin(a1)*0.12 - 0.08
    tip1_y = SRY + math.cos(a1*0.7)*0.08
    tip1_z = table_z + 0.02
    sh1 = [tower_x-0.15, tower_y, tower_top_z]
    mid1 = [(sh1[0]+tip1_x)/2, (sh1[1]+tip1_y)/2, (sh1[2]+tip1_z)/2+0.15]
    try:
        bb.resetBasePose(s1_shoulder, sh1, qI)
        bb.resetBasePose(s1_upper, mid1, qI)
        bb.resetBasePose(s1_lower, [(mid1[0]+tip1_x)/2,(mid1[1]+tip1_y)/2,(mid1[2]+tip1_z)/2], qI)
        bb.resetBasePose(s1_tool, [tip1_x, tip1_y, tip1_z+0.10], qI)
        g = 0.012+0.008*math.sin(t*2.5)
        bb.resetBasePose(s1_grip_L, [tip1_x, tip1_y-g, tip1_z], qI)
        bb.resetBasePose(s1_grip_R, [tip1_x, tip1_y+g, tip1_z], qI)
    except: pass

    a2 = t * 0.5 + 2.0
    tip2_x = SRX + math.sin(a2)*0.10 + 0.08
    tip2_y = SRY + math.cos(a2*0.8)*0.10
    tip2_z = table_z + 0.03
    sh2 = [tower_x+0.15, tower_y, tower_top_z]
    mid2 = [(sh2[0]+tip2_x)/2, (sh2[1]+tip2_y)/2, (sh2[2]+tip2_z)/2+0.15]
    try:
        bb.resetBasePose(s2_shoulder, sh2, qI)
        bb.resetBasePose(s2_upper, mid2, qI)
        bb.resetBasePose(s2_lower, [(mid2[0]+tip2_x)/2,(mid2[1]+tip2_y)/2,(mid2[2]+tip2_z)/2], qI)
        bb.resetBasePose(s2_tool, [tip2_x, tip2_y, tip2_z+0.10], qI)
        g2 = 0.012+0.006*math.sin(t*3.0+1.0)
        bb.resetBasePose(s2_grip_L, [tip2_x, tip2_y-g2, tip2_z], qI)
        bb.resetBasePose(s2_grip_R, [tip2_x, tip2_y+g2, tip2_z], qI)
    except: pass

    cam_x = SRX + math.sin(t*0.3)*0.05
    cam_y = SRY + math.cos(t*0.25)*0.04
    cam_z = table_z + 0.30
    try:
        bb.resetBasePose(s3_shoulder, [tower_x, tower_y, tower_top_z], qI)
        bb.resetBasePose(s3_boom, [(tower_x+cam_x)/2,(tower_y+cam_y)/2,(tower_top_z+cam_z)/2], qI)
        bb.resetBasePose(s3_cam, [cam_x, cam_y, cam_z], qI)
        bb.resetBasePose(s3_lens, [cam_x, cam_y, cam_z-0.05], qI)
    except: pass


def animate_lokomat(t):
    global belt_offset
    qI = bb.getQuaternionFromEuler([0, 0, 0])
    hip_z = LK_HIP_HEIGHT

    for side, sign, thigh_b, shank_b, foot_b, knee_m in [
        ("L", -1, lk_L_thigh, lk_L_shank, lk_L_foot, lk_L_knee_motor),
        ("R",  1, lk_R_thigh, lk_R_shank, lk_R_foot, lk_R_knee_motor),
    ]:
        ph = t * LK_GAIT_SPEED + (0.0 if side=="L" else math.pi)
        hip_a = LK_HIP_AMP * math.sin(ph)
        knee_b = LK_KNEE_AMP * max(0, math.sin(ph - 0.5))

        knee_x = LKX + LK_THIGH_LEN * math.sin(hip_a)
        knee_z = hip_z - LK_THIGH_LEN * math.cos(hip_a)
        total_a = hip_a + knee_b
        ankle_x = knee_x + LK_SHANK_LEN * math.sin(total_a)
        ankle_z = knee_z - LK_SHANK_LEN * math.cos(total_a)
        lat = sign * 0.10

        try:
            q_th = bb.getQuaternionFromEuler([0, -hip_a, 0])
            bb.resetBasePose(thigh_b, [(LKX+knee_x)/2, LKY+lat, (hip_z+knee_z)/2], q_th)
            q_sh = bb.getQuaternionFromEuler([0, -total_a, 0])
            bb.resetBasePose(shank_b, [(knee_x+ankle_x)/2, LKY+lat, (knee_z+ankle_z)/2], q_sh)
            bb.resetBasePose(foot_b, [ankle_x, LKY+lat, ankle_z-0.02], qI)
            bb.resetBasePose(knee_m, [knee_x, LKY+lat-0.04, knee_z], q_th)
        except: pass

    belt_offset += LK_BELT_SPEED
    if belt_offset > 0.16:
        belt_offset -= 0.16
    for i, bm_body in enumerate(belt_markers):
        bx = LKX - 0.40 + i*0.16 + belt_offset
        if bx > LKX + 0.48:
            bx -= 0.96
        try:
            bb.resetBasePose(bm_body, [bx, LKY, 0.254], qI)
        except: pass

# ============================================================
# MAIN LOOP
# ============================================================
while True:
    bb.stepSimulation(DT)
    step_timer += 1
    sim_time += DT

    # ── Vacuum robot ──────────────────────────────────────────
    tgt = vac_path[vac_wp]
    dvx = tgt[0]-vac_x; dvy = tgt[1]-vac_y
    d   = math.sqrt(dvx*dvx+dvy*dvy)
    if d < 0.15:
        vac_wp = (vac_wp+1) % len(vac_path)
    else:
        vac_x += (dvx/d)*vac_spd; vac_y += (dvy/d)*vac_spd
        ang = math.atan2(dvy,dvx)
        try:
            bb.resetBasePose(vac_body,[vac_x,vac_y,0.045],
                bb.getQuaternionFromEuler([0,0,ang]))
            bb.resetBasePose(vac_light,[vac_x,vac_y,0.14],
                bb.getQuaternionFromEuler([0,0,ang]))
        except: pass

    # ── Animations ────────────────────────────────────────────
    animate_surgical_robot(sim_time)
    animate_lokomat(sim_time)
    animate_outside(sim_time)

    # ── Imaging Room animations (togglable) ───────────────────
    try:
        if bb.readDebugParameter('MRI_Active'):
            animate_mri(sim_time)
    except: pass
    try:
        if bb.readDebugParameter('XRay_Active'):
            animate_xray(sim_time)
    except: pass

    # ── Robot Dog patrol in reception ─────────────────────────
    try:
        animate_spot_dog()
    except: pass

    # ── READ MOVEABLE-OBJECT SLIDERS ──────────────────────────
    cur_bed_x  = bb.readDebugParameter('bed_X')
    cur_bed_y  = bb.readDebugParameter('bed_Y')
    cur_base_x = bb.readDebugParameter('base_X')
    cur_base_y = bb.readDebugParameter('base_Y')
    cur_iv_x   = bb.readDebugParameter('iv_X')
    cur_iv_y   = bb.readDebugParameter('iv_Y')
    cur_cart_x = bb.readDebugParameter('cart_X')
    cur_cart_y = bb.readDebugParameter('cart_Y')
    cur_o2_x   = bb.readDebugParameter('o2_X')
    cur_o2_y   = bb.readDebugParameter('o2_Y')
    cur_mon_x  = bb.readDebugParameter('mon_X')
    cur_mon_y  = bb.readDebugParameter('mon_Y')

    # ── REPOSITION MOVEABLE GROUPS ────────────────────────────
    # Bed
    if abs(cur_bed_x - prev_bed_x) > 0.001 or abs(cur_bed_y - prev_bed_y) > 0.001:
        reposition_group(bed_parts, cur_bed_x, cur_bed_y, BED_AX, BED_AY)
        prev_bed_x = cur_bed_x; prev_bed_y = cur_bed_y

    # Robot base + tray (move URDF + decoration)
    if abs(cur_base_x - prev_base_x) > 0.001 or abs(cur_base_y - prev_base_y) > 0.001:
        reposition_group(robo_parts, cur_base_x, cur_base_y, RBX, RBY)
        try:
            bb.resetBasePose(robot,
                [cur_base_x, cur_base_y, RBZ], robo_orn)
        except: pass
        prev_base_x = cur_base_x; prev_base_y = cur_base_y

    # IV Stand
    if abs(cur_iv_x - prev_iv_x) > 0.001 or abs(cur_iv_y - prev_iv_y) > 0.001:
        reposition_group(iv_parts, cur_iv_x, cur_iv_y, IVX, IVY)
        prev_iv_x = cur_iv_x; prev_iv_y = cur_iv_y

    # Crash Cart
    if abs(cur_cart_x - prev_cart_x) > 0.001 or abs(cur_cart_y - prev_cart_y) > 0.001:
        reposition_group(cart_parts, cur_cart_x, cur_cart_y, CCX, CCY)
        prev_cart_x = cur_cart_x; prev_cart_y = cur_cart_y

    # Oxygen Tank
    if abs(cur_o2_x - prev_o2_x) > 0.001 or abs(cur_o2_y - prev_o2_y) > 0.001:
        reposition_group(o2_parts, cur_o2_x, cur_o2_y, OXX, OXY)
        prev_o2_x = cur_o2_x; prev_o2_y = cur_o2_y

    # Monitor
    if abs(cur_mon_x - prev_mon_x) > 0.001 or abs(cur_mon_y - prev_mon_y) > 0.001:
        reposition_group(mon_parts, cur_mon_x, cur_mon_y, MNX, MNY)
        prev_mon_x = cur_mon_x; prev_mon_y = cur_mon_y

    # ── READ BUTTONS ──────────────────────────────────────────
    new_pick_btn   = bb.readDebugParameter('PickAndDrop')
    new_reset_btn  = bb.readDebugParameter('ResetCube')
    new_grip_open  = bb.readDebugParameter('GripOpen')
    new_grip_close = bb.readDebugParameter('GripClose')
    new_move_btn   = bb.readDebugParameter('MoveArm')

    # ── RESET CUBE — teleport back to tray ────────────────────
    if new_reset_btn > old_reset_btn:
        base_dx = cur_base_x - RBX
        base_dy = cur_base_y - RBY
        reset_pos = [LOC_A[0]+base_dx, LOC_A[1]+base_dy, LOC_A[2]]
        try:
            bb.resetBasePose(cube, reset_pos,
                bb.getQuaternionFromEuler([0,0,0]))
        except: pass
        cube_at_A = True
        auto_running = False
        step_idx = 0; step_timer = 0; gripped = False
        step_start_pos = None; manual_moving = False
        open_grip()
        arm_home()
        old_reset_btn = new_reset_btn

    # ── PICK-AND-DROP BUTTON — start auto cycle ───────────────
    if new_pick_btn > old_pick_btn and not auto_running:
        base_dx = cur_base_x - RBX
        base_dy = cur_base_y - RBY
        bed_dx  = cur_bed_x - BED_AX
        bed_dy  = cur_bed_y - BED_AY

        cur_pick = [LOC_A[0]+base_dx, LOC_A[1]+base_dy, LOC_A[2]]
        cur_drop = [LOC_B[0]+bed_dx,  LOC_B[1]+bed_dy,  LOC_B[2]]

        if cube_at_A:
            seq = make_sequence(cur_pick, cur_drop)
        else:
            seq = make_sequence(cur_drop, cur_pick)

        step_idx = 0; step_timer = 0; gripped = False
        auto_running = True
        prev_label = ""
        old_pick_btn = new_pick_btn
    else:
        old_pick_btn = new_pick_btn

    # ── AUTO MODE  (pick-and-drop cycle — smooth) ───────────────
    if auto_running and seq is not None:
        label, stype, action_fn, target_pos, hold = seq[step_idx]

        if label != prev_label:
            # capture start position for smooth interpolation
            step_start_pos = get_ee_pos()
            try:
                if status_txt is not None:
                    bb.removeDebugObject(status_txt)
                direction = "TRAY->BED" if cube_at_A else ""
                status_txt = bb.createDebugText(
                    direction + " | " + label,
                    [cur_base_x, cur_base_y-0.65, 1.55],
                    color='green', size=1.0)
            except: pass
            prev_label = label

        if stype == "action":
            # instant actions: fire once, then wait
            if step_timer == 1:
                action_fn()
                gripped = (label in CARRY_STEPS)
        else:
            # smooth IK move: interpolate every frame
            frac = step_timer / max(1, hold)
            interp = lerp3(step_start_pos, target_pos, frac)
            ik_move(interp[0], interp[1], interp[2])
            gripped = (label in CARRY_STEPS)

        if step_timer >= hold:
            # snap to exact target at end of move step
            if stype == "move" and target_pos:
                ik_move(target_pos[0], target_pos[1], target_pos[2])
            step_timer = 0
            step_idx  += 1
            if step_idx >= len(seq):
                cube_at_A = not cube_at_A
                auto_running = False
                gripped = False
                step_idx = 0
                step_start_pos = None
                try:
                    if status_txt is not None:
                        bb.removeDebugObject(status_txt)
                        status_txt = None
                except: pass

    elif not auto_running:
        # ── MANUAL MODE (smooth) ─────────────────────────────
        if step_timer > 0:
            step_idx = 0; step_timer = 0; prev_label = ""
            step_start_pos = None
        try:
            if status_txt is not None:
                bb.removeDebugObject(status_txt)
                status_txt = None
        except: pass

        ex = bb.readDebugParameter('ee_X')
        ey = bb.readDebugParameter('ee_Y')
        ez = bb.readDebugParameter('ee_Z')
        try: bb.resetDebugObjectPose(goal_frame, [ex,ey,ez], DQ)
        except: pass

        if new_move_btn > old_move_btn:
            manual_moving = True
            manual_start_pos = get_ee_pos()
            manual_target = [ex, ey, ez]
            manual_frames = 0

        # Smooth interpolation toward manual target
        if manual_moving and manual_target is not None:
            manual_frames += 1
            frac = manual_frames / manual_frame_max
            if frac >= 1.0:
                ik_move(manual_target[0], manual_target[1], manual_target[2])
                manual_moving = False
            else:
                interp = lerp3(manual_start_pos, manual_target, frac)
                ik_move(interp[0], interp[1], interp[2])

        if new_grip_open > old_grip_open_btn:
            open_grip()
            gripped = False

        if new_grip_close > old_grip_close_btn:
            close_grip()
            gripped = True

    old_move_btn       = new_move_btn
    old_grip_open_btn  = new_grip_open
    old_grip_close_btn = new_grip_close

    # ── VISUAL FINGERS ────────────────────────────────────────
    try:
        ep, eo = bb.getLinkPose(robot, ee_link)
        update_fingers(ep, eo, grip_spread)
    except: pass

    # ── CARRY CUBE (kinematic override while gripped) ─────────
    if gripped:
        try:
            ep, eo = bb.getLinkPose(robot, ee_link)
            bb.resetBasePose(cube, [ep[0], ep[1], ep[2]-CARRY], eo)
        except: pass

    time.sleep(DT)
