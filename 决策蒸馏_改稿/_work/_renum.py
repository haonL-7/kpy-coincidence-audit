# -*- coding: utf-8 -*-
import io, re, json

src='draft_v2.md'
t=io.open(src,encoding='utf-8').read()

head, refs = t.split('## 参考文献')
refs='## 参考文献'+refs

TOK=re.compile(r'\[(\d+(?:[-,]\d+)*)\]')

def expand(tok):
    # tok like '1' or '2-5' ; no comma ranges present but handle anyway
    out=[]
    for part in tok.split(','):
        if '-' in part:
            a,b=part.split('-'); out.extend(range(int(a),int(b)+1))
        else:
            out.append(int(part))
    return out

# ---- 1. first-appearance order in body ----
order=[]
for m in TOK.finditer(head):
    for n in expand(m.group(1)):
        if n not in order:
            order.append(n)
print('first-appearance order:', order)
assert len(order)==18, len(order)
mapping={old:i+1 for i,old in enumerate(order)}
print('mapping:', mapping)

# ---- 2. body replace (single pass, whole-token) ----
def repl(m):
    inner=m.group(1)
    parts=[]
    for part in inner.split(','):
        if '-' in part:
            a,b=part.split('-')
            na,nb=mapping[int(a)],mapping[int(b)]
            nums=[mapping[x] for x in range(int(a),int(b)+1)]
            # keep range form only if new numbers are contiguous ascending
            if nums==list(range(min(nums),max(nums)+1)) and nums==sorted(nums):
                parts.append('%d-%d'%(nums[0],nums[-1]))
            else:
                parts.append(','.join(str(x) for x in nums))
        else:
            parts.append(str(mapping[int(part)]))
    return '['+','.join(parts)+']'

head_new=TOK.sub(repl, head)

# ---- 3. reorder reference entries ----
lines=[l for l in refs.split('\n')]
heading=lines[0]
entries=[l for l in lines[1:] if l.strip()]
assert len(entries)==18, len(entries)
byno={}
for e in entries:
    m=re.match(r'^\[(\d+)\]\s*(.*)$', e)
    assert m, e[:40]
    byno[int(m.group(1))]=m.group(2)
assert sorted(byno)==list(range(1,19))
new_entries=[]
for newno in range(1,19):
    oldno=[o for o in mapping if mapping[o]==newno][0]
    new_entries.append('[%d] %s'%(newno, byno[oldno]))

out = head_new.rstrip('\n') + '\n\n' + heading + '\n\n' + '\n\n'.join(new_entries) + '\n'
io.open('draft_final.md','w',encoding='utf-8').write(out)

# ---- verification ----
f=io.open('draft_final.md',encoding='utf-8').read()
fh, fr = f.split('## 参考文献')
order2=[]
for m in TOK.finditer(fh):
    for n in expand(m.group(1)):
        if n not in order2: order2.append(n)
tok_before=len(TOK.findall(head)); tok_after=len(TOK.findall(fh))
num_before=sum(len(expand(m.group(1))) for m in TOK.finditer(head))
num_after=sum(len(expand(m.group(1))) for m in TOK.finditer(fh))
chk={}
chk['first_appearance_strict']= order2==list(range(1,19))
chk['first_appearance_sequence']=order2
chk['tokens_before_after']=[tok_before,tok_after]
chk['expanded_before_after']=[num_before,num_after]
chk['entry_count']=len([l for l in fr.split('\n') if re.match(r'^\[\d+\] ',l)])
chk['entries_seq_1_18']=[int(re.match(r'^\[(\d+)\] ',l).group(1)) for l in fr.split('\n') if re.match(r'^\[\d+\] ',l)]==list(range(1,19))
# every cited number has an entry
cited=set()
for m in TOK.finditer(fh): cited.update(expand(m.group(1)))
have=set(int(re.match(r'^\[(\d+)\] ',l).group(1)) for l in fr.split('\n') if re.match(r'^\[\d+\] ',l))
chk['cited_without_entry']=sorted(cited-have)
chk['entry_without_citation']=sorted(have-cited)
# entry text preserved (ignoring number label)
orig_texts=sorted(byno.values()); new_texts=sorted(re.match(r'^\[\d+\] (.*)$',l).group(1) for l in fr.split('\n') if re.match(r'^\[\d+\] ',l))
chk['entry_texts_identical']=orig_texts==new_texts
io.open('_work/renumber.json','w',encoding='utf-8').write(json.dumps({'mapping':mapping,'order':order,'chk':chk},ensure_ascii=False,indent=1))
print(json.dumps(chk,ensure_ascii=False)[:1200])
