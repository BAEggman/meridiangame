"""Anatomical route graph built from the user's source evidence, not ID adjacency."""
from copy import deepcopy
def make_routes(points, evidence, patches):
    P={p['id']:p for p in points}
    # Registration of conceptual internal landmarks in each projection. These are
    # organ/region anchors, not additional acupuncture points or measured anatomy.
    C={
    'middle-jiao':([390,525],[350,525],[335,525]),
    'large-intestine':([418,610],[373,610],[351,610]),
    'stomach-orifice':([402,495],[360,495],[324,495]),
    'diaphragm':([380,474],[346,474],[354,474]),
    'lung':([412,390],[369,390],[373,401]),
    'lung-system':([385,336],[346,336],[357,345]),
    'stomach':([415,518],[370,518],[324,520]),
    'heart':([373,421],[344,421],[342,421]),
    'small-intestine':([376,613],[340,613],[320,613]),
    'heart-system':([378,397],[345,397],[348,397]),
    'eye-system':([400,233],[361,233],[342,239]),
    'chest':([382,423],[347,423],[350,423]),
    'pericardium':([383,435],[350,435],[355,435]),
    'three-jiao':([427,555],[380,555],[360,555]),
    'liver':([330,493],[310,493],[355,493]),
    'gallbladder':([338,513],[316,513],[370,513]),
    'kidney':([345,560],[319,560],[380,560]),
    'bladder':([380,648],[346,648],[329,648]),
    'brain':([380,207],[346,207],[382,227]),
    'vertex':([380,155],[346,160],[391,192]),
    'lower-teeth':([393,281],None,[321,288]),
    'upper-teeth':([393,271],None,[322,272]),
    'posterior-throat':([380,311],[346,311],[374,320]),
    'tongue-root':([382,291],[346,291],[340,297]),
    'lower-jiao-origin':([380,645],[346,645],[343,645]),
    'inferior-orbit':([404,236],None,[323,252]),
    'abdomen':([430,610],[390,610],[318,610]),
    'abdomen-inner':([400,586],[360,586],[340,586]),
    'cheek-inner':([410,265],[368,265],[345,271]),
    'forehead':([380,200],[346,186],[327,220]),
    'lateral-ribs':([476,492],[425,492],[367,492]),
    'lateral-ribs-inner':([454,505],[403,505],[369,505]),
    'lip-inner':([381,276],None,[310,278]),
    'lower-abdomen':([390,639],[354,639],[323,639]),
    'medial-posterior-thigh':([419,737],[403,746],[350,750]),
    'nasal-root-ST':([389,226],None,[317,239]),
    'nasopharynx':([381,249],[348,249],[348,253]),
    'paraspinal-deep':([367,550],[353,550],[394,550]),
    'pharynx':([382,313],[348,313],[361,320]),
    'pubic-hair-border':([397,666],[360,666],[331,666]),
    'spine':([380,575],[346,575],[400,575]),
    'spleen':([442,530],[394,530],[362,530]),
    'stomach-side':([426,522],[380,522],[337,522]),
    'throat':([380,315],[346,315],[348,323]),
    'tongue-underside':([380,285],None,[333,288]),
    'shoulder-back-BL':(None,[371.5,325],[421,350]),
    'lumbar-BL':(None,[371.5,566],[395,566]),
    'sacral-region-BL':(None,[361,642],None),
    'gluteal-BL':(None,[402,717],[391,717]),
    'posterior-wrist':([551,629],[530,639],[458,667]),
    'index-inner-margin':([577,704],[553,705],[475,751]),
    'foot-dorsum-ST':([522,995],None,[290,1020]),
    'foot-dorsum-GB':([556,1008],None,[277,1021]),
    'great-toe-ST':([530,1019],None,[248,1057]),
    'great-toe-nail-GB':([535,1025],None,[245,1061]),
    'palm-PC':([566,686],None,[470,736]),
    'ring-finger':([567,710],[563,716],[482,760]),
    'little-finger-interface':([560,719],[577,724],[488,764]),
    'under-little-toe':([578,1011],[504,989],[236,1059]),
    'ear-posterior-TE':(None,[399,254],[426,265]),
    'ear-internal-TE':([441,244],[395,244],[411,250]),
    'ear-anterior-TE':([445,244],None,[399,252]),
    'cheek-SI':([426,260],None,[349,269]),
    'nose-SI':([389,250],None,[301,253]),
    'cheek-TE':([426,260],None,[349,269]),
    }
    nodes={}
    for n in patches['anatomical_nodes']:
        key=n['id'].split('.',1)[1]
        assert key in C, key
        nodes[n['id']]={**n,'views':dict(zip(['front','back','side'],C[key]))}
    nodes['anatomy.middle-toe-ST']={'id':'anatomy.middle-toe-ST','label':'中指外間','layer':'surface','views':{'front':[576,1016],'back':None,'side':[244,1053]}}
    nodes['anatomy.ear-upper-BL']={'id':'anatomy.ear-upper-BL','label':'耳上角','layer':'surface','views':{'front':[442,219],'back':[400,210],'side':[414,215]}}
    edges=[]
    def chain(channel,ids,kind,source,note='',target=None):
        for a,b in zip(ids,ids[1:]):
            assert a in P or a in nodes,a
            assert b in P or b in nodes,b
            edges.append({'id':f'{channel}:{a}>{b}:{kind}','channel':channel,'from':a,'to':b,
                          'kind':kind,'source':source,'note':note,'nextChannel':target})
    for s in patches['surface_chains']:
        chart=s['kind'] in ['point-chart-only','point-chart-overlay']
        chain(s['channel'],s['nodes'],'chart' if chart else 'surface',s['source'],s['note'])
    for s in patches['deep_chains']:chain(s['channel'],s['nodes'],'deep',s['source'],s['note'])
    for i,s in enumerate(patches['handoffs']):
        target=evidence['cycle'][i]['to']
        deep=all(n.startswith('anatomy.') and nodes[n]['layer']=='deep' for n in s['nodes'])
        chain(s['channel'],s['nodes'],'deep-handoff' if deep else 'handoff',s['source'],s['note'],target)
    # Junctions whose source is a region, not necessarily an exact numbered point.
    additions=[
      ('LU',['LU7','anatomy.posterior-wrist'],'surface',195),
      ('ST',['ST42','anatomy.foot-dorsum-ST'],'surface',215),
      ('ST',['anatomy.stomach','anatomy.stomach-orifice'],'deep',213),
      ('ST',['ST36','anatomy.middle-toe-ST'],'surface',214),
      ('BL',['BL7','anatomy.vertex','anatomy.ear-upper-BL'],'surface',269),
      ('SP',['SP13','anatomy.abdomen'],'deep',234),
      ('SI',['SI15','ST12','SI16'],'surface',257),
      ('SI',['SI18','anatomy.cheek-SI'],'surface',259),
      ('BL',['BL10','anatomy.shoulder-back-BL'],'surface',271),
      ('BL',['BL23','anatomy.lumbar-BL'],'surface',272),
      ('KI',['KI10','anatomy.medial-posterior-thigh'],'deep',289),
      ('PC',['PC8','anatomy.palm-PC'],'surface',303),
      ('TE',['TE15','ST12'],'surface',313),
      ('TE',['TE18','anatomy.ear-posterior-TE'],'surface',315),
      ('GB',['GB41','anatomy.foot-dorsum-GB'],'surface',323),
      ('LR',['LR12','anatomy.lower-abdomen'],'deep',339),
      ('CV',['anatomy.lower-jiao-origin','CV1'],'deep',523),
      ('CV',['CV24','anatomy.inferior-orbit'],'surface',523),
      ('GV',['anatomy.lower-jiao-origin','GV1'],'deep',511),
      ('GV',['GV16','anatomy.brain'],'deep',511),
      ('GV',['anatomy.lower-jiao-origin','anatomy.kidney','anatomy.heart'],'deep',511)
    ]
    for c,ids,k,b in additions:chain(c,ids,k,[{'doc':'doc4','block':b}],
                                   '본문의 해부 부위를 가까운 혈위와 연결한 도식 접속점. 동일 혈위라는 판정이 아님.')
    # GB/LR chart routes have a separate anatomical course; no invented node at the toe to connect into liver.
    for c,ids,b in [
      ('GB',['GB1','ST8','GB12','GB20','GB21','ST12'],319),
      ('GB',['ST12','GB22','anatomy.lateral-ribs','GB30'],322),
      ('GB',['GB30','GB31','GB33','GB34','GB39','GB40','GB41','GB44'],322),
      ('LR',[f'LR{i}' for i in range(1,13)],339)]:
        chain(c,ids,'surface',[{'doc':'doc4','block':b}],'해부 구간의 표면 투영. 혈위 배열과 원문의 분지 전체를 구분한다.')
    # Two flank branches of the extraordinary channels are not the confluent-point shortcuts.
    for ex in evidence['extraordinary']:
        if ex['id'] in ['CV','GV']:continue
        ids=[p for p in ex['borrowed_or_owned_point_order'] if p in P]
        chain(ex['id'],ids,'extra',ex['source'],'교재의 교회혈 순서 투영. 통회혈에서 곧바로 출발하지 않음.')
    for ex,ids,kind,b in [
       ('CHONG',['anatomy.lower-jiao-origin','CV1','ST30'],'deep',535),
       ('CHONG',['KI21','anatomy.chest','anatomy.throat','anatomy.lip-inner'],'deep',535),
       ('CHONG',['ST30','anatomy.medial-posterior-thigh','KI10','KI3','KI1'],'extra',535),
       ('DAI',['LR13','GB26','GB27','GB28'],'extra',551)]:
        chain(ex,ids,kind,[{'doc':'doc4','block':b}])
    # Explicit exclusion checks apply even after adding branches.
    bad={(e['from'],e['to']) for e in patches['exclusions']}
    assert not any((e['from'],e['to']) in bad for e in edges)
    # Deduplicate repeated anatomical paths without discarding evidence.
    unique={}
    for e in edges:
        k=(e['channel'],e['from'],e['to'],e['kind'])
        if k in unique:unique[k]['source']+=e['source']
        else:unique[k]=e
    for n in nodes.values():
        refs=[r for e in unique.values() if n['id'] in [e['from'],e['to']] for r in e['source']]
        n['source']=refs or [{'doc':'doc4','loc':'유주 해부 표지'}]
    return list(nodes.values()),list(unique.values())

