"""Source-informed display atlas. Numeric coordinates are authored projections, not measurements.
Every placement is joined to the per-point KMCRIC/WHO location record by build-stage1.py.
Front/back/side are independently registered by anatomical region; hidden surfaces stay hidden.
"""
import math
LAYOUT = {}
def put(code, i, xy, view='front', region='', secondary=None, inset=None, medial=False):
    key=f'{code}{i}'
    assert key not in LAYOUT, key
    views={'front':None,'back':None,'side':None}
    views[view]=list(xy)
    if secondary:
        views.update({k:list(v) for k,v in secondary.items()})
    LAYOUT[key]={'views':views,'preferredView':view,'region':region,'inset':inset,
                 'sideSurface':'medial' if medial else 'lateral','xy':list(xy)}
def line(code,start,coords,view='front',region='',**kw):
    for i,xy in enumerate(coords,start):put(code,i,xy,view,region,**kw)
def lerp(a,b,t):return [round(a[0]+(b[0]-a[0])*t,2),round(a[1]+(b[1]-a[1])*t,2)]
# Named anchors; ratios use regional B-cun, never one universal centimetre scale.
REGIONAL = {'front':{'wrist':[550,650],'elbow':[492,500],'axilla':[465,415]},
            'back':{'wrist':[539,657],'elbow':[481,510],'axilla':[439,410]},
            'side':{'wrist':[454,687],'elbow':[428,562],'axilla':[433,425]}}
def arm(c,i,cun,rim,views,region='forearm'):
    xy={}
    for v in views:
        anchors=REGIONAL[v];p=lerp(anchors['wrist'],anchors['elbow'],cun/12)
        p[0]+=rim if v=='front' else -rim if v=='back' else rim*.55
        xy[v]=p
    preferred=views[0];put(c,i,xy.pop(preferred),preferred,region,xy)
def upper(c,i,from_elbow,rim,views):
    xy={}
    for v in views:
        a=REGIONAL[v];p=lerp(a['elbow'],a['axilla'],from_elbow/9);p[0]+=rim if v=='front' else -rim
        xy[v]=p
    preferred=views[0];put(c,i,xy.pop(preferred),preferred,'upper-arm',xy)
# Thoracic levels and abdominal B-cun grid.
IC={i:337+22*i for i in range(1,8)}
def abdominal(c,i,up,lateral):
    put(c,i,[380+lateral*17,580-up*16],'front','abdomen',
        {'side':[292+lateral*7,580-up*16]})
def chest(c,i,intercostal,lateral):
    put(c,i,[380+lateral*17,IC[intercostal]],'front','thorax',
        {'side':[291+lateral*12,IC[intercostal]]})
# LU: radial anterior arm; first two points are 6 B-cun from midline.
chest('LU',1,1,6);put('LU',2,[482,337],'front','thorax',{'side':[361,337]})
upper('LU',3,6,10,['front','side']);upper('LU',4,5,10,['front','side'])
for i,cun in [(5,12),(6,7),(7,1.5),(8,1),(9,0)]:arm('LU',i,cun,9,['front','side'])
line('LU',10,[[574,680],[587,697]],region='palm')
# LI: dorsoradial. Hand is dorsal, not the palm.
line('LI',1,[[556,722],[550,705],[547,690],[542,678]],'back','hand-dorsal')
for i,cun in [(5,0),(6,3),(7,5),(8,8),(9,9),(10,10),(11,12),(12,13)]:
    arm('LI',i,cun,11,['back','side'])
upper('LI',13,3,12,['front','side']);upper('LI',14,7,12,['front','side'])
put('LI',15,[481,373],'front','shoulder',{'side':[430,390]})
put('LI',16,[423,340],'back','shoulder',{'side':[418,372]})
line('LI',17,[[423,321],[420,307],[393,269],[397,255]],region='neck-face')
# ST: face; neck is a branch from ST5, never ST8.
line('ST',1,[[404,236],[405,246],[405,258],[407,276],[427,285],[437,273],[441,246],[434,189]],region='face')
line('ST',9,[[410,307],[412,321],[410,334],[448,328]],region='neck')
put('ST',13,[448,337],'front','thorax',{'side':[339,337]})
for i,ic in [(14,1),(15,2),(16,3),(17,4),(18,5)]:chest('ST',i,ic,4)
for i,up in enumerate(range(6,-6,-1),19):abdominal('ST',i,up,2)
line('ST',31,[[447,690],[452,756],[459,795],[461,808],[466,838]],region='anterior-thigh')
for i,down in [(36,3),(37,6),(38,8),(39,9)]:
    xy=lerp([466,838],[497,974],down/16);put('ST',i,xy,'front','anterior-leg')
xy=lerp([466,838],[497,974],.5);xy[0]+=10;put('ST',40,xy,'front','anterolateral-leg')
line('ST',41,[[497,974],[522,995],[548,1008],[569,1017],[578,1022]],region='foot-dorsal')
# SP: medial foot/leg. Medial view is an explicit unfolded near-surface view.
line('SP',1,[[527,1023],[516,1016],[508,1009],[494,993],[481,976]],region='medial-foot',medial=True)
for i,cun in [(6,3),(7,6),(8,10),(9,13)]:
    xy=lerp([481,970],[446,838],cun/13);put('SP',i,xy,'front','medial-leg',medial=True)
line('SP',10,[[437,794],[425,723],[437,660]],region='medial-thigh',medial=True)
for i,up in [(13,-4.3),(14,-1.3),(15,0),(16,3)]:abdominal('SP',i,up,4)
for i,ic in [(17,5),(18,4),(19,3),(20,2)]:chest('SP',i,ic,6)
put('SP',21,[369,469],'side','lateral-thorax')
# HT ulnar anterior. PC occupies the middle; LU the radial margin.
put('HT',1,[453,421],'front','axilla',{'side':[426,424]})
upper('HT',2,3,-11,['front']);arm('HT',3,12,-11,['front'])
for i,cun in [(4,1.5),(5,1),(6,.5),(7,0)]:arm('HT',i,cun,-9,['front'])
line('HT',8,[[554,688],[559,720]],region='palm')
# SI ulnar posterior, scapular loop.
line('SI',1,[[577,724],[564,703],[559,689],[550,674],[548,657]],'back','hand-dorsal')
arm('SI',6,1,-9,['back']);arm('SI',7,5,-9,['back']);arm('SI',8,12,-9,['back'])
line('SI',9,[[441,405],[435,383],[403,412],[401,365],[378,366],[397,339],[380,321]],'back','scapula')
line('SI',16,[[427,307],[436,287],[426,260],[445,244]],region='neck-face')
# Vertebral numbering: no interpolation across the missing T8 point or between inner/outer BL lines.
T={i:339+(i-1)*17 for i in range(1,13)}
L={i:543+(i-1)*23 for i in range(1,6)}
S={i:649+(i-1)*13 for i in range(1,5)}
line('BL',1,[[393,231],[393,218],[393,194],[405.5,194],[405.5,187],[405.5,174],[405.5,163]],region='head-front')
line('BL',8,[[371.5,170],[368,231],[371,289]],'back','head-back')
for i,level in list(zip(range(11,18),range(1,8)))+[(18,9),(19,10),(20,11),(21,12)]:
    put('BL',i,[371.5,T[level]],'back','spine-T'+str(level))
for i,level in zip(range(22,27),range(1,6)):put('BL',i,[371.5,L[level]],'back','spine-L'+str(level))
for i,level in zip(range(27,31),range(1,5)):put('BL',i,[371.5,S[level]],'back','sacrum-S'+str(level))
for i,level in zip(range(31,35),range(1,5)):put('BL',i,[361,S[level]],'back','sacral-foramen-'+str(level))
put('BL',35,[354.5,700],'back','coccyx')
line('BL',36,[[417,733],[427,777],[451,824],[454,835],[434,835]],'back','posterior-thigh')
for i,level in [(41,2),(42,3),(43,4),(44,5),(45,6),(46,7),(47,9),(48,10),(49,11),(50,12)]:
    put('BL',i,[397,T[level]],'back','spine-T'+str(level))
put('BL',51,[397,L[1]],'back','spine-L1');put('BL',52,[397,L[2]],'back','spine-L2')
put('BL',53,[397,S[2]],'back','sacrum-S2');put('BL',54,[397,S[4]],'back','sacrum-S4')
for i,down in [(55,2),(56,5),(57,8),(58,9),(59,13),(60,16)]:
    xy=lerp([434,835],[457,973],down/16)
    if i in [58,59,60]:xy[0]+=11
    put('BL',i,xy,'back','posterior-leg',{'side':[323+(.5 if i>=58 else 0)*12,835+down/16*138]})
line('BL',61,[[326,1017],[316,1005],[295,1020],[279,1033],[263,1044],[249,1050],[236,1057]],'side','lateral-foot')
# KI1 is plantar, not a dorsal dot; close-up makes the surface explicit.
put('KI',1,[521,1009],'front','sole',inset='sole',medial=True)
line('KI',2,[[477,993],[479,970],[474,980],[470,988],[480,986]],region='medial-foot',medial=True)
for i,cun,rim in [(7,2,-5),(8,2,2),(9,5,-7)]:
    xy=lerp([480,970],[441,835],cun/13);xy[0]+=rim;put('KI',i,xy,'front','posteromedial-leg',medial=True)
put('KI',10,[419,835],'back','posteromedial-knee',medial=True)
for i,up in [(11,-5),(12,-4),(13,-3),(14,-2),(15,-1),(16,0),(17,2),(18,3),(19,4),(20,5),(21,6)]:abdominal('KI',i,up,.5)
for i,ic in [(22,5),(23,4),(24,3),(25,2),(26,1)]:chest('KI',i,ic,2)
put('KI',27,[414,337],'front','thorax',{'side':[315,337]})
chest('PC',1,4,5);upper('PC',2,7,0,['front']);arm('PC',3,12,0,['front'])
for i,cun in [(4,5),(5,3),(6,2),(7,0)]:arm('PC',i,cun,0,['front'])
line('PC',8,[[566,686],[575,725]],region='palm')
# TE dorsal forearm.
line('TE',1,[[570,729],[565,709],[552,690]],'back','hand-dorsal')
for i,cun,rim in [(4,0,0),(5,2,0),(6,3,0),(7,3,-5),(8,4,0),(9,7,0),(10,13,0)]:arm('TE',i,cun,rim,['back'])
upper('TE',11,2,0,['back']);upper('TE',12,5,0,['back']);upper('TE',13,6,-6,['back'])
line('TE',14,[[452,372],[401,341]],'back','shoulder')
put('TE',16,[401,316],'side','neck');put('TE',17,[420,286],'side','ear')
line('TE',18,[[427,267],[429,242],[414,215],[400,240],[389,231],[339,233]],'side','ear')
# GB head follows three turns, explicitly sampled against the head landmarks.
line('GB',1,[[340,247],[397,265],[381,241],[358,219],[366,226],[373,233],[380,240],[408,204],[426,205],[437,228],[438,251],[432,285]],'side','temporal-head')
line('GB',13,[[431,194],[405,208],[414,194],[414,182],[414,172],[414,161]],region='head-front')
line('GB',19,[[387,231],[390,285],[410,328]],'back','head-neck')
put('GB',22,[369,425],'side','lateral-thorax');put('GB',23,[356,425],'side','lateral-thorax')
chest('GB',24,7,4)
line('GB',25,[[389,545],[368,580],[333,628],[341,658],[380,682],[397,700],[374,772],[370,791],[362,831],[347,856]],'side','lateral-trunk-leg')
for i,up,dx in [(35,7,7),(36,7,-4),(37,5,-4),(38,4,-4),(39,3,-4)]:
    xy=lerp([310,985],[350,845],up/16);xy[0]+=dx;put('GB',i,xy,'side','lateral-leg')
line('GB',40,[[299,985],[277,1021],[261,1034],[245,1043],[237,1049]],'side','foot-dorsal')
# LR medial foot, then crosses behind SP above 8 B-cun; knee/upper leg are medial.
line('LR',1,[[535,1025],[534,1016],[517,1003],[489,975]],region='medial-foot',medial=True)
for i,cun in [(5,5),(6,7)]:
    xy=lerp([481,970],[446,838],cun/13);xy[0]+=7;put('LR',i,xy,'front','anteromedial-leg',medial=True)
put('LR',7,[438,842],'front','medial-knee',medial=True);put('LR',8,[425,835],'back','medial-knee',medial=True)
line('LR',9,[[426,775],[426,708],[422,692],[422.5,660]],region='medial-thigh',medial=True)
put('LR',13,[359,523],'side','floating-rib-11');chest('LR',14,6,4)
# CV/GV midline; perineal/oral locations have separate local panels.
put('CV',1,[380,708],'front','perineum',inset='perineum')
for i,up in [(2,-5),(3,-4),(4,-3),(5,-2),(6,-1.5),(7,-1),(8,0),(9,1),(10,2),(11,3),(12,4),(13,5),(14,6),(15,7)]:abdominal('CV',i,up,0)
put('CV',16,[380,452],'front','xiphisternal');put('CV',17,[380,IC[4]],'front','thorax')
for i,ic in [(18,3),(19,2),(20,1)]:chest('CV',i,ic,0)
line('CV',21,[[380,337],[380,321],[380,302],[380,284]],region='midline-neck-face')
put('GV',1,[346,708],'back','perineum',inset='perineum');put('GV',2,[346,682],'back','sacral-hiatus')
for i,level in [(3,4),(4,2),(5,1)]:put('GV',i,[346,L[level]],'back','spine-L'+str(level))
for i,level in [(6,11),(7,10),(8,9),(9,7),(10,6),(11,5),(12,3),(13,1)]:put('GV',i,[346,T[level]],'back','spine-T'+str(level))
line('GV',14,[[346,321],[346,289],[346,269],[346,231],[346,201],[346,175]],'back','midline-head-neck')
line('GV',20,[[380,155],[380,166],[380,180],[380,190],[380,196],[380,257],[380,268],[380,275]],region='midline-head-face')
put('GV',28,[380,274],'front','oral-frenulum',inset='oral')
# Individually assigned lateral scalp projections preserve the crown arc. No affine body squeezing.
head_side={
'BL1':[318,245],'BL2':[322,234],'BL3':[326,216],'BL4':[333,215],'BL5':[341,209],'BL6':[359,200],'BL7':[382,195],'BL8':[409,199],'BL9':[445,250],'BL10':[416,316],
'GB13':[344,216],'GB14':[331,227],'GB15':[339,213],'GB16':[350,205],'GB17':[365,199],'GB18':[387,196],'GB19':[439,250],'GB20':[421,313],'GB21':[422,365],
'GV14':[426,344],'GV15':[421,320],'GV16':[433,303],'GV17':[446,256],'GV18':[441,223],'GV19':[425,204],'GV20':[391,192],'GV21':[368,194],'GV22':[347,203],'GV23':[336,211],'GV24':[330,217],'GV25':[286,255],'GV26':[293,266],'GV27':[287,273],'GV28':[301,274],
'ST1':[323,252],'ST2':[326,260],'ST3':[327,268],'ST4':[306,278],'ST5':[360,307],'ST6':[383,289],'ST7':[394,251],'ST8':[350,213],
'LI17':[389,337],'LI18':[377,322],'LI19':[298,268],'LI20':[302,258],
'SI16':[400,326],'SI17':[397,306],'SI18':[349,269],'SI19':[399,252],
'CV21':[314,369],'CV22':[314,353],'CV23':[318,324],'CV24':[298,290]
}
for key,xy in head_side.items():LAYOUT[key]['views']['side']=xy
# Cross-point landmark review against WHO/KMCRIC notes. Patellar base differs
# from the patellar ligament at ST35, and all thigh ratios share one scale.
for key,cun in [('ST32',6),('ST33',3),('ST34',2),('SP10',2),('LR9',4)]:
    LAYOUT[key]['views']['front'][1]=820-cun*12
    LAYOUT[key]['xy'][1]=820-cun*12
LAYOUT['KI10']['views']['back'][0]=428
LAYOUT['KI10']['xy'][0]=428
LAYOUT['LR8']['views']['back'][0]=419
LAYOUT['LR8']['xy'][0]=419
LAYOUT['GB20']['views']['back'][1]=269
LAYOUT['GB20']['views']['side'][1]=303
LAYOUT['GB20']['xy'][1]=269
LAYOUT['GV17']['views']['side'][1]=250
for key in ['GB14','GB15','GB16','GB17','GB18']:
    LAYOUT[key]['views']['front'][0]=405
    LAYOUT[key]['xy'][0]=405
LAYOUT['GB21']['views']['back']=[399,346.5]
LAYOUT['GB21']['xy']=[399,346.5]
LAYOUT['GB21']['views']['side']=[428,367]
# Lateral elbow margin can be seen frontally; dorsal forearm points remain hidden.
LAYOUT['LI11']['views']['front']=[504,500]
LAYOUT['LI12']['views']['front']=[503,487.5]
# Explicit medial leg side projection; it is displayed only when "內側" is selected.
for key,p in LAYOUT.items():
    if p['sideSurface']=='medial' and not p['inset'] and p['views']['side'] is None:
        x,y=p['xy'];p['views']['side']=[round(290+(1000-y)*.15 + (x-480)*.12,2),y+9]
        p['preferredView']='front' if p['views']['front'] else 'back'
# Lumbar/thoracic back lines are invisible from the front, not transposed onto the chest.
COUNTS={'LU':11,'LI':20,'ST':45,'SP':21,'HT':9,'SI':19,'BL':67,'KI':27,'PC':9,'TE':23,'GB':44,'LR':14,'CV':24,'GV':28}
assert len(LAYOUT)==361
assert set(LAYOUT)=={f'{c}{i}' for c,n in COUNTS.items() for i in range(1,n+1)}

