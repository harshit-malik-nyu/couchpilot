"""Deterministic request boundaries shared conceptually with web/engine.mjs.

These checks constrain the model; passing them is not proof of semantic accuracy.
"""
import re
import unicodedata

STOP = set('the a an to me where is it in of this that please show explain about can you go take back and then my on with how why does do step chapter part save send phone card jump move navigate playback anything just without not dont don t keep there as for should we what these those into which at'.split())

def normalize(text):
    return unicodedata.normalize('NFKC', text).lower().replace('’', "'")

def tokens(text):
    return set(re.findall(r'[a-z0-9]+', normalize(text))) - STOP

def rank(query, segments):
    q = tokens(query)
    hits = [dict(s, score=len(q & tokens(' '.join(s['tags']))) * 4 + len(q & tokens(s['text']))) for s in segments]
    return sorted((s for s in hits if s['score']), key=lambda s: (-s['score'], s['start']))[:3]

def tools_for(query):
    q = normalize(query)
    seek = bool(re.search(r'\b(go|jump|seek|navigate|rewind|skip|find)\b|\btake (me|us)\b', q))
    card = bool(re.search(r'\b(phone|send|save|card)\b', q))
    # Scope negation to the action clause, not to every action in the request.
    no = r"(?:do not|don't|dont|never|without|no)\s+(?:\w+\s+){0,2}"
    if re.search(no+r'(?:jump|go|seek|navigate|rewind|skip|move|change|changing|find)\b', q): seek = False
    if re.search(no+r'(?:send|save|prepare|share)\b', q): card = False
    explain = bool(re.search(r'\bexplain\b|^(?:why|how|what)\b', q))
    if re.search(no+r'explain\b', q): explain = False
    tools = (['seek'] if seek else []) + (['explain'] if explain else []) + (['prepare_card'] if card else [])
    return tools or ['explain']

def inspect_request(query, current, segments):
    if not isinstance(query,str) or not 1 <= len(query.strip()) <= 500:
        raise ValueError('Use 1–500 characters')
    by_id = {s['id']:s for s in segments}
    if current not in by_id: raise ValueError('Unknown current segment')
    q = normalize(query)
    def stop(status, reason): return dict(status=status, reason=reason, tools=[], evidence=[], target=None)
    if re.search(r'\b(buy|purchase|subscribe|comment|password|ignore|delete|secret|system)\b|https?://', q):
        return stop('unsupported','Account actions, external links and instruction overrides are outside this lesson.')
    target = None
    number = re.search(r'\bstep\s+(\d+)\b',q)
    ordinal = next((i for i,w in enumerate(['first','second','third','fourth','fifth'],1) if re.search(r'\b'+w+r'\s+step\b',q)),None)
    relative = re.search(r'\b(next|previous)\s+(?:step|chapter)\b',q)
    if number or ordinal:
        step = int(number.group(1)) if number else ordinal
        if step not in range(1,6): return stop('unsupported','This lesson contains steps 1 through 5.')
        target = next(s['id'] for s in segments if s['step']==step)
    elif relative:
        step = by_id[current]['step'] + (1 if relative.group(1)=='next' else -1)
        target = next((s['id'] for s in segments if s['step']==step),None)
        if target is None: return stop('clarify','There is no chapter in that direction. Choose a listed chapter.')
    explicit = set(re.findall(r'\b(denominator|assignment|uncertainty|guardrails?|review|introduction)\b',q))
    explicit = {'guardrails' if x in ('guardrail','guardrails') else 'intro' if x=='introduction' else x for x in explicit}
    if len(explicit)>1: return stop('clarify','Choose one chapter per request; these topics have different sources.')
    if not target and explicit: target = next(iter(explicit))
    if not target and re.search(r'\b(this|here|current)\b',q): target = current
    hits = [dict(by_id[target],score=100)] if target else rank(q,segments)
    if not hits:
        generic = not tokens(q) or re.search(r'\b(?:the step|next|previous|there)\b',q)
        return stop('clarify' if generic else 'unsupported','Specify one chapter or ask about a lesson topic.')
    if not target and len(hits)>1 and hits[0]['score']==hits[1]['score']:
        return stop('clarify','Two source chapters match equally. Choose one chapter.')
    return dict(status='ready', reason='Within the lesson and action boundary.', tools=tools_for(q), evidence=hits, target=target)
